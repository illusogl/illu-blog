using System.Collections.Generic;
using UnityEngine;

/// <summary>
/// A* 的演示脚本。生成一张测试地图，从 (0, 0) 寻路到 target 所在位置。
/// </summary>
public class AstarDemo : MonoBehaviour
{
    [SerializeField] private Transform target;

    /// <summary>
    /// 生成测试地图并执行一次寻路，把路径逐格输出到 Console。
    /// 目标为空时默认使用 (40, 40) 作为终点。
    /// </summary>
    private void Start()
    {
        AstarMgr mgr = AstarMgr.Instance;
        BuildTestMap(mgr);

        Vector2 end = target != null
            ? (Vector2)target.position
            : new Vector2(40, 40);

        List<AstarNode> path = mgr.FindPath(Vector2.zero, end);

        if (path == null)
        {
            Debug.LogWarning("没有可行路径");
            return;
        }

        foreach (AstarNode node in path)
            Debug.Log($"({node.x}, {node.y})");
    }

    /// <summary>
    /// 生成一张 48×48 的测试地图：中间竖一堵墙，只在 y = 18..21 留一个缺口。
    /// </summary>
    /// <param name="mgr">要修改的寻路管理器。</param>
    private static void BuildTestMap(AstarMgr mgr)
    {
        for (int x = 0; x < AstarMgr.Size; x++)
        {
            for (int y = 0; y < AstarMgr.Size; y++)
                mgr.nodes[x, y].nodeType = NodeType.Normal;
        }

        for (int y = 0; y < AstarMgr.Size; y++)
            mgr.nodes[24, y].nodeType = NodeType.Obstacle;

        for (int y = 18; y < 22; y++)
            mgr.nodes[24, y].nodeType = NodeType.Normal;
    }
}
