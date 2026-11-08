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
