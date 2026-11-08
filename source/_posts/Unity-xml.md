---
title: "Unity xml"
date: 2026-11-04 18:19:53
categories:
  - "Unity"
tags:
  - "XMind转换"
  - "Unity"
  - "Data"
---

> 这篇「Unity xml」笔记是过去思维导图笔记的ai转换版。

## 1. 基本格式

这一节先整理基本格式。

### 1.1 注释

- &lt;!--<br>这是注释<br>可以有多行<br>--&gt;

### 1.2 固定内容

示例代码如下：

```xml
<!--固定必写内容,
version代表版本，encoding代表编码格式-->
<?xml version="1.0" encoding="UTF-8"?>
```

### 1.3 基本语法

示例代码如下：

```xml
<!--xml基本语法就是 <元素标签></元素标签>配对-->
```

```xml
<playerInfo>
	<name> illu </name>
	<age> 20 </age>
	<list>
		<item>
			<id>1</id>
			<num>10</num>
		</item>
		<item>
			<id>2</id>
			<num>14</num>
		</item>
	</list>
</playerInfo>
```

- tab进位表示嵌套
- 必须有一个根节点

### 1.4 基本规则

主要包括：

- 每个标签必须有对应关闭标签
- 命名规则要遵照变量命名规则
- 必须有根元素
- XML标签对大小写敏感
- **特殊符号用实体引用**
  - &amp;lt 对应 &lt;
  - &amp;gt 对应 &gt;
  - &amp;amp 对应 &amp;
  - &amp;apos 对应 '
  - &amp;quot 对应 "

## 2. XML属性

接下来整理XML属性。

- **为了让一个节点包含多个信息而不嵌套**

示例代码如下：

```xml
<!--属性就是在元素标签后面加空格 添加的内容-->
<!--属性必须有引号包裹单引号双引号都行-->
<playerInfo name="illu" age="20">
12345
</playerInfo>
```

```xml
<!--如果不想要元素信息可以-->
<friend name="张三" age="20"/>
```

- **属性和节点没啥区别**

## 3. C#存取XML

再整理C#存取XML。

### 3.1 存放位置

- 只读不写可放在Resources或StreamingAssests文件夹（自己创）
- 动态存取要放在Application.persistentDataPath

### 3.2 读取xml

- 1.XmlDocument<br>2.XmlTextReader 只读不写，不常用<br>3.Linq
- 使用xmlDocument需引用System.Xml

示例代码如下：

```csharp
XmlDocument xmlDoc = new XmlDocument();
TextAsset textAsset = Resources.Load<TextAsset>("Resources中的文件名");
xmlDoc.LoadXml(textAsset.text);
通过上面三行代码读取xml文件
```

```csharp
xmlDoc.Load(Application.streamingAssetsPath + "/testxml.xml");
通过StreamAssetsPath路径直接加载
```

### 3.3 信息读取

- xml文件已经被读取到xmlDoc

示例代码如下：

```csharp
//先得到根节点信息
XmlNode node = xmlDoc.SelectSinglrNode("根节点名字");
//再根据根节点往下找节点信息，信息需要用.InnerText点出
        XmlNode name = node.SelectSingleNode("name");
        print(name.InnerText);
```

```csharp
得到节点的属性
XmlNode weapon = node.SelectSingleNode("weapon");
print(weapon.Attributes["属性名"].Value);
```

- XmlNodeList nodeList = node.SelectNodes("friend"); //获取多个同名节点
```csharp
//foreach遍历多节点，内部再用SelectSingleNode读取子节点
foreach (XmlNode item in nodeList)
        {
            XmlNode nameF = item.SelectSingleNode("name");
            XmlNode atkF = item.SelectSingleNode("atk");
            print(nameF.InnerText);
            print(atkF.InnerText);
        }
```

```csharp
//for遍历
        for(int i = 0; i < nodeList.Count; i++)
        {
            XmlNode nameF = nodeList[i].SelectSingleNode("name");
            XmlNode atkF = nodeList[i].SelectSingleNode("atk");
            print(nameF.InnerText);
            print(atkF.InnerText);
        }
```

### 3.4 信息存储

- 存在Application.persistentDataPath(可读可写)
- 关键类<br>XmlDocument用于创建节点 存储文件<br>XmlDeclaration 用于添加版本信息<br>XmlElement 节点类

示例代码如下：

```csharp
1.创建文本对象
XmlDocument xmlDoc = new XmlDocument();
2.添加固定版本信息
XmlDeclaration xmlDeclaration = xmlDoc.CreateXmlDeclaration("1.0", "UTF-8", null);
xmlDoc.AppendChild(xmlDeclaration);
3.添加根节点
XmlElement root = xmlDoc.CreateElement("PlayerInfo");
xmlDoc.AppendChild(root);
```

```csharp
4.添加子节点
XmlElement name = xmlDoc.CreateElement("name");
name.InnerText = "张三";
//加到root根节点加内容
root.AppendChild(name);
```

```csharp
5.嵌套添加节点
XmlElement Listint = xmlDoc.CreateElement("Listint");
for (int i = 0; i < 5; i++)
{
      XmlElement intNode = xmlDoc.CreateElement("int");
      intNode.InnerText = i.ToString();
      Listint.AppendChild(intNode);
}
root.AppendChild(Listint);
```

```csharp
6.添加有属性的节点
XmlElement friend = xmlDoc.CreateElement("friend");
friend.SetAttribute("id", "1");
friend.SetAttribute("name", "李四");
root.AppendChild(friend);
```

```csharp
7.最重要，保存到指定路径
string path = Application.persistentDataPath + "/PlayInfo2.xml";
xmlDoc.Save(path);
```

### 3.5 修改XML

示例代码如下：

```csharp
先判断文件是否存在
引用System.IO
if(File.Exists(path))
{
      //内容写在这里
}
```

```csharp
if(File.Exists(path))
{
            //读取xml文件
            XmlDocument newXmlDoc = new XmlDocument();
            newXmlDoc.Load(path);
            //修改就是在原来基础上移除，添加
            //可以通过/来得到多重子节点
            XmlNode node = newXmlDoc.SelectSingleNode("PlayerInfo/name");
            //先得到父节点。用父节点的方法移除子节点
            XmlNode rootNode = newXmlDoc.SelectSingleNode("PlayerInfo");
            rootNode.RemoveChild(node);
            //新建一个相同节点
            XmlElement newName = newXmlDoc.CreateElement("name");
            newName.InnerText = "王五";
            rootNode.AppendChild(newName);
            newXmlDoc.Save(path);
}
```

## 4. XML实践相关

接着整理XML实践相关。

### 4.1 C#中XML序列化

- **什么是序列化和反序列化**
  - 序列化：把对象转化为字节序列过程为序列化
  - 反序列化：把字节序列转为对象的过程
- **序列化步骤**
  - 先准备一个能new的数据结构类
  - XmlSerializer 用于序列化xml的关键类<br>StreamWriter 用于存储文件<br>using 方便流对象释放和销毁

  示例代码如下：

  ```csharp
  //第二步：结合 using知识点 和 StreamWriter这个流对象 来写入文件
  // 括号内的代码：写入一个文件流 如果有该文件 直接打开并修改 如果没有该文件 直接新建一个文件
  // using 的新用法 括号当中包裹的声明的对象 会在 大括号语句块结束后 自动释放掉 
  // 当语句块结束 会自动帮助我们调用 对象的 Dispose这个方法 让其进行销毁
  // using一般都是配合 内存占用比较大 或者 有读写操作时  进行使用的 
  using ( StreamWriter stream = new StreamWriter(path) )
  {
       //第三步：进行xml文件序列化
       XmlSerializer s = new XmlSerializer(typeof(Lesson1Test));
       //这句代码的含义 就是通过序列化对象 对我们类对象进行翻译 将其翻译成我们的xml文件 写入到对应的文件中
       //第一个参数 ： 文件流对象
       //第二个参数: 想要备翻译 的对象
       //注意 ：翻译机器的类型 一定要和传入的对象是一致的 不然会报错
       s.Serialize(stream, lt);
  }
  ```

  - 序列化不支持字典，并且只能读public
  - \[XmlAttribute("new name")\]特性能把这种对象由节点变成属性,括号内表示属性名，不写括号表示不用换名字<br>\[XmlElement("testPublic123123")\]特性表示改变元素的名字<br>\[XmlArray("name")\]特性能改数组，list中节点的名字
- **反序列化**
  - **判断文件存在**
    - if(File.Exists(path))
  - 使用using和StreamReader<br>xmlSerializer的Deserialize
  ```csharp
  using(StremReader reader = new StreamReader(path))
  {
  	XmlSerializer s = new XmlSerializer(typeof(类名))；
  	类名 l = s.Deserialize(reader) as 类名；
  }
  ```

  - 特别注意，如果是List数组，反序列化会往数组内加节点，而不是覆盖原List
- 被序列化的类对象必须有无参构造

### 4.2 Ixmlserializable接口

- 为了让Dictionary支持序列化

示例代码如下：

```csharp
作用是可拓展XmlSerializer
 需使用using System.Xml.Serialization;
```

```csharp
需实现3个接口
//第一个接口返回结构，默认为空就行
public XmlSchema GetSchema()
{
    return null;
}
//反序列化时自动调用的方法
public void ReadXml(XmlReader reader)
{
    //在里面自定义反序列化规则
    this.name = reader["name"];
    this.age = int.Parse(reader["age"]);
    //写节点
     while(reader.Read())
        {
            if(reader.NodeType == XmlNodeType.Element)
            {
                switch(reader.Name)
                {
                    case "name":
                        reader.Read();
                        this.name = reader.Value;
                        break;
                    case "age":
                        reader.Read();
                        this.age = int.Parse(reader.Value);
                        break;
                }
            }
        }
}
//序列化时自动调用的方法
public void WriteXml(XmlWriter writer)
{
   //在里面自定义序列化规则
   writer.WriteAttributeString("name",this.name);
   writer.WriteAttributeString("age",this.age.ToString());
	//第二种写节点形式·
    writer.WriteElementString("name",this.name);
    writer.WriteElementString("age",this.age.ToString());
}
```

- **用writer写属性**
  - writer.WriteAttributeString("属性名",需写入的值，必须是string);
- **用writer写节点**
  - writer.WriteElementString("属性名",需写入的值，必须是string);
- 用reader读取属性
  ```csharp
  this.属性 = reader["属性名"];
  //返回值是string，需做对应转换
  ```

- **用reaader写节点**
  - 用reader.read()往下找节点，第一次访问节点头，接着访问节点值，接着访问·节点尾，接着是下一个节点头
- 用writer写包裹节点
  ```csharp
  //写包裹节点
          XmlSerializer s = new XmlSerializer(typeof(string));
          writer.WriteStartElement("name");
          s.Serialize(writer,this.name);
          writer.WriteEndElement();

          XmlSerializer s1 = new XmlSerializer(typeof(int));
          writer.WriteStartElement("age");
          s1.Serialize(writer,this.age);
          writer.WriteEndElement();
  ```

- 用reader读包裹节点
  ```csharp
  XmlSerializer s = new XmlSerializer(typeof(string));
          reader.Read();
          reader.ReadStartElement("name");
          this.name = s.Deserialize(reader) as string;
          reader.ReadEndElement();
          XmlSerializer s1 = new XmlSerializer(typeof(int));
          reader.Read();
          reader.ReadStartElement("age");
          this.age = (int)s1.Deserialize(reader);
          reader.ReadEndElement();
  ```

### 4.3 Dictionary无法序列化

- 我们可以自己写一个类，让他继承Dictionary，内部实现序列化
- 通过序列化的方法来写属性，用Dictionary举例

  示例代码如下：

  ```csharp
  public void ReadXml(XmlReader reader)
      {
          XmlSerializer sKey = new XmlSerializer(typeof(TKey));
          XmlSerializer sValue = new XmlSerializer(typeof(TValue));
          reader.Read();
          while(reader.NodeType != XmlNodeType.EndElement)
          {
              TKey key = (TKey)sKey.Deserialize(reader);
              TValue value = (TValue)sValue.Deserialize(reader);
              this.Add(key,value);
          }
          reader.Read();//防止影响之后的读取
      }

      public void WriteXml(XmlWriter writer)
      {
          XmlSerializer sKey = new XmlSerializer(typeof(TKey));
          XmlSerializer sValue = new XmlSerializer(typeof(TValue));
          foreach(KeyValuePair<TKey,TValue> item in this)
          {   
              sKey.Serialize(writer,item.Key);
              sValue.Serialize(writer,item.Value);
          }

      }
  ```

## 5. 查错

最后整理查错。

- **https://www.runoob.com/**
