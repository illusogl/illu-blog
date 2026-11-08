# C#进阶

## 简单数据结构类

### Arraylist

- 本质
  - object类型的数组
  - C#封装好的数组
  - 能够像数组增删查改
```csharp
ArrayList array = new ArrayList( );
需要引用命名空间System.Collections
```

- 增删查改
  - 增
    - array.Add( );里面可以存任意类型
    - array.AddRange( /\*ArrayList型\*/);增加一个范围
    - array.Insert(1 , 1233);再第一个位置插入值，后面的值全部后移
  - 删
    - array.Remove(1); 移除数组中指定元素，移除1
    - array.RemoveAt(1); 移除数组中指定位置元素；移除第2个
    - array.Clear( );清空
  - 查
    - array.Contains(/\*值\*/ );返回值为bool型，如果array中有元素，这返回true
    - int index =array.IndexOf( /\*值\*/)；正向寻找第一个遇见值的所在位置，返回位置，没有则是-1
    - int index =array.LastIndexOf( /\*值\*/)；反向寻找第一个遇见值的所在位置，返回位置，没有则是-1
    - array\[0\];直接访问所在位置
  - 改
    - array\[index\] = 'a';改第index位置的值
- 遍历
  - for循环 查找
  - 长度array.Count<br>容量array.Capacity
  - 迭代器遍历<br>foreach（object item in array）<br>{<br>Console.WriteLine(item);<br>}
    - 把array的值放到item中
- 装箱拆箱
  - 作为万物之父，可以把任意类型转为object 并用as转回去
- 相较于数组的优点，自动扩容，记录不定长度数组方便

### stack(栈)

- C#封装好的类，本质是object数组<br>\*\*\*栈是先进后出的
- 声明
  - 引用命名空间System.Collectins
  - Stack stack = new Stack( );
- 增删查改
  - 增
    - 压栈
    - stack.Push("2331");
  - 取
    - 栈中不能删除，只有取的概念，先进后出
    - 弹栈:将最上面的东西弹出
    - object v = stack.Pop( );
  - 查
    - 栈无法查看指定元素，只能看栈顶内容
    - v = stack.Peek( );
    - 只查不弹
    - contain
      - 查找是不是有123
      - stack.Contain(123);
      - 返回bool
  - 改
    - 无法单独修改,只能清除
    - stack.Clear( );
- 遍历
  - stack.Count得到长度
  - 用foreach遍历（没有索引器，不能查找特定位置值）
    ```csharp
    foreach(object item in stack)
    {
    	Console.WriteLine(item);
    }
    ```

    - 遍历的数据从栈顶到栈底，1，2，3插入。输出3，2，1
  - 转换为object数组,来遍历
    ```csharp
    object [ ]array = stack.ToArray( ); 
    再遍历数组
    ```

    - 遍历的结果也是从栈顶到栈底
  - 循环弹栈
    ```csharp
    while（stack.Count>0）
    {
    	object o = stack.Pop( );
    	Console.WriteLine(o);
    }
    ```

- 用法：UI面板，二进制计算

### Queue（队列）

- C#封装好的类，本质是object数组<br>\*\*\*队列是先进先出的
- 声明
  - 引用命名空间System.Collectins
  - Queue queue = new Queue( );
- 增取查改
  - 增
    - quene.Enqueue("23r");
  - 取
    - 取出先加入的对象
    - object v = quene.Deueue( );
  - 查
    - v = quene.Peek( );
    - 不拿出，只查看
    ```csharp
    queue.Contain(0);
    查找有没有整数0	返回bool值
    ```

  - 改
    - quene.Clear( );
- 遍历
  - queue.Count得到长度
  - 用foreach遍历（没有索引器，不能查找特定位置值）
    ```csharp
    foreach(object item in queue)
    {
    	Console.WriteLine(item);
    }
    ```

    - 遍历的数据按进入顺序，1，2，3插入。输出1,2,3
  - 转换为object数组,来遍历
    ```csharp
    object [ ]array = queue.ToArray( ); 
    再遍历数组
    ```

  - 循环弹栈
    ```csharp
    while（queue.Count>0）
    {
    	object o = queue.Pop( );
    	Console.WriteLine(o);
    }
    ```

### Hashtable(哈希表)

- 基于哈希代码组织起来的键值对；一个键对应一个值<br>通过键找值
- 声明
  - 引用命名空间System.Collectins
  - Hashtable hash = new Hashtable( );
- 增删查改
  - 增
    - hash.Add(1 ,"123");//不能有相同的键（前面的）
  - 删
    - 只能通过键删除
    - hash.Remove(1);
    - 删除不存在的键，不会有反应
    - hash.Clear( );
  - 查
    - 输入键，查看值
      ```csharp
      Console.Write(hash["123"]);
      ```

    - 查看键是否存在
      - hash.ContainsKey("2")<br>返回bool值
    - 查看值是否存在
      - hash.ContainsValue("2")<br>返回bool值
  - 改
    - 改只能改键对应的值内容<br>不能改键
    - hash\[2\] = 100;
- 遍历
  - hash.Count 得到长度
  - 用foreach
  ```csharp
  foreach（object item in hash.Key）
  {
  	Console.WriteLine(item);//返回键
  	Console.WriteLine(hash[item]);//返回值
  }
  ```

  ```csharp
  foreach（object item in hash.Values）
  {
  	Console.WriteLine(item);
  	//返回值
  }
  ```

  - foreach（DictionaryEntry item in hash）<br>{<br>Console.WriteLine(item.Key);<br>Console.WriteLine(item.Value);<br>}
    - 结构体
  - 迭代器方法

## 泛型

### 泛型

- 类型占位符，用以实现同一份代码操作多种类型
- 分类
  - 泛型类
    - class 类名&lt;泛型占位字母&gt;//说是字母，实际可以写字符串
    - 类内部可以用占位字母代替变量类型
    - 加上泛型变成不同类，可以与普通类同名
  - 泛型接口
    - interface 类名&lt;泛型占位字母&gt;
  - 泛型函数
    - 函数名&lt;泛型占位字母&gt;(参数列表)
    - 函数中占位字母可用在参数列表，和返回值，逻辑处理中
    - 初始化泛型数据 T t = default(T);//得到默认值
  - 泛型占位字母可以有多个，用逗号隔开
- 泛型类，泛型接口使用
  - 在后面使用时<br>类名&lt;具体变量&gt; t = new 类名&lt;具体变量&gt; （）；
  - 将占位字母变成具体的变量类型
- 不同类型的对象用相同逻辑可以用泛型<br>使用泛型可以避免装箱拆箱

### 泛型约束

- 让泛型的类型有一定的限制
- 语法
  ```csharp
  值类型						where 泛型字母：struct 
  引用类型					where 泛型字母：class
  存在无参公共构造函数				where 泛型字母：new（）
  某个类本身或其派生类				where 泛型字母：类名
  某个接口本身或其派生类型			where 泛型字母：接口名
  另一个泛型类型本身或其派生类型	where 泛型字母：另一个泛型字母
  ```

  ```csharp
  实例： 1) 引用类型约束
  public class ReferenceCache<T> where T : class
  {
      public T Value { get; set; }
  }
  ```

- 约束的组合使用
  - 通过逗号，实现多个约束
- 多个泛型有约束
  - 加空格接着写

## 常用泛型数据结构类

### List

- 可变类型的泛型数组（ArrayList的泛型翻版）
- 申明
  - 引用命名空间System.Collections.Generic
  - List&lt;int&gt; list = new List&lt;int&gt;( );
- 增删查改
  - 增
    - list.Add(1);
    ```csharp
    list.AddRange(list2); 	加一个同类型List
    ```

  - 删
    - list.Remove(1);
      - 移除指定元素
    - list.RemoveAt(0);
      - 移除指定位置
    - list.Clear( );
      - 清空
  - 查
    ```csharp
    Console.WriteLine(list[0]);
    ```

    - list.Contain(1);
      - 查看是否存在，返回bool值
    - list.IndexOf(2);
      - 正向查找位置
    - list.LastIndexOf(3);
      - 反向查找位置
  - 改
    - list\[3\] = 23;
- 插入
  - list.Insert(0 , 231);
    - 在第0处插入231
- 遍历
  - 长度Count
  - 容量Capacity
  ```csharp
  for(int i = 0 ; i<list.Count;i++)
  {
  	Console.WriteLine(list[i]);
  }
  ```

  ```csharp
  foreach(int item in each)
  {
  	Console.WriteLine(item);
  }
  ```

### List排序

- List自带的排序方式
  - List名.Sort( )；
  - List名.Reverse( )；//反转
  - 用来排序数字等系统自带变量
- 自定义类的排序
  - 自定义类要加上排序的接口
    - IComparable&lt;类名&gt;
  - 接口的方法
    - 接口提供了一个CompareTo函数，当你调用Sort，调用函数
    - 中间逻辑自己写，传入参数为list中其他成员，返回值小于0放在传入值后面，大于0放在传入值前面
  - 通过委托方法排序
    - Sort中有重载依靠委托的函数，可传入函数进行比较
    - 函数规则
      ```csharp
      返回值int  参数：两个参数a，b
      内部逻辑自己写，返回值大于0，a放到b右边，返回值小于0，a放到b左边
      ```

### Dictionary

- 泛型翻版的Hashtable
- 申明
  - Dictionary&lt;int , string&gt; dictionary = new Dictionary&lt;int ,string&gt;( );
  - 键不能相同，值可以
  - 键和值可以是不同类型，上面键是int，值是string
  - 引用命名空间System.Collections.Generic
- 增删查改
  - 增
    - dictionary.Add(2,"333");
  - 删
    - dictionary.Remove(3);
    - 通过键删除，找不到就没反应
    - dictionary.Clear( );
  - 查
    - 通过键查看值，找不到不会返回空，会报错
      ```csharp
      Console.WriteLine(dictionary[0]);
      ```

    - 查看键是否存在
      - dictionary.ContainsKey(2)<br>返回bool值
    - 查看值是否存在
      - dictionary.ContainsValue("2")<br>返回bool值
  - 改
    - 改只能改键对应的值内容<br>不能改键
    - dictionary\[2\] = “100”;
- 遍历
  - dictionary.Count 得到长度
  - 用foreach
  ```csharp
  foreach（int item in hash.Key）
  {
  	Console.WriteLine(item);//返回键
  	Console.WriteLine(hash[item]);//返回值
  }
  ```

  ```csharp
  foreach（string item in hash.Values）
  {
  	Console.WriteLine(item);
  	//返回值
  }
  ```

  - foreach（KeyValuePair&lt;int,string&gt;item in hash）<br>{<br>Console.WriteLine(item.Key);<br>Console.WriteLine(item.Value);<br>}
    - 结构体
  - 迭代器方法

### 顺序存储和链式存储

- 顺序存储
  - 用连续地址的存储单元，存储线性表各个元素
- 链式存储
  - 单向链表，双向链表，循环链表
  - 用任意存储单元存储线性表中各个元素
- C#中实现链表
  - 节点
    ```csharp
    class LinkNode<T>
    {
    	public T data;
    	public LinkNode<T>nextNode;
    	public LinkNode(T value){data = value;}//初始化
    }
    ```

  - 类（管理节点）
    ```csharp
    class Linklist<T>
    {
    	public LinkNode<T> head ;
    	public LinkNode<T> last
    	public void Add(T data)
    	{
    		LinkNode<T> node = new LinkedNode<T>(value);
    		if(head == null){head = node;	last = node;}
    		else(last.nextNode = node ; 	last = node;)
    	}
    }
    ```

    ```csharp
    public void RemoveAt(T value)
    {
    	if(head == null){return;}
    	else if(head.value.Equals(value))
    	{
    		head= head.nextNode;
    		if(head == null){last = null;}
    		return;
    	}
    	LinkNode<T> node = head;
    	while(node.next !=null)
    	{
    		if(node.next.Equal(value)){node.next = node.next.next;break;}
    		node = node.next;
    	}
    }
    ```

- 链式存储易于增删，顺序存储易于查改

### LinkedList

- C#包装好的泛型双向链表
- 申明
  - 引用System.Collections.Generic
  - LinkedList&lt;string&gt; link = new LinkList&lt;string&gt;( );
  - LinkListNode 节点类
    - Next下一个
    - Previous上一个
    - Value数值
- 增删查改
  - 增
    - link.AddLast("ad");
      - 尾插法
    - link.AddFirst("das")；
      - 头插法
    - LinkListNode&lt;string&gt; node = LinkList.Find("s");
      - link.AddAfter(node , "ads");
        - 往节点后面插
      - link.AddBefore(node , "as");
        - 往节点前面插
  - 删
    - link.RemoveFirst( );
      - 移除头节点
    - link.RemoveLast( );
      - 移除尾节点
    - link.Remove("asd");
      - 移除指定节点
    - link.Clear( );
      - 清空
  - 查
    - LinkListNode&lt;string&gt; first = link.Frist;
      - 查头节点
    - LinkListNode&lt;string&gt; last = link.Last;
      - 查尾节点
    - 无法通过索引器找
      - LinkListNode&lt;string&gt; node = link.Find("asd");
        - 查找值，没有则返回空
    - 判断是否存在
      - link.Contains("ad");
      - 返回bool值
  - 改
    - 得到节点，改Vaule
- 遍历
  - foreach
    ```csharp
    foreach(string item in link)
    {
    	Console.WriteLine(item);
    }
    ```

  - 用节点遍历
    ```csharp
    LinkedListNode<string> nowNode = linkedList.Frist ;
    while(nowNode != null)
    {	Console.WriteLine(nowNode.Value);	
    	nowNode = nowNode.Next;
    }
    ```

### 泛型栈和队列

- Stack和Queue泛型翻版
- 申明
  - 引用System.Collections.Generic
  - Stack&lt;int&gt; stack = new Stack&lt;int&gt;( );
  - Queue&lt;int&gt; Queue = newQueue&lt;int&gt;( );

## 委托与事件

### 委托

- 表示函数的变量类型 本质是一个类
- 语法
  - 申明
    - 访问修饰符 delegate 返回值 委托名（参数列表）
    - 写在class或namespace中
    - 委托默认为public
    - 委托不能重载
  - 使用
    - 委托用来装函数，常用在作为类的成员，作为函数参数
    ```csharp
    委托名 变量名 = new 委托名（函数名）；|| 委托名 变量名 = 函数名；
    //函数的变量和返回值与委托要一样
    变量名.Invoke(参数/*如果要的话*/);	||	变量名（参数）；
    ```

    - 作为类的变量，可以将函数当变量传入
- 用委托传入多个函数
  - MyFun ff = Fun；<br>ff+=Fun2；<br>ff有Fun和Fun2两个函数<br>ff（）；//执行两个函数
  - 删
    - ff-=Fun2；
    - 多删不会报错，删空了执行会报错
- 系统定义好的委托
  - Action 无参无返回委托
  - Func&lt;变量类型&gt; 无参返回类型任意的委托
  - Action&lt;参数，参数……&gt; 无返回值有n个参数的委托（最多16个）
  - Func&lt;参数，参数……，参数&gt;有n个参数，一个返回值的委托，最后1个参数是返回值的
- 想要让有返回值的委托返回所有返回值
  - 通过foreach遍历遍历每一个函数单独执行单独获取
  - foreach（Func&lt;string&gt; del in fun.GetInvocationList( )）
  - GetInvocationList( )可以返回委托中函数数组

### 事件

- 基于委托的存在，委托的安全包裹
- 申明
  ```csharp
  访问修饰符 event 委托类型 事件名；
  public event Action myEvent;
  public event Action<int,string> myEvent;
  ```

  - 作为成员变量存于类中，委托怎么用事件就怎么用<br>事件不能在类外部赋值，调用，只能在类和接口，结构体中
- 用法
  - 与委托一样
  - 但是事件不能在类外部置空和赋值，可以在类外部加减<br>事件不能在外部调用
  - 只能作为成员，不能随意申明

### 匿名函数

- 无名字的函数，只能配合委托和事件使用
- 申明
  ```csharp
  delegate(参数列表)
  {
  	//函数逻辑
  }
  ```

- 使用
  ```csharp
  Action a delegate（）
  {
  	//函数逻辑
  } ；
  ```

  - 调用即调用委托
  - 有返回值是直接return就行
- 缺点
  - 添加到委托或事件中，无法单独移除

### Lambad表达式

- 匿名函数的简写，用法与匿名函数相似
- 语法
  - （参数列表）=&gt;{//函数体}
- 闭包
  - 内层函数可以使用外层函数的变量，即使外层函数执行已经终止
  - 这种变量不能实时传入值，只能得到变量最终值<br>即执行内部函数时，得到的值是父函数的最终值（执行完外部函数的值）

## 反射与特性

### 反射

- 程序集
  - 一个代码集合	代码库dll	可执行文件exe
- 元数据
  - 描述数据的数据
- 反射
  - 程序运行时，程序查看其他程序或自己的元数据叫做反射
  - 得到所有元数据和其特性
  - 程序运行时，实例化对象，操作对象
  - 创建新对象，用这些对象执行任务
- 语法
  - Type（类的信息类）
    - 获取Type
      ```csharp
      int a = 10；
      Type t = a.GetType( );
      ```

      - Type t = typeof(int);
      ```csharp
      Type t = Type.GetType("System.Int32");	要写命名空间
      ```

    - 获取类的程序集信息（不重要）
      - t.Assembly
    - 获取类中所有公共资源
      - 引用命名空间System.Reflection
      - MemberInfo\[ \] infos = t.GetMembers( );
      - ctor-&gt;构造函数
    - 获取公共构造函数并调用
      - 得到所有
        - ConstructorInfo\[ \] ctors = t.GetConstructors( );
      - 得到无参构造
        - ConstructorInfo ctor = t.GetConstructor(new Type\[0\] );
        - 内部type数组时构造函数按顺序需要的参数类型
        - 执行无参构造
          - 类名 名字 = ctor.Invoke(null) as 类名
      - 得到有参构造
        ```csharp
        ConstructorInfo ctor = t.GetConstructor(new Type[ ] { typeof（int）} );
        ```

        - 执行有参构造
          - 类名 名字 = ctor.Invoke(new object\[ \] { 2 } ) as 类名
    - 获取类中公共成员变量
      - FieldInfo\[ \] infos = t.GetFields( );
      - 获取指定名称变量
        - FieldInfo info = t.GetField(“变量名”);
      - 通过反射得到和设置
        - info.GetValue(类对象)
        - info.SetValue(类对象，值)
    - 获取公共方法
      - Methodinfo\[ \] method = t.GetMethods( );
      - 得到指定方法
        ```csharp
        Methodinfo method = t.GetMethod("方法名" , new Type[ ]{ typeof(int) });
        前面写方法名，后面填的是传入的参数类型//应对重载
        ```

      - 调用该方法
        - method.Invoke(执行方法的对象 ， object形式的参数)；
        - 执行方法的对象：可以是新建类的对象，如果是静态方法，传入null
        - 传两个参数：new object\[ \]{ 3 ,5 }
    - 得事件，得接口，得枚举，得属性
  - Activator（快速实例化）
    - 将Type型的数据快速实例化对象<br>实例化结果为object
    - 无参构造
      ```csharp
      Type t = typeof（Test）;
      Test test = Activator.CreateInstance(t) as Test
      ```

    - 有参构造
      ```csharp
      Type t = typeof（Test）;
      Test test = Activator.CreateInstance(t ， 参数列表) as Test
      ```

      - 参数与构造函数对应，否则报错
  - Assembly（程序集类，得到别的程序集dll）
    - 只有先调用程序集，才能为其他文件夹文件调用Type
    - 加载同一文件夹其他程序集
      - Assembly a = Assembly.Load("程序集名称")；
    - 加载不在同一文件夹下程序集
      - Assembly a = Assembly.LoadFrom("包含程序集清单的文件名称或路径")
      - Assembly a = Assembly.LoadFile("加载文件的完全限定路径")
      - 写文件路径前面加@来取消转义字符
    - Type t = a.GetType(类对象)
- 类库文件的创建
  - 纯写代码，无法运行的程序集，通过反射调用
  - 写完完记得生成

### 特性

- 是什么
  - 是一个类，可以为元数据添加额外信息，用反射获取
  - 例如为类，结构体，加一些属性
- 自定义特性
  - 让一个类继承Attribute
  - class MyAttribute : Attribute
- 特性申明
  - \[特姓名（参数列表）\] 名字里写最后的Attribute会省略
  - 参数列表用以特性的构造函数使用
  - 写在类，函数，变量，成员属性，函数参数前面
- 特性使用
  - 用Type装元素
  - 判断是否用特性
    - type.IsDefine(typeof(MyCustomAttribute) , false)<br>返回bool值	false表示只找自己本体的，不找父类<br>参数1：特性名（类型）	参数2：是否搜索继承链（属性事件忽略）
  - 反射得到特性
    ```csharp
    t.GetCustomAttributes(true);得所有
    t.GetCustomAttribute(特性的Type);得指定
    //true表示找自己以及自己父类，无法看内部
    ```

    - 找到特性后，可以将特性从object转成对应类去执行
- 限制自定义特性使用范围
  - 通过给特性加一个系统的特性来限制特性使用范围
  - \[AttributeUsage(AttributeTargets.Class | AttributeTargets.Struct , AllowMutiple = true , Inherity = true)\]<br>第一个：特性能用在哪（类和结构体）<br>第二个：是否允许多个特性用在同一个目标上（写多个特性）<br>第三个：是否能被派生类或重写继承
- 过时特性
  - Obsolete 提示用户使用的方法已经过时，建议用新方法，写在函数前
  ```csharp
  [Obsolete("调用时提示的内容"，bool)] //true的话使用报错，false使用警报
  public void Fun( ){	}
  ```

- 调用者信息特性
  - 写在函数参数前，用以返回默认值（没啥用）
  - 引用命名空间System.Runtime.CompilerServices
  - \[CallerFilePath\]哪个文件调用<br>\[CallerLineNumber\]哪一行调用<br>\[CallerMemberName\]哪个函数调用
  - 用在try catch中打印信息
- 条件编译特性
  - Conditional<br>与#define配合用,用在调试代码时有时想执行又时不想执行的代码上
  - 引用System. Diagnostics
  - \[Conditional("条件")\]<br>函数
    - 当你没有define条件时，不会执行函数
- 外部dkk包函数
  - 用来标记c和c++的dll包
  - 引用命名空间System.Runtime.InteropServices
  ```csharp
  [DllImport("Test.dll")] //（同一文件加下的dll包名字）或目录
  public static extern 返回类型 名字( 参数 )；
  //返回类型 名字 参数，都在dll包里面完全符合
  ```

## 其他

### 协变逆变

- 协变
  - 子类变父类<br>如string变object<br>正常的<br>用来修饰泛型字母是用out
- 逆变
  - 父类变子类<br>object变string<br>不和谐的<br>用来修饰泛型字母用in
- 只有泛型接口和泛型委托可使用
- 作用
  - 用out修饰的泛型只能作为返回值
  - 用in修饰的泛型只能作为参数
  - 让委托满足里氏替换原则

### 多线程

- 进程和线程
  - 进程——就是程序<br>线程——包含在进程中运作单位
- 多线程
  - 多个线程并行
- 语法
  - 需要引用命名空间System.Thread
  - 申明新线程
    - Thread t = new Thread（）；
    - 括号内填入函数，让线程执行这个函数
  - 启动线程
    - t.start( );
  - 设为后台线程
    - 后台线程：主线程一结束，后台线程会直接结束<br>防止主线程结束后程序不停下
    - t.IsBackground = True;
  - 关闭一个线程
    - 1. t = null;
    - 2. 给线程的死循环设置一个bool值
    - 3.t.Abort( );
      - 控制台会报错
  - 线程休眠
    - Thread.Sleep(1000);
      - 休眠1000毫秒
    - 在哪个线程写这个，休眠那个线程
  - 线程之间共享数据
    - 线程之间内存共享<br>多线程操作同一片区域会造成逻辑循序的差错
    - 加锁避免问题
      ```csharp
      lock（引用类型的对象a）
      {
      	//要执行的代码
      }
      ```

      - 会运行多个lock，每个lock会有相同对象a
      - 当执行一个lock时，lock中的对象a会被锁，其他用相同对象a的lock内程序无法执行

### 预处理器指令

- 指导编译器对编译开始进行处理
- 以#开头 如#region
- 常见预处理指令
  - 1定义
    - #define 定义一个符号
    - #undef 取消定义符号
  - 2.if
    - #if  符号<br>//代码<br>#endif
      - 如果程序有定义过符号，会执行内部代码
    - #elif
      - 写到#if和#endif里面相当于else if
    - #else
      - 写到#if和#endif里面相当于else
  - 3.
    - #warning 提示文本
      - 警告
    - #error 提示文本
      - 错误，禁止执行

### 迭代器

- 程序设计的设计模式，提供一个访问聚合对象各个元素且不暴露内部标识的方式
- 实现方法
  - 关键接口IEnumerator ， IEnumerable<br>命名空间System.Collections<br>自己定义一个值为-1的变量光标，一进MoveNext就++
  - IEnumerable
    - get方法
      - 继承了IEnumerator，调用Reset直接return this就行
  - IEnumerator
    - Current成员<br>MoveNext方法<br>ReSet方法（初始化）
    - MoveNext返回值可以是return 光标&lt;Length
    - Reset直接把光标变成-1就行
- foreach本质<br>获取in后面对象的IEnumertor（用get方法）<br>执行对象里MoveNext方法<br>只要返回值是true，得到Current给item
- yield return语法糖快速实现
  - 调用IEnumerable<br>命名空间System.Collections
  - 循环多次yield return 返回值
    ```csharp
    for（int i = 0 ; i<Length ; i++）
    {
    	yield return list[i]
    }
    ```

  - 编译器看到后自动帮我们写代码
  - yield return同样可以用于泛型类中

### 特殊语法

- var隐式类型
  - 表示任意变量类型
  - 不能表示类的成员，只能临时申明（函数）<br>必须初始化，初始化后类型确定无法更改
- 设置对象初始值
  ```csharp
  申明类时
  Text t = new Text（）{ t1 = 3 , t2 = "df"};
  ```

  ```csharp
  设置线性表时
  List<int> list = new List<int>{3,5,6};
  ```

  ```csharp
  字典
  Dictionary<int,string> d = new Dictionary<int,string>
  {
  {1,"345"},{4,"sad"}
  };
  ```

  - 语法糖
- 匿名类
  - var v = new {age = 10， money = 13}；
- 可空类型
  - 值类型不可为空
  - 申明时在值类型后面加？就能设置空了<br>int？ i = null；
  - i.HasValue<br>判断是否为空
  - 安全获取可空类型
    - i.GetValueOrDefault( );
    - 没有值返回默认值，或返回括号内的值（括号内的值是暂时的不会赋值）
  - 同样的，对于引用类型会报错的语句，如ToString，在变量后加？可以跳过报错
- 空合并
  - 左边值 ？？右边值<br>左边为空返回右边，否则返回左边
- 内插字符串
  ```csharp
  Console.Write($"你好 { i } ")
  ```

- 单句逻辑简略写法
  - 一句代码可以不加{ }
  ```csharp
  类中的属性,函数
  get => i;
  set =>  i = value;
  public void Add(int x, int y)=> x+y;
  public void Speak(string str) => Console.Write(str);
  ```

### 值和引用类型

- 判断
  - 进内部看是类还是结构体，来判断是值还是引用
- 变量生命周期
  - 栈上系统自动管理，堆上手动管理C#有GC
  - 如果想跳过回收可以把变量在更高层记录或静态记录
- 结构体的值和引用
  - 结构体的值存在栈中
  - 结构体中引用类型存在堆中，结构体用指针引用
- 类的之和引用
  - 值和引用都在堆中
  - 值类型存在堆房间中，引用在堆房间放地址，在堆的其他地方引用
- 数组与类一样
- 结构体继承接口
  - 用里氏替换用接口装结构体<br>会把值存入堆中

## 排序补充

### 插入

- 将数组分为排序区与未排序区，将未排序区元素插入排序区中，排序区向前移
- 步骤
  - 取出未排序区的元素，i=1循环
  - 取出排序区最后一个元素索引<br>取出未排序区第一个元素
  - 在排序区进行比较，移动位置，插入数字

### 希尔

- 插入升级版
- 把整个序列分成若干序列，分别进行插入，极限情况降低时间复杂度
- 步骤
  - 实现插入排序（插入排序步长默认为一）
  - 确定步长，一开始是数组长度/2，之后不断/2，最后到1
  - 执行插入排序

### 归并

- 递归加合并
- 递归不停分，分完在排序，排序结束往上走，边走边合并，走到头顶出结果
- 步骤
  - 1.基本排序函数
  - 2.递归平分数组（返回基本排序数组内部是自身函数）//函数会先执行括号内的函数

### 快速

- 选取基准，产生左右标识，左右比基准，满足则换位
- 步骤
  - 申明快速排序的数组，传入左右边界
  - 记录基准值，左右游标
  - 交换逻辑，左右游标相同会退出循环
  - 放置基准值
  - 递归继续
  - 结束条件

### 堆排序

- 构建二叉树，大堆顶调整，堆顶往后放，不停变堆顶
- 规则
  - 最大非叶子节点Length/2 - 1<br>父节点为i，左节点为2i+1，右节点为2i+2
- 步骤
  - 实现父节点和左右节点比较
  - 构建大堆顶
  - 重复构建大堆顶n次，每次将最大数放最后，不比最后的数
