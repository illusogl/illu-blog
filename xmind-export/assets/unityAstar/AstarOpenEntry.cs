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
