#include<bits/stdc++.h>
using namespace std;
class Solution {
public:
    //并查集查找父亲节点的代码，如果不是最终的父亲则会往上继续递归查找
    int Find(vector<int> &parent,int index)
    {
        if(parent[index] != index)
        {
            parent[index] = Find(parent,parent[index]);
        }
        return parent[index];
    }
    //并查集合并的代码，将两个根节点判断大小，让小的当最大根
    void Union(vector<int>& parent, vector<int>& rank, int index1, int index2) {
        int x = Find(parent, index1);
        int y = Find(parent, index2);
        if (x == y) return;       
        // 按树高合并：矮树挂到高树下
        if (rank[x] < rank[y]) 
        {
            parent[x] = y;
        } 
        else if (rank[x] > rank[y]) 
        {
            parent[y] = x;
        } 
        else 
        {
            parent[y] = x;
            rank[x]++;
        }
    }
    //根据并查集检测无向图中的环并找到冗余边。
    vector<int> findRedundantConnection(vector<vector<int>>& edges) 
    {
        int n = edges.size();
        vector<int> rank(n+1);
        vector<int> parent(n + 1);
        vector<int> ans;
        for(int i = 1; i <= n; i++)
        {
            parent[i] = i;
        }
        for(vector<int> p : edges)
        {
            //依据题目要求 如果无向图中两个节点的父节点相同，则说明构成了回路，可以返回答案
            if(Find(parent,parent[p[0]]) == Find(parent,parent[p[1]]))
            {
                ans = {p[0],p[1]};
            }
            //如果不构成回路则连接两节点
            else
            {
                Union(parent,rank,p[0],p[1]);
            }
        }
        return ans;
    }
    //利用dsu找有向图中弱联通区域数
    void find_WeaklyConnected_in_digraph(int lineLength, vector<int> rank ,vector<int> startPos ,vector<int> endPos )
    {
        vector<int> graph(20);
        for(int i = 0; i < 20; i++)
        {
            graph[i] = i;
        }
        for(int i = 0; i < lineLength;i++)
        {
            Union(graph,rank,startPos[i],endPos[i]);
        }
        for(int i = 0; i < lineLength;i++)
        {
            Union(graph,rank,endPos[i],startPos[i]);
        }
        set<int> Count;
        for(int i = 0;i < 20;i++)
        {
            Count.insert(graph[i]);
        }
        cout << Count.size() << "\n";
    }
};