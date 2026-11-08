---
title: "Unity 对象池"
date: 2026-11-08 18:10:00
categories:
  - "Unity"
tags:
  - "Unity"
  - "C#"
  - "优化架构"
---

> 根据前面的对象池实现、官方 `ObjectPool<T>` 对比、`Clear/Dispose` 改造和 C# 语法讨论整理。

<!-- more -->

## 1. 对象池是干什么的

### 1.1 解决什么问题

在 Unity 里频繁创建和销毁对象，成本很高：

```csharp
Instantiate(prefab); // 创建 GameObject、组件、物理体、渲染对象……
Destroy(gameObject); // 销毁，还要等帧末，可能产生 GC
```

- `Instantiate` 和 `Destroy` 本身有开销；
- 频繁创建会产生托管堆垃圾，增加 GC 压力；
- 大量对象同时创建/销毁可能造成帧率波动；
- 重复加载预制体、重复 `GetComponent`、重复绑定事件都很浪费。

对象池的思路是：

> **对象不用了就失活，下次需要时直接拿出来复用，而不是销毁再创建。**

### 1.2 对象池的生命周期

```text
           Create（池子为空时）
                 │
                 ▼
        ┌─────────────────┐
        │   Pool（空闲）   │
        └─────────────────┘
           │           ▲
        Get│           │Release
           ▼           │
        ┌─────────────────┐
        │   Active（使用） │
        └─────────────────┘
                 │
                 │ Clear / Dispose
                 ▼
              Destroy
```

三个核心操作：

| 操作 | 作用 |
|---|---|
| `GetObject()` | 从池子取一个对象；池子空就创建 |
| `ReleaseObject()` | 把用完的对象放回池子 |
| `Clear()` / `Dispose()` | 销毁池子里的空闲对象，彻底清理 |

### 1.3 适合使用的场景

- 子弹、特效、飘字、掉落物
- 大量重复出现的小怪、障碍物
- UI 列表项、格子
- 任何“短暂使用、频繁出现”的同类对象

### 1.4 不适合使用的场景

- 只创建一次、一直存在的对象（没必要池化）
- 每个对象差异很大、无法统一重置的对象
- 对象占用内存很大，池子缓存太多反而浪费
- 生命周期很长、几乎不重复使用的对象

### 1.5 对象池的关键问题

设计对象池时，必须回答三个问题：

1. **对象从哪来？**  
   → `createFunc` / `IniCube`

2. **取出和放回时怎么重置状态？**  
   → `actionOnGet` / `actionOnRelease`

3. **什么时候真正销毁？**  
   → `actionOnDestroy` / `Clear` / `Dispose`

---

## 2. 核心代码解析

### 2.1 当前 `MyObjectPool<T>`

```csharp
using System;
using System.Collections.Generic;

public class MyObjectPool<T> : IDisposable where T : class
{
    private readonly Func<T> funcOnIni;
    private readonly Action<T> actionOnGet, actionOnRelease, actionOnDestroy;
    private readonly Stack<T> pool;

    public MyObjectPool(
        Func<T> funcOnIni,
        Action<T> actionOnGet,
        Action<T> actionOnRelease,
        Action<T> actionOnDestroy)
    {
        this.funcOnIni = funcOnIni;
        this.actionOnGet = actionOnGet;
        this.actionOnRelease = actionOnRelease;
        this.actionOnDestroy = actionOnDestroy;
        pool = new Stack<T>();
    }

    public T GetObject()
    {
        if (pool.Count == 0)
        {
            T newObject = funcOnIni?.Invoke();
            pool.Push(newObject);
        }

        T getObject = pool.Pop();
        actionOnGet?.Invoke(getObject);
        return getObject;
    }

    public void ReleaseObject(T releaseObject)
    {
        pool.Push(releaseObject);
        actionOnRelease?.Invoke(releaseObject);
    }

    public void Clear()
    {
        while (pool.Count > 0)
        {
            T item = pool.Pop();
            actionOnDestroy?.Invoke(item);
        }
    }

    public void Dispose()
    {
        Clear();
    }
}
```

### 2.2 字段解析

| 字段 | 作用 |
|---|---|
| `Func<T> funcOnIni` | 池子为空时创建新对象 |
| `Action<T> actionOnGet` | 取出对象后的回调：激活、重置位置等 |
| `Action<T> actionOnRelease` | 放回对象前的回调：停用、清理状态 |
| `Action<T> actionOnDestroy` | 真正销毁对象：`Destroy(obj)` |
| `Stack<T> pool` | 存放空闲对象的栈 |

`readonly` 表示这些字段只能在构造函数里赋值，之后不能重新指向别的委托或栈。它保护的是**引用**，不是对象内容：

```csharp
private readonly Stack<T> pool;

pool = new Stack<T>(); // 编译错误
pool.Push(item);       // 可以，修改的是栈的内容
```

### 2.3 `GetObject()` 解析

```csharp
public T GetObject()
{
    if (pool.Count == 0)
    {
        T newObject = funcOnIni?.Invoke();
        pool.Push(newObject);
    }

    T getObject = pool.Pop();
    actionOnGet?.Invoke(getObject);
    return getObject;
}
```

流程：

1. 池子空了 → 调用 `funcOnIni` 创建新对象；
2. 把新对象 `Push` 进池子；
3. 立刻 `Pop` 出来；
4. 调用 `actionOnGet`；
5. 返回对象。

当前写法的问题：

- 创建后 `Push` 再 `Pop`，绕了一圈；
- `funcOnIni` 可能为 `null`，会 `Push(null)`；
- `funcOnIni` 返回 `null` 时，也会把 `null` 放进池子；
- 没有统计“当前借出多少、池子里还有多少”。

### 2.4 `ReleaseObject()` 解析

```csharp
public void ReleaseObject(T releaseObject)
{
    pool.Push(releaseObject);
    actionOnRelease?.Invoke(releaseObject);
}
```

当前Release的逻辑是：

```text
Push 入池 → actionOnRelease
```

问题：如果 `actionOnRelease` 抛异常，对象已经进了池子，但状态可能没清理干净。下次 `GetObject` 可能拿到一个“没停用/没重置”的对象。

官方逻辑是：

```text
检查重复 → actionOnRelease → Push 入池
```
这样子能保证避免二次Release，坏处是时间复杂度会从O(1) 变成O(n)

写法：

```csharp
public void ReleaseObject(T releaseObject)
{
    if (collectionCheck && pool.Count > 0 && pool.Contains(releaseObject))
        throw new InvalidOperationException("对象被重复放回池子");

    actionOnRelease?.Invoke(releaseObject);
    pool.Push(releaseObject);
}
```

### 2.5 `Clear()` / `Dispose()` 解析

```csharp
public void Clear()
{
    while (pool.Count > 0)
    {
        T item = pool.Pop();
        actionOnDestroy?.Invoke(item);
    }
}

public void Dispose()
{
    Clear();
}
```

特点：

- 只销毁**池子里的空闲对象**；
- 已经借出去的对象不在 `Stack` 里，`Clear` 不会碰它们；
- 用 `while + Pop` 而不是 `foreach`，避免“遍历时修改集合”的异常；
- `actionOnDestroy` 为 `null` 时，只是把引用清掉，不会真正销毁 Unity 对象。

`Dispose()` 只是 `Clear()` 的别名，配合 `IDisposable` 使用。

### 2.6 `Main` 里的使用流程

```csharp
void Start()
{
    objectPool = new MyObjectPool<GameObject>(
        IniCube,
        GetCube,
        ReleaseCube,
        DestoryCube
    );
}

void Update()
{
    if (Keyboard.current != null &&
        Keyboard.current.spaceKey.wasPressedThisFrame)
    {
        objectPool.GetObject();
    }
}

public GameObject IniCube()
{
    GameObject prefab = Resources.Load<GameObject>("Cube");
    GameObject cubeObject = Instantiate(prefab);

    cubeObject.GetComponent<MyCube>()
        .releaseEvent
        .AddListener(() => objectPool.ReleaseObject(cubeObject));

    return cubeObject;
}

public void GetCube(GameObject cube)
{
    cube.transform.position = boinTrans.position;
    cube.SetActive(true);
}

public void ReleaseCube(GameObject cube)
{
    cube.SetActive(false);
}

public void DestoryCube(GameObject cube)
{
    if (cube != null)
        Destroy(cube);
}

void OnDestroy()
{
    objectPool?.Dispose();
}
```

完整流程：

```text
按下空格
→ GetObject()
→ 池子为空？
   ├─ 是：IniCube()
   │      → Resources.Load 预制体
   │      → Instantiate 克隆
   │      → 给克隆体的 releaseEvent 添加监听
   └─ 否：从 Stack 里 Pop 一个
→ GetCube()
   → 设置位置
   → SetActive(true)
→ 方块下落
→ MyCube.Update 检测到 y < 0
→ releaseEvent.Invoke()
→ ReleaseObject(cube)
→ actionOnRelease → SetActive(false)
→ Push 回池子
```

### 2.8 `MyCube` 的作用

```csharp
public class MyCube : MonoBehaviour
{
    public UnityEvent releaseEvent;

    void Update()
    {
        if (this.transform.position.y < 0)
        {
            releaseEvent?.Invoke();
        }
    }
}
```

它负责判断“方块掉出地面”，然后通知对象池回收。

当前写法有一个隐患：只要 `y < 0`，每帧都会 `Invoke()`。虽然 `ReleaseCube` 里 `SetActive(false)` 会让 `Update` 停止，但更稳妥的做法是加一个 `released` 标志：

```csharp
public class MyCube : MonoBehaviour
{
    public UnityEvent releaseEvent;
    private bool released;

    void Update()
    {
        if (released) return;

        if (transform.position.y < 0)
        {
            released = true;
            releaseEvent?.Invoke();
        }
    }

    public void ResetState()
    {
        released = false;
    }
}
```

### 2.9 当前版本评价

这个对象池实现了以下功能：

- 对象池核心逻辑 `Get / Release / Clear / Dispose`；
- `readonly` 注入回调，结构清晰；
- `Clear` 用 `while + Pop`，不会遍历时修改集合；

官方版本的变化：

- 重复释放检查；
- 添加 `maxSize`，池子可能无限增长；
- 添加数量统计；

---

## 3. C# 语法复习

### 3.1 泛型与 `where T : class`

```csharp
public class MyObjectPool<T> : IDisposable where T : class
```

- `T` 是类型参数，使用时才确定：`MyObjectPool<GameObject>`、`MyObjectPool<Bullet>`。
- `where T : class` 是泛型约束：`T` 必须是引用类型。
- 好处：
  - 可以写 `obj == null`；
  - 避免值类型装箱；
  - 明确表示池子存放的是对象引用。

### 3.2 `Func<T>` 和 `Action<T>`

| 委托 | 返回值 | 用途 |
|---|---|---|
| `Func<T>` | 返回 `T` | 创建对象 |
| `Action<T>` | 无返回值 | 取出、放回、销毁时的回调 |

```csharp
Func<GameObject> create = () => Instantiate(prefab);
Action<GameObject> release = cube => cube.SetActive(false);
```

`?.Invoke()` 是空条件调用：

```csharp
actionOnRelease?.Invoke(obj);
```

等价于：

```csharp
if (actionOnRelease != null)
    actionOnRelease(obj);
```

### 3.3 Lambda 与闭包

```csharp
cubeObject.GetComponent<MyCube>()
    .releaseEvent
    .AddListener(() => objectPool.ReleaseObject(cubeObject));
```

这里的 lambda 捕获了外部的 `cubeObject` 变量，这叫**闭包**。

关键点：

- 每个 `IniCube()` 调用都会创建自己的 `cubeObject`，所以每个克隆体的 listener 捕获的是自己的实例；
- 如果在 `for` 循环里直接捕获循环变量，可能所有 lambda 都指向最后一个值；
- 解决方法是循环内用局部变量：
  ```csharp
  for (int i = 0; i < 10; i++)
  {
      GameObject cube = Instantiate(prefab);
      cube.GetComponent<MyCube>().releaseEvent.AddListener(
          () => objectPool.ReleaseObject(cube)
      );
  }
  ```

### 3.4 `event` 和 `readonly` 委托字段

下面写法是**错误**的：

```csharp
private readonly event Func<T> funcOnIni; // 编译错误
```

原因：

- `readonly` 只能修饰字段；
- `event` 不是普通字段，它是一对 `add/remove` 访问器加一个委托；
- `event` 的合法修饰符里没有 `readonly`。

如果真的需要event修改委托就不要用readonly

### 3.5 `UnityEvent` 的持久监听 vs 运行时监听

`UnityEvent.AddListener()` 添加的是**运行时监听**：

```csharp
releaseEvent.AddListener(() => objectPool.ReleaseObject(cube));
```

它有几个特点：

- 只存在于当前内存中的对象上；
- 不会被序列化进预制体；
- `Instantiate` 不会复制它；
- 每次 `AddListener` 都会增加一个回调，重复添加会叠加。

预制体在 Inspector 里配置的 UnityEvent 监听是**持久监听**：

- 会被序列化；
- `Instantiate` 会复制；
- 保存的是“目标对象 + 方法名 + 参数”，不是 lambda。

所以下面这段代码是错的：

```csharp
GameObject prefab = Resources.Load<GameObject>("Cube");
prefab.GetComponent<MyCube>().releaseEvent.AddListener(...); // 加到预制体资源上
return Instantiate(prefab); // 克隆体不会继承这个运行时监听
```

正确顺序是：

```csharp
GameObject prefab = Resources.Load<GameObject>("Cube");
GameObject cube = Instantiate(prefab); // 先实例化
cube.GetComponent<MyCube>()
    .releaseEvent
    .AddListener(() => objectPool.ReleaseObject(cube)); // 再加到实例上
```

### 3.6 `Resources.Load` 和 `Instantiate` 的区别

```csharp
GameObject prefab = Resources.Load<GameObject>("Cube");
```

返回的是 **Project 里的预制体资源**，不是场景中的对象。

```csharp
GameObject cube = Instantiate(prefab);
```

才是创建一个场景中的克隆体。

### 3.7 `IDisposable` 和 `using`

```csharp
public class MyObjectPool<T> : IDisposable
{
    public void Dispose()
    {
        Clear();
    }
}
```

`IDisposable` 只有一个方法：

```csharp
void Dispose();
```

配合 `using`：

```csharp
using (var pool = new MyObjectPool<GameObject>(...))
{
    var cube = pool.GetObject();
}
// 离开 using 时自动调用 pool.Dispose()
```

注意：

- `Dispose()` **不会自动调用**；
- 对单例来说，没有天然的 `using` 作用域，必须有人在退出时调用；
- `MonoBehaviour` 通常用 `OnDestroy()` / `OnApplicationQuit()`；
- `Dispose()` 要幂等，重复调用不能报错；

### 3.8 `Stack<T>` 和 `List<T>`

| 操作 | `Stack<T>` | `List<T>` 当栈用 |
|---|---|---|
| 入栈 | `Push` | `Add` |
| 出栈 | `Pop` | `RemoveAt(Count - 1)` |
| 看栈顶 | `Peek` | `list[Count - 1]` |
| 按下标访问 | 不支持 | 支持 |
| 删除任意元素 | 不支持 | `Remove` / `RemoveAt` |
| 遍历 | 支持 | 支持 |
| 尾部增删 | O(1) | O(1) |

Unity 官方用 `List<T>` + `m_FreshlyReleased` 缓存，是因为它还需要：

- 遍历检查重复释放；
- 给编辑器工具直接访问；
- 更灵活地删除/索引。

### 3.9 `Destroy` 和 `SetActive(false)`

对象池里通常：

```csharp
actionOnRelease: cube => cube.SetActive(false);
actionOnDestroy: cube => Destroy(cube);
```

区别：

- `SetActive(false)`：对象还在，只是隐藏/停用，可以再次复用；
- `Destroy(cube)`：真正销毁，之后不能再用。

### 3.10 接口补充：`IDisposable`、`IObjectPool<T>`

- `IDisposable`：清理/释放，支持 `using`。
- `IObjectPool<T>`：Unity 公开的泛型池接口，包含 `Get`、`Release`、`Get(out)`、`Clear`、`CountInactive`。

自己写池子时，实现 `IDisposable` 就够了；想和 Unity 生态兼容，可以再实现 `IObjectPool<T>`。

---

## 4. 额外改进

### 4.1 修正 `Release` 顺序

可以修改Release的顺序使其更符合逻辑

```text
检查重复 → actionOnRelease → Push
```

而不是：

```text
Push → actionOnRelease
```

这样如果回调抛异常，对象不会以“没清理干净”的状态留在池子里。

### 4.2 加重复释放检查

同一个对象被 `Release` 两次，会导致池子里出现两个相同引用，之后可能同时借给两个地方。

```csharp
private readonly bool collectionCheck;

public void ReleaseObject(T obj)
{
    if (collectionCheck && pool.Count > 0 && pool.Contains(obj))
    {
        throw new InvalidOperationException(
            "对象已经被重复放回池子。");
    }

    actionOnRelease?.Invoke(obj);
    pool.Push(obj);
}
```

`Stack.Contains` 是 O(n)，池子很大时可以考虑关闭检查或换 `HashSet`。

### 4.3 加 `maxSize`

池子不能无限增长。峰值创建了 1000 个对象，之后即使不用，也会一直占内存。

```csharp
private readonly int maxSize;

// Release 时
if (pool.Count < maxSize)
{
    pool.Push(obj);
}
else
{
    CountAll--;
    actionOnDestroy?.Invoke(obj);
}
```

### 4.4 加数量统计

```csharp
public int CountAll { get; private set; }        // 总创建数
public int CountInactive => pool.Count;          // 空闲数
public int CountActive => CountAll - CountInactive; // 借出数
```

这样在调试时会更方便：

```csharp
Debug.Log($"总:{pool.CountAll} 借出:{pool.CountActive} 空闲:{pool.CountInactive}");
```

### 4.5 参数判空

```csharp
this.createFunc = createFunc
    ?? throw new ArgumentNullException(nameof(createFunc));
```

创建结果也检查：

```csharp
T obj = createFunc();
if (obj == null)
    throw new InvalidOperationException("createFunc 返回了 null");
```

### 4.6 预热和初始容量

如果知道大概需要多少个对象，可以预先创建：

```csharp
public void Prewarm(int count)
{
    for (int i = 0; i < count; i++)
    {
        T obj = CreateNew();
        actionOnRelease?.Invoke(obj);
        pool.Push(obj);
    }
}
```

还可以给 `Stack<T>` 指定初始容量：

```csharp
pool = new Stack<T>(initialCapacity);
```

### 4.7 复用对象时重置状态

`GetCube` 现在只重置位置。如果方块有 `Rigidbody`，复用时最好重置速度和旋转：

```csharp
public void GetCube(GameObject cube)
{
    cube.transform.position = boinTrans.position;
    cube.transform.rotation = Quaternion.identity;

    Rigidbody rb = cube.GetComponent<Rigidbody>();
    if (rb != null)
    {
        rb.linearVelocity = Vector3.zero;  // Unity 6
        rb.angularVelocity = Vector3.zero;
    }

    cube.GetComponent<MyCube>().ResetState();
    cube.SetActive(true);
}
```

### 4.8 给 `MyCube` 加“只触发一次”标志

```csharp
public class MyCube : MonoBehaviour
{
    public UnityEvent releaseEvent;
    private bool released;

    void Update()
    {
        if (released) return;

        if (transform.position.y < 0)
        {
            released = true;
            releaseEvent?.Invoke();
        }
    }

    public void ResetState()
    {
        released = false;
    }
}
```

这样即使回收逻辑有延迟，也不会同一帧重复触发 `Release`。

### 4.9 缓存组件

每次 `GetCube` 都 `GetComponent<Rigidbody>()` 有一点开销。可以在初始化时缓存：

```csharp
private class PooledCube
{
    public GameObject GameObject;
    public MyCube MyCube;
    public Rigidbody Rigidbody;
}
```

或者用 `Dictionary<GameObject, Rigidbody>`。对象少的时候不必过度优化，知道有这回事即可。

### 4.10 可选：`m_FreshlyReleased`

官方的 `m_FreshlyReleased` 是微优化：

- 把最近释放的一个对象单独缓存；
- `Get` 时优先返回它；
- 省掉一次 `Add/RemoveAt` 或 `Push/Pop`。

### 4.11 生产环境直接用 Unity 内置池

Unity 已经提供了：

```csharp
using UnityEngine.Pool;

ObjectPool<GameObject> pool = new ObjectPool<GameObject>(
    createFunc: () => Instantiate(prefab),
    actionOnGet: cube => cube.SetActive(true),
    actionOnRelease: cube => cube.SetActive(false),
    actionOnDestroy: cube => Destroy(cube),
    collectionCheck: true,
    defaultCapacity: 10,
    maxSize: 100
);
```

自己写对象池主要是为了学习原理；实际项目优先用内置的 `ObjectPool<T>`

### 4.12 改进版完整代码

```csharp
using System;
using System.Collections.Generic;

public class MyObjectPool<T> : IDisposable where T : class
{
    private readonly Func<T> createFunc;
    private readonly Action<T> actionOnGet;
    private readonly Action<T> actionOnRelease;
    private readonly Action<T> actionOnDestroy;
    private readonly Stack<T> pool;
    private readonly bool collectionCheck;
    private readonly int maxSize;

    public int CountAll { get; private set; }
    public int CountInactive => pool.Count;
    public int CountActive => CountAll - CountInactive;

    public MyObjectPool(
        Func<T> createFunc,
        Action<T> actionOnGet = null,
        Action<T> actionOnRelease = null,
        Action<T> actionOnDestroy = null,
        bool collectionCheck = true,
        int initialCapacity = 10,
        int maxSize = 10000)
    {
        this.createFunc = createFunc
            ?? throw new ArgumentNullException(nameof(createFunc));

        if (maxSize <= 0)
            throw new ArgumentException("maxSize 必须大于 0", nameof(maxSize));

        this.actionOnGet = actionOnGet;
        this.actionOnRelease = actionOnRelease;
        this.actionOnDestroy = actionOnDestroy;
        this.collectionCheck = collectionCheck;
        this.maxSize = maxSize;

        pool = new Stack<T>(initialCapacity);
    }

    public T GetObject()
    {
        T obj;

        if (pool.Count > 0)
        {
            obj = pool.Pop();
        }
        else
        {
            obj = CreateNew();
        }

        actionOnGet?.Invoke(obj);
        return obj;
    }

    private T CreateNew()
    {
        T obj = createFunc();
        if (obj == null)
            throw new InvalidOperationException("createFunc 返回了 null");

        CountAll++;
        return obj;
    }

    public void ReleaseObject(T obj)
    {
        if (obj == null)
            throw new ArgumentNullException(nameof(obj));

        if (collectionCheck && pool.Count > 0 && pool.Contains(obj))
            throw new InvalidOperationException("对象已经被重复放回池子。");

        actionOnRelease?.Invoke(obj);

        if (CountInactive < maxSize)
        {
            pool.Push(obj);
        }
        else
        {
            CountAll--;
            actionOnDestroy?.Invoke(obj);
        }
    }

    public void Prewarm(int count)
    {
        count = Math.Min(count, maxSize);

        for (int i = 0; i < count; i++)
        {
            T obj = CreateNew();
            actionOnRelease?.Invoke(obj);
            pool.Push(obj);
        }
    }

    public void Clear()
    {
        int idleCount = pool.Count;

        while (pool.Count > 0)
        {
            T obj = pool.Pop();
            actionOnDestroy?.Invoke(obj);
        }

        CountAll -= idleCount;
    }

    public void Dispose()
    {
        Clear();
    }
}
```

> `Clear` 只销毁空闲对象；如果还有对象借出，`CountAll` 只减去空闲数量，借出数量仍然保留。
>
> 如果希望 `Clear` 时连借出的对象也一起处理，需要额外维护“活跃对象列表”，这会增加复杂度；官方池也没有销毁借出对象。
>
> 另外，只应该 `Release` 由这个池子创建的对象。把外部对象放进来会让 `CountAll / CountActive` 的统计失真。

