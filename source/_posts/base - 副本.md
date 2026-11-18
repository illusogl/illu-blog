---
title: ManagerOfManagers架构
date: 2026-11-16 10:29:00
categories:
  - 架构
tags:
  - 架构
  - Unity
---

> ManagerOfManagers架构

<!-- more -->

## 什么是ManagerOfManagers架构

在一个大型的游戏框架中 我们可能需要一大堆的单例管理器 例如`UIMgr`，`AudioMgr` ………… 为了管理这么多的管理器我们就需要引用一个更大的中央管理器`GameManager`来管理这些小管理器 这就是所谓的`ManagerOfManagers(MOM)`架构

## 实现

由于要管理众多单例模式 我们可以通过一个简单的抽象类来实现单例模式
```csharp
public abstract class Singleton<T> where T : class, new()
{
    private static T _instance;
    public abstract void Init();

    public static T Instance
    {
        get
        {
            if(_instance == null)
                _instance = new T();
            return _instance;
        }
    }
}
```
普通的Manager类的接口
```csharp
public abstract inter IBaseManager
{
    public abstract void OnInit();
    public abstract void OnClear();
}
```


GameManager的实现逻辑

```csharp
using System;
using System.Collections.Generic;
namespace Manager
{
    /// <summary>
    /// Manager入口
    /// </summary>
    public partial class GameManager : Singleton<GameManager>
    {
        //用一个map字典来管理其余的Mgr
        private Dictionary<Type,BaseManager> managerDic = new Dictionary<Type, BaseManager>();

        public override void Init()
        {
            OnInit();
        }
        //寻找对应的Mgr，没有就放进去
        public T Get<T>() where T : BaseManager, new()
        {
            Type type = typeof(T);
            if (!managerDic.ContainsKey(type))
            {
                T manager = new T();
                manager.OnInit();
                managerDic[type] = manager;
            }
            return (T)managerDic[type];
        }
        //删除Mgr
        public void ClearManager<T>(T type) where T : BaseManager, new()
        {
            if(managerDic.ContainsKey(type as Type))
            {
                type.OnClear();
                managerDic[type as Type] = null;
                type = null;
            }
        }
        //删掉所有的Mgr
        public void CleaerAllManagers()
        {
            foreach (var keyValuePair in managerDic)
            {
                keyValuePair.Value.OnClear();
                BaseManager manager = keyValuePair.Value;
                manager = null;
            }
            managerDic.Clear();
        }
    }
}
```

