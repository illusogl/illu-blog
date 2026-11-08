---
title: "C# 语法补充：readonly"
date: 2026-11-08 18:00:00
categories:
  - "C#"
tags:
  - "C#"
---

## readonly 的作用
`private` 和 `readonly` 的区别：
- **`private` 管“谁能访问”**：类外部看不到这个字段。
- **`readonly` 管“谁能赋值”**：只能在声明时或构造函数里赋值，之后不能重新赋值。
它的作用是**防止后续代码意外改掉初始化时确定下来的依赖**，同时表达“这个字段创建后就不应该再变”。

<!-- more -->

## readonly 的赋值时机
`readonly` 字段可以在以下位置赋值：
1. 声明时直接初始化：
   ```csharp
   private readonly int maxCount = 10;
   ```
2. 构造函数里赋值：
   ```csharp
   private readonly Action<T> actionOnDestroy;

   public MyObjectPool(Action<T> actionOnDestroy)
   {
       this.actionOnDestroy = actionOnDestroy;
   }
   ```
不能在普通方法里再次赋值：
```csharp
void Clear()
{
    actionOnDestroy = null; // 编译错误
}
```
## readonly 只锁引用，不锁内容
`readonly` 对引用类型只保证“引用不能变”，不保证“对象内容不能变”：
```csharp
private readonly Stack<T> pool = new Stack<T>();
pool = new Stack<T>(); // 不行：不能换引用
pool.Push(item);       // 可以：修改对象内容
pool.Clear();          // 可以：修改对象内容
```
所以下面这种写法很常见：
```csharp
private readonly List<GameObject> cubes = new List<GameObject>();
```
意思是“`cubes` 这个列表引用不能换，但列表里可以增删元素”。
## 常见使用场景
`readonly` 用于“创建后不应该再改变”的字段，例如：

- 构造函数注入的依赖：
  ```csharp
  private readonly Action<T> actionOnGet;
  private readonly Action<T> actionOnRelease;
  ```
- 只初始化一次的集合：
  ```csharp
  private readonly Stack<T> pool = new Stack<T>();
  ```
- 配置值：
  ```csharp
  private readonly int maxSize;
  ```
- 静态只读实例：
  ```csharp
  private static readonly MyObjectPool<GameObject> Instance = new MyObjectPool<GameObject>(...);
  ```