using System.Collections.Generic;
using UnityEngine;

/// <summary>
/// A* 网格寻路管理器。负责维护 48×48 的节点地图、开放列表和最终路径。
/// 开放列表使用 SortedSet 保存不可变条目，旧条目通过惰性删除跳过。
/// </summary>
public class AstarMgr
{
    /// <summary>
    /// 地图边长。数组长度和边界判断共用这个常量，避免出现数组开 48、边界写 47 的问题。
    /// </summary>
    public const int Size = 48;

    private const float StraightCost = 1f;
    private const float DiagonalCost = 1.41421356f;

    private static readonly Vector2Int[] Dirs =
    {
        new Vector2Int(1, 0),
        new Vector2Int(-1, 0),
        new Vector2Int(0, 1),
        new Vector2Int(0, -1),
        new Vector2Int(1, 1),
        new Vector2Int(1, -1),
        new Vector2Int(-1, 1),
        new Vector2Int(-1, -1)
    };

    private static AstarMgr instance;

    /// <summary>
    /// 全局唯一实例。AstarMgr 不是 MonoBehaviour，第一次访问时创建。
    /// </summary>
    public static AstarMgr Instance
    {
        get
        {
            if (instance == null)
                instance = new AstarMgr();

            return instance;
        }
    }

    /// <summary>
    /// 网格节点数组，按 nodes[x, y] 访问。
    /// </summary>
    public readonly AstarNode[,] nodes;

    /// <summary>
    /// 已处理节点。仅用于调试或可视化，判断是否关闭请使用 node.isClosed。
    /// </summary>
    public readonly List<AstarNode> closeList = new List<AstarNode>();

    /// <summary>
    /// 最近一次搜索得到的路径，从起点到终点排列。下一次 FindPath 会清空它。
    /// </summary>
    public readonly List<AstarNode> pathList = new List<AstarNode>();

    /// <summary>
    /// 最近一次搜索是否找到了路径。
    /// </summary>
    public bool pathFound;

    /// <summary>
    /// 是否正在执行寻路。可用于控制调试绘制，避免搜索过程中重复绘制。
    /// </summary>
    public bool IsUse;

    // 开放列表保存的是不可变快照，同一个节点可能对应多条记录。
    private readonly SortedSet<AstarOpenEntry> _openList = new SortedSet<AstarOpenEntry>();

    // 入队序号，用来区分同一个节点或相同 F/H 的多条记录。
    private long _sequence;

    // 记录本次搜索碰过的节点，下次搜索只重置这些节点，不用遍历整张图。
    private readonly List<AstarNode> _touched = new List<AstarNode>();

    /// <summary>
    /// 创建 48×48 的网格，所有节点默认都是可通行的普通节点。
    /// 外部通过 AstarMgr.Instance 获取单例。
    /// </summary>
    private AstarMgr()
    {
        nodes = new AstarNode[Size, Size];

        for (int x = 0; x < Size; x++)
        {
            for (int y = 0; y < Size; y++)
                nodes[x, y] = new AstarNode(x, y);
        }
    }

    /// <summary>
    /// 重置上一次搜索留下的状态。
    /// 清空开放列表、关闭列表和路径列表，并只重置本次搜索碰过的节点。
    /// </summary>
    public void Initialize()
    {
        _openList.Clear();
        _sequence = 0;
        closeList.Clear();
        pathList.Clear();

        for (int i = 0; i < _touched.Count; i++)
            _touched[i].Reset();

        _touched.Clear();
        pathFound = false;
    }

    /// <summary>
    /// 计算从起点到终点的路径。
    /// 返回的列表包含起点和终点；找不到路径时返回 null。
    /// </summary>
    /// <param name="start">起点坐标，可以是世界坐标，内部会自动四舍五入到格子。</param>
    /// <param name="end">终点坐标，可以是世界坐标，内部会自动四舍五入到格子。</param>
    /// <returns>从起点到终点的节点列表；无路可走或坐标非法时返回 null。</returns>
    public List<AstarNode> FindPath(Vector2 start, Vector2 end)
    {
        Initialize();
        IsUse = true;

        if (!TryGetNode(start, out AstarNode startNode) ||
            !TryGetNode(end, out AstarNode endNode))
            return Fail();

        AddToOpen(startNode, null, 0f, endNode);

        while (_openList.Count > 0)
        {
            AstarOpenEntry entry = _openList.Min;
            _openList.Remove(entry);

            AstarNode current = entry.node;

            // 节点已经关闭，或者这条记录的 G 比节点当前最优 G 更差，
            // 说明它是一条过期记录，直接跳过。
            if (current.isClosed || entry.gCost > current.gCost)
                continue;

            // 接受这条记录：把快照里的父节点和分数提交到节点上。
            current.gCost = entry.gCost;
            current.hCost = entry.hCost;
            current.parentNode = entry.parent;
            current.isClosed = true;
            closeList.Add(current);

            if (current == endNode)
                return BuildPath(endNode);

            ExpandNeighbors(current, endNode);
        }

        return Fail();
    }

    /// <summary>
    /// 扩展当前节点的八个邻居。
    /// 对每个可通行邻居计算新的 G，如果比邻居当前最优 G 更小，就生成一条新的开放列表记录。
    /// </summary>
    /// <param name="current">当前正在处理的节点。</param>
    /// <param name="goal">寻路终点，用来计算邻居的 H 值。</param>
    private void ExpandNeighbors(AstarNode current, AstarNode goal)
    {
        for (int i = 0; i < Dirs.Length; i++)
        {
            Vector2Int dir = Dirs[i];

            if (!TryGetNode(current.x + dir.x, current.y + dir.y, out AstarNode neighbor))
                continue;

            if (neighbor.isClosed)
                continue;

            bool diagonal = dir.x != 0 && dir.y != 0;
            if (diagonal && !CanMoveDiagonally(current, dir))
                continue;

            float newG = current.gCost + (diagonal ? DiagonalCost : StraightCost);
            if (newG >= neighbor.gCost)
                continue;

            AddToOpen(neighbor, current, newG, goal);
        }
    }

    /// <summary>
    /// 生成一条新的开放列表记录。
    /// 这里只更新节点的最优 G/H，不修改节点父节点；父节点要等记录真正出队时才提交，
    /// 这样旧记录不会覆盖新路径的父节点。
    /// </summary>
    /// <param name="node">要加入开放列表的节点。</param>
    /// <param name="parent">到达该节点所使用的父节点，起点可以为 null。</param>
    /// <param name="gCost">从起点到该节点的新 G 值。</param>
    /// <param name="goal">寻路终点，用来计算 H 值。</param>
    private void AddToOpen(AstarNode node, AstarNode parent, float gCost, AstarNode goal)
    {
        if (node.isClosed)
            return;

        // G 还是正无穷，说明这是该节点第一次被访问，需要记录到 touched 里。
        if (float.IsPositiveInfinity(node.gCost))
            _touched.Add(node);

        float hCost = Heuristic(node, goal);
        node.gCost = gCost;
        node.hCost = hCost;

        _openList.Add(new AstarOpenEntry(node, parent, gCost, hCost, _sequence++));
    }

    /// <summary>
    /// 从终点沿 parentNode 回溯到起点，并反转成从起点到终点的顺序。
    /// 同时更新 pathFound 和 IsUse 状态。
    /// </summary>
    /// <param name="endNode">寻路终点。</param>
    /// <returns>从起点到终点的节点列表。</returns>
    private List<AstarNode> BuildPath(AstarNode endNode)
    {
        for (AstarNode node = endNode; node != null; node = node.parentNode)
            pathList.Add(node);

        pathList.Reverse();
        pathFound = true;
        IsUse = false;
        return pathList;
    }

    /// <summary>
    /// 统一处理寻路失败：清除搜索状态并返回 null。
    /// </summary>
    /// <returns>始终返回 null。</returns>
    private List<AstarNode> Fail()
    {
        pathFound = false;
        IsUse = false;
        return null;
    }

    /// <summary>
    /// 把浮点坐标四舍五入到格子坐标，并取出对应节点。
    /// </summary>
    /// <param name="pos">世界坐标或浮点格子坐标。</param>
    /// <param name="node">取到的节点；坐标越界或节点是障碍时为 null。</param>
    /// <returns>坐标合法且节点可通行时返回 true。</returns>
    private bool TryGetNode(Vector2 pos, out AstarNode node)
    {
        return TryGetNode(Mathf.RoundToInt(pos.x), Mathf.RoundToInt(pos.y), out node);
    }

    /// <summary>
    /// 检查整数坐标是否在地图内且不是障碍，并取出对应节点。
    /// </summary>
    /// <param name="x">格子 X 坐标。</param>
    /// <param name="y">格子 Y 坐标。</param>
    /// <param name="node">取到的节点；坐标越界或节点是障碍时为 null。</param>
    /// <returns>坐标合法且节点可通行时返回 true。</returns>
    private bool TryGetNode(int x, int y, out AstarNode node)
    {
        if (x < 0 || x >= Size || y < 0 || y >= Size ||
            nodes[x, y].nodeType == NodeType.Obstacle)
        {
            node = null;
            return false;
        }

        node = nodes[x, y];
        return true;
    }

    /// <summary>
    /// 判断能否从当前节点沿指定方向斜向移动。
    /// 要求两个直角相邻格都不是障碍，避免角色从墙角夹缝中穿过去。
    /// </summary>
    /// <param name="from">当前节点。</param>
    /// <param name="dir">斜向移动方向，两个分量都不为 0。</param>
    /// <returns>两个直角相邻格都可行走时返回 true。</returns>
    private bool CanMoveDiagonally(AstarNode from, Vector2Int dir)
    {
        return nodes[from.x + dir.x, from.y].nodeType != NodeType.Obstacle &&
               nodes[from.x, from.y + dir.y].nodeType != NodeType.Obstacle;
    }

    /// <summary>
    /// 计算八方向网格上的对角距离（octile distance），作为 A* 的 H 值。
    /// 该启发函数不会高估真实代价，因此可以保证找到最短路。
    /// </summary>
    /// <param name="a">起点节点。</param>
    /// <param name="b">终点节点。</param>
    /// <returns>两个节点之间的估计代价。</returns>
    private static float Heuristic(AstarNode a, AstarNode b)
    {
        int dx = Mathf.Abs(a.x - b.x);
        int dy = Mathf.Abs(a.y - b.y);
        int diagonal = Mathf.Min(dx, dy);

        return (dx + dy) * StraightCost +
               (DiagonalCost - 2f * StraightCost) * diagonal;
    }
}
