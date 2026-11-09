---
title: 在 Unity 实现一个简单的 A* 寻路
date: 2026-11-04 17:10:00
categories:
  - Unity
tags:
  - Unity
  - C#
  - 算法
  - 寻路
---

> 这是博客搭好后的第一篇文章，也是一次排版测试。代码来自我项目里的 `AstarMgr` / `AstarNode`。

<!-- more -->

## 为什么从 A* 开始

A* 是我最早接触的寻路算法之一，心血来潮想搭建一个博客，说以把他从项目里翻出来重新整理一遍作为第一篇博客的文章。


## 核心公式

A* 给每个待探索的节点算一个分数：

| 符号 | 含义 | 在网格里的取值 |
| --- | --- | --- |
| `G(n)` | 从起点走到 `n` 的实际代价 | 直走 `1`，斜走 `sqrt（2）` |
| `H(n)` | 从 `n` 到终点的估计代价 | 八方向用对角距离 |
| `F(n)` | `G(n) + H(n)` | 每次取最小的 |

这里用的是八方向移动，所以 `H` 不能再用曼哈顿距离。曼哈顿距离会把斜走估计成 `2`，而实际只要 `1.414`，A* 可能因此错过最短路。正确做法是对角距离（octile distance）：

```text
dx = |x1 - x2|
dy = |y1 - y2|
H = (dx + dy) + (√2 - 2) * min(dx, dy)
```
A*算法的核心逻辑就是用一个优先队列来存候补的路径，从起点开始 每次从优先队列取一个路径代价最小的点，将他加入行动路径并且将它周围八方向所有未走过点加入优先队列
直到走到终点为止，从到终点的行动路径往回走到起点给出最终路径

## 节点和网格

地图是 `AstarNode[48, 48]`，按 `nodes[x, y]` 访问。节点类型保留原来的 `Normal / Obstacle / Start / End`，其中 A* 真正关心的是 `Obstacle`，`Start` 和 `End` 更多是给地图编辑或可视化用的标记。

每个节点保存坐标、父节点、`G / H` 两个分数和一个 `isClosed` 标记。未访问节点的 `G` 初始化为正无穷，这样 `newG < gCost` 可以直接判断“是否找到了更短的走法”

## AstarNode.cs

```csharp
using UnityEngine;

/// <summary>
/// 网格节点类型。A* 只把 Obstacle 视为不可通行。
/// </summary>
public enum NodeType
{
    Normal,
    Obstacle,
    Start,
    End
}

/// <summary>
/// 网格节点。保存坐标、节点类型、父节点以及 A* 使用的 G/H 分数。
/// </summary>
public class AstarNode
{
    public readonly int x;
    public readonly int y;

    public NodeType nodeType;
    public AstarNode parentNode;
    public float gCost;
    public float hCost;

    /// <summary>
    /// F = G + H。节点自身的 F 只用于调试，开放列表使用条目里的快照值。
    /// </summary>
    public float fCost => gCost + hCost;

    /// <summary>
    /// 是否已经处理过。关闭的节点不会再被扩展。
    /// </summary>
    public bool isClosed;

    /// <summary>
    /// 创建一个网格节点。
    /// 未访问节点的 G 初始化为正无穷，这样 newG 小于 gCost 可以直接判断是否首次访问。
    /// </summary>
    /// <param name="x">网格 X 坐标。</param>
    /// <param name="y">网格 Y 坐标。</param>
    /// <param name="nodeType">节点类型，默认是可通行的普通节点。</param>
    public AstarNode(int x, int y, NodeType nodeType = NodeType.Normal)
    {
        this.x = x;
        this.y = y;
        this.nodeType = nodeType;
        gCost = float.PositiveInfinity;
    }

    /// <summary>
    /// 清除上一次寻路留下的父节点、G/H 分数和搜索状态，方便节点复用。
    /// </summary>
    public void Reset()
    {
        parentNode = null;
        gCost = float.PositiveInfinity;
        hCost = 0f;
        isClosed = false;
    }
}
```

`Reset` 是复用节点时用的。每次寻路都 `new` 一批节点当然也可以，但 48×48 的图每次搜索都重新分配没有必要。

## AstarOpenEntry.cs：开放列表里的不可变记录

```text
Entry = (node, parent, gCost, hCost, sequence)
```

每次发现更短的路径，就新建一条记录加入 `SortedSet`；旧记录不主动删除，等它排到集合最前面、出队时再丢弃。这样节点降权时不需要 `Remove + Add`，写起来更像迪杰斯特拉更方便理解。

几个关键点：

- **记录不可变**：`F / H` 在入队时就算好并固定下来，之后节点怎么变化都不会破坏 `SortedSet` 的红黑树排序
- **`sequence` 唯一**：同一个节点可能有多条记录，F/H 也可能相同，自增序号保证两条不同记录不会比较为 0，`SortedSet` 不会把它们当成重复元素
- **惰性删除**：出队时如果 `entry.gCost > node.gCost`，说明节点已经找到更短路径，这条记录过期，直接跳过
- **父节点放在记录里**：节点自己的 `parentNode` 要等记录真正出队时才提交，旧记录不会覆盖新路径的父节点

代价是最坏情况下集合里会有 `O(E)` 条记录，而不是每个节点一条；旧记录也要逐个出队丢弃。网格里 `E ≈ 8V`，算法时间复杂度能控制在O(ElogE)

```csharp
using System;

/// <summary>
/// 开放列表中的一条不可变记录。
/// 它保存节点、父节点以及入队时的 G/H 快照，因此节点之后怎么变化都不会破坏集合的排序。
/// sequence 是唯一序号，用来区分同一个节点的多条记录，也用来保证两条不同记录不会比较为 0。
/// </summary>
public readonly struct AstarOpenEntry : IComparable<AstarOpenEntry>
{
    public readonly AstarNode node;
    public readonly AstarNode parent;
    public readonly float gCost;
    public readonly float hCost;
    public readonly float fCost;

    /// <summary>
    /// 入队序号。数值越小表示越早入队，只在 F、H 都相同时用于打破平局。
    /// </summary>
    public readonly long sequence;

    /// <summary>
    /// 创建一条开放列表记录。
    /// F 和 H 会在这里固定下来，之后不再修改。
    /// </summary>
    /// <param name="node">要记录的节点。</param>
    /// <param name="parent">到达该节点时使用的父节点，起点可以为 null。</param>
    /// <param name="gCost">从起点到该节点的实际代价。</param>
    /// <param name="hCost">从该节点到终点的估计代价。</param>
    /// <param name="sequence">唯一入队序号。</param>
    public AstarOpenEntry(AstarNode node, AstarNode parent, float gCost, float hCost, long sequence)
    {
        this.node = node;
        this.parent = parent;
        this.gCost = gCost;
        this.hCost = hCost;
        fCost = gCost + hCost;
        this.sequence = sequence;
    }

    /// <summary>
    /// 比较两条记录的优先级：先比 F，再比 H，最后用入队序号保证顺序唯一。
    /// </summary>
    /// <param name="other">另一条记录。</param>
    /// <returns>负数表示当前记录优先，正数表示另一条优先，0 表示比较的是同一条记录。</returns>
    public int CompareTo(AstarOpenEntry other)
    {
        int result = fCost.CompareTo(other.fCost);
        if (result != 0)
            return result;

        result = hCost.CompareTo(other.hCost);
        if (result != 0)
            return result;

        return sequence.CompareTo(other.sequence);
    }
}
```

## AstarMgr.cs

由于unity的C#不能用优先队列，这里用set代替 核心存储数据的容器是`SortedSet<AstarOpenEntry>`。`FindPath` 从集合里取最小 `F` 的记录，确认它没有过期后，才把记录里的父节点和分数提交到节点上。

```csharp
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
```

现在 `FindPath` 只剩下“重置 → 校验 → 起点入队 → 取最小记录 → 确认记录 → 到终点就回溯 → 否则扩展邻居 → 没路了返回失败”这条主线，具体细节都拆到了独立方法里：

| 方法 | 职责 |
| --- | --- |
| `Initialize` | 清空容器，只重置上一次搜索碰过的节点 |
| `TryGetNode` | 坐标取整、边界判断、障碍判断 |
| `Heuristic` | 八方向对角距离 |
| `AddToOpen` | 生成一条新的不可变记录并加入集合 |
| `ExpandNeighbors` | 遍历八个方向，计算新的 `G` 并决定是否松弛 |
| `BuildPath` | 从终点沿 `parentNode` 回溯并反转 |
| `Fail` | 统一处理失败状态 |

几个实现细节：

- `closeList` 还在，但只用于调试或画格子，判断是否关闭直接读 `node.isClosed`，是 O(1)。
- 只有在 `newG < neighbor.gCost` 时才生成新记录。旧记录留下来，靠出队时的 G 比较丢弃。
- 记录出队时先检查 `entry.gCost > current.gCost`。如果节点已经通过更短的路径更新过，这条记录就是旧数据。
- 节点的 `parentNode` 只在记录被接受时提交，保证最终路径对应的是最优的那条记录。
- 斜走前检查两个相邻的直角格，避免从两个障碍的夹角里穿过去。
- `Initialize` 不遍历整张图，只重置 `_touched` 里记录过的节点，地图再大也不会每次搜索都全表扫描。

## 复杂度

设节点数为 `V`，边数为 `E`。网格里每个节点最多八个邻居，所以 `E` 大约是 `8V`。

| 取最小 F 的方式 | 查找 open / closed | 时间复杂度 | 空间 |
| --- | --- | --- | --- |
| `List` 线性扫描 | `Contains` O(V) | 接近 `O(V²)` | `O(V)` |
| 每轮 `Sort` | `Contains` O(V) | `O(V² log V)` | `O(V)` |
| `SortedSet` + 不可变条目（本文） | 出队时比较 G，O(1) | `O(E log E)` | `O(E)` |

每条成功松弛的边都会产生一条记录，最坏情况下集合里有 `O(E)` 条记录。网格里 `E ≈ 8V`，所以时间可以看作 `O(V log V)` 的量级，只是常数和内存会比“每个节点一条记录”的索引堆大一些。

## 几个容易踩的坑

1. **在邻居循环里用 `List.Contains`**：每个邻居都扫一遍开放/关闭列表，节点一多就会变成主要开销。
2. **`closeList` 重复添加**：原代码在弹出当前节点时加了一次，循环末尾又把 `openList[0]` 加了一次；后者既可能重复，也没有从开放列表移除，容易让节点提前被当成已关闭。现在只在弹出时标记一次。
3. **不比较 `G` 就覆盖父节点**：同一个节点可能先被一条差路径访问，后来才发现更短的走法。必须先比较 `newG` 和旧的 `gCost`。
4. **八方向用曼哈顿距离**：`H` 会高估斜走的代价，A* 可能找不到最短路。八方向要用对角距离。
5. **允许斜穿墙角**：两个障碍斜着摆时，角色会从夹缝中穿过去。斜走前要检查两个直角邻居。
6. **浮点坐标直接参与索引**：`(int)` 是向零截断，不是四舍五入，负坐标尤其容易落到错误的格子。先 `RoundToInt`，再判断边界。
7. **返回的 `pathList` 是复用的**：下一次 `FindPath` 会清空它。如果调用方需要长期保存路径，先复制一份。
8. **直接在 `SortedSet` 里改节点的 `F / H`**：节点在集合里时排序键必须稳定，改分数会破坏红黑树。本文把分数放进不可变的 `AstarOpenEntry` 快照里。
9. **惰性删除忘了判过期**：出队时如果不比较 `entry.gCost` 和 `node.gCost`，旧记录可能用更差的 `G` 把节点关闭。需要同时检查 `isClosed` 和 G。
