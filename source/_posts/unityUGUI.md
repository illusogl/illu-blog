---
title: "Unity UGUI"
date: 2026-11-04 18:19:49
categories:
  - "Unity"
tags:
  - "XMind转换"
  - "UI"
  - "Unity"
---

> 这篇「Unity UGUI」笔记是过去思维导图笔记的ai转换版。

## 1. 基础知识

这一节先整理基础知识。

### 1.1 六大基础组件

主要包括：

- 直接在Hierarchy右键就能放UGUI
- **六大组件有**
  - **Canvas上的**
    - **Canvas**
      - 画布组件，用于渲染UI
    - **CanvasScaler**
      - 分辨率自适应的组件
    - **RectTransform**
      - 射线事件交互的组件
    - **GraphicRaycaster**
      - 控制UI位置和对其方式的
  - **EventStsem上的**
    - **EventSystem**
      - 玩家输入响应系统
    - **StandaloneInputMoudle**
      - 独立输入模块组件
- **Canvas**
  - 负责渲染自己的所有子对象
  - 场景中可以有多个Canvas对象管理不同渲染方式，通常只要一个就好
  - **Canvas的三种渲染方式RenderMode**
    - **ScreenSpace-overlay 屏幕空间，覆盖模式，UI始终在前**
      - Pixel Perfect无锯齿精确渲染（性能换效果）
      - SortOrder 排序层编号，多个Canvas时的渲染先后顺序
      - TargetDisplay目标设备
      - Additional Shader Channels决定着色器读取那些数据
    - ScreenSpace-Camera屏幕空间，摄像机模式，3D物体可以显示在UI之前
      - **RenderCamera用于渲染UI的摄像机（不太推荐用主摄像机）**
        - 选用哪个摄像机，这个摄像机的3D物体会在UI之前显示
        - 我们推荐新建一个摄像机渲染UI内容，对于显示UI的摄像机，我们可以在Canvas中放3D模型，这样就能把需要的模型放到UI前
      - planeDistance UI平面在摄像机前方的距离，类似z轴
      - SortingLayer 所在排序层
      - Order in Layer排序层序号
    - **WorldSpace 世界空间，3D模式**
      - 把UI当3D物体处理
- **CanvasScaler**
  - **必备知识**
    - 渲染模式overlay下 ：宽高 \* 缩放系数 = 屏幕分辨率<br>渲染模式camera下：宽高 = 屏幕分辨率

      如下图所示：

      ![](/img/xmind/unityUGUI/01.png)

    - 通过不同算法计算屏幕分辨率和参考分辨率得到缩放参考系数，用以影响UI大小
  - **Constant Pixel Size恒定像素模式**
    - Scale Factor缩放系数，按照这个系数缩放所有组件
    - ReferencePixelsPerUnit 单位参考像素，多少像素对应unity中1个单位
      - UI原始尺寸 = 图片像素/(Pixels Per Unit/Reference Pixels Per Unity)
      - 每次修改大小，需要点图片上的恢复原始大小Set Native Size
    - 这个模式不会根据屏幕自适应，很少使用
  - **Scale with Screen Size缩放模式**
    - ReferenceResolution参考分辨率（出图的标准分辨率），缩放和匹配模式会基于这个参数进行计算
    - **ScreenMatchMode匹配模式**
      - **Expand**
        - 水平或垂直扩展画布时，会根据宽高比变化来放大缩小画布，可能有黑边
        - 缩放系数 = min(屏幕宽/参考宽，屏幕高/参考高)<br>画布尺寸 = 屏幕尺寸 /缩放系数<br>尽可能缩小UI，扩大Canvas Size
      - **Shrink**
        - 水平或垂直裁剪画布时，会根据宽高比变化来放大缩小画布，可能有裁剪
        - 缩放系数 = max(屏幕宽/参考宽，屏幕高/参考高)<br>画布尺寸 = 屏幕尺寸 /缩放系数<br>尽可能放大UI，减小Canvas Size
      - **MatchWidthOrHeight**
        - 以宽高或二者均值来缩放画布、

        示例代码如下：

        ```csharp
        float logWidth = Math.log(屏幕宽/参考宽,2);
        float logHeight = Math.log(屏幕高/参考高,2);
        float logAve = Mathf.Lerp(logWidth,logHeight,m_matchWidthOrHeight);
        scaleFactor = Mathf.Pow(2,logAve);
        ```

        - 横屏模式值用1，竖屏模式用0
  - **Constant Physical Size恒定物理模式**
    - **dpi 每英寸长度像素点数**
      - 越高密度越大，效果越好
    - fallback screen dpi 备用dpi，当设备找不到dpi值用这个
    - default sprite dpi 默认图片dpi
    - 该模式与恒定像素类似，不会缩放，用处是在不同物理设备上改变像素多少，使之看起来大小相似
  - **3D模式**
    - Canvas的渲染模式为World时，才会有
    - Dynamic Pixels Per Unit 动态像素密度 越大越清晰
- **GraphicRaycaster**
  - 图形射线投射器 ，用于检测UI输入事件的射线发射器
  - Ignore Reversed graphics 是否忽略反转图形<br>UI图形可以旋转x，y，z轴，x,y被反转180度后无法点击
  - Blocking Objects 射线被哪些3D物体阻挡，覆盖模式无效
  - Blocking Mask 射线被哪些层级物体阻挡，覆盖模式无效
- **EventSystem**
  - 事件系统，管理玩家输入事件并分发给各UI控件
  - **First Selected**
    - 首先选择的游戏对象
  - **Send Navigation Events**
    - 是否允许导航事件（通过键盘来操作按钮选中哪个，回车表示点击）
  - **Drag Threshold**
    - 拖拽操作的阈值，移动多少像素算拖曳
- **Standalone Input Moudle**
  - 独立输入模块，处理鼠标键盘等的输入
  - 热键轴管理，对应InputManager中热键的名字；
  - Input Action Per Second 每秒最多检测几次输入
  - Repeat Deley 重复操作的延迟时间
  - Force module active 是否强制 处于激活
- **Recttransform**
  - 矩形变换，继承transform，处理UI元素位置大小等
  - **参数**
    - pivot 中心点（0~1）矩形左下角（0，0）右上点（1，1）
    - Anchoors 相对父对象的锚点范围<br>当锚点为点时，PosXYZ是相对于锚点的偏移
      - 若锚点是范围，PosXY变成Left，Right，Top，Button表示UI对象左边，右边，上边，下边的距离，会拉伸
    - 虚线框（蓝图模式）编辑时外部矩形不会随着图片旋转而变化
    - R 原始编辑模式 轴心和锚点值不会改变矩形位置
    - 左边九宫格可以快速设置锚点，按住Alt可以同时设置中心点，按住Shift可以同时改位置
    - rp.anchiredPosition 在代码中得到自身锚点指向当前坐标的向量
  - **代码中得到RectTransform信息**
    - 用this.transform as RectTransform (里氏替换)

### 1.2 三大基础控件

- **Image**
  - UGUI中显示精灵图片的组件
  - **参数**
    - Source Image: 图片来源，必须是Sprite精灵类型
    - Color 图像的颜色
    - Material 图像材质（一般不修改）
    - Raycast Target是否作为射线检测目标 不勾选则不会响应射线检测
    - Maskable是否能遮罩
    - **ImageType图片类型**
      - Simple 均匀缩放整个图片
      - **Sliced 9宫格拉伸，只拉伸中央十字区域（防止四个角被拉伸）**
        - 要求下载2DSprite包，去原图文件上点SpriteEdtior后改变Border
        - Fill Center中心填充
        - 用来拼背景
      - Tiled 重复中央部分
      - **Filled 填充模式**
        - Fill Method 填充模式 可以来做血条，蓝条等效果
        - FillOrigin 填充原点
        - Fill Amount 填充量0-1
    - Preserve Aspect 保持宽高比
    - Set Native Size 设为原始效果
  - 代码修改

    示例代码如下：

    ```csharp
    Image image = this.GetComponent<Image>();
    image.sprite = Resources.Load<Sprite>("test");
    代码设置图片，需应用命名空间UnityEngine.UI
    ```

    ```csharp
    float time = 0;
        Image image;
        void Start()
        {
            image = this.GetComponent<Image>();
            image.sprite = Resources.Load<Sprite>("test");
            image.type = Image.Type.Filled;
            image.fillMethod = Image.FillMethod.Radial360;
            image.fillOrigin = (int)Image.Origin360.Right;

        }
        void Update()
        {
            time += Time.deltaTime;
            if(time > 10f)
            {
                time = 0;
            }
            image.fillAmount = time/10;
        }
    简单实现一个技能条功能
    ```

- **text**
  - 文本组件
  - **参数**
    - Text：文本内容
    - Font 字体
    - **FontStyle字体样式**
      - Normal普通<br>Bold 加粗<br>Italic 斜体
    - RichText 是否开启富文本
    - FontSize 字体大小
    - LineSpacing 行间距
    - Alignment 对齐方式
    - Align ByGeometry 字体范围设置，不用管
    - **Horizontal Overflow 处理文本太宽的处理方式**
      - Wrap：自动空行<br>Overfklow 溢出
    - **Verticall Overflow 处理文本太高的处理方式**
      - Truncate：截断<br>Overfklow 溢出
    - **BestFit 自动调整字体大小**
      - 能选择最小字体和最大字体
  - **富文本**
    - 类似xml，可以选择部分加粗
    - 加粗: &lt;b&gt;内容&lt;/b&gt;
    - 斜体： &lt;i&gt;内容&lt;/i&gt;
    - 大小： &lt;size=50&gt;内容&lt;/size&gt;
    - 颜色:&lt;color = red&gt;内容&lt;/color&gt;
  - **边缘线**
    - 引入Outline脚本
  - **阴影**
    - 引入Shadow脚本
  - **代码修改**
    - 同Image 引用UnityEngine.UI命名空间
    ```csharp
    Text tex = this.GetCompoment<Text>();
    tex.text = "1234";
    ```

- **RawImage**
  - 大图模式
  - Texture 图像纹理<br>UVrect图像在矩形内的偏移和大小

### 1.3 组合控件

- **Button**
  - 父对象是Button组件依附对象，挂了Image作为背景图<br>有个子对象作为按钮文本（能删）
  - 参数

    如下图所示：

    ![](/img/xmind/unityUGUI/02.png)

    ![](/img/xmind/unityUGUI/03.png)

  - **代码控制**
    - Button btn = this.Getcompoment&lt;Button&gt;();
  - **按钮监听事件**
    - 1.代码添加<br>2.脚本拖进去
    - 拖到OnClick中，拖对象，接着选脚本和函数

    示例代码如下：

    ```csharp
    代码
    btn.onClick.addListener(函数名);
    用Lamda表达式添加
    btn.onClick.AddListener(()=>
    {

    });
    移除加入函数的监听函数
    btn.onClick.RemoveListener(textClick);
    ```

- **Toggle**
  - 开关组件，处理单选框多选框
  - **参数**
    - 许多参数和Button相似
    - IsOn 是否处于打开状态
    - Toggle Transaction 开关过渡 Fade有淡入淡出 None无
    - Graphic 钩的图片，一般不改这个而是直接换图
    - Group 变成单选，需要有相同的Toggle Group组件，一般把多个Toggle放到同一个空物体的子对象中
      - Allow Switch  Off可以一个单选框都不选
  - 代码控制
    ```csharp
    引用命名空间 
    Toggle tog = this.GetComponent<Toggle>( );
    tog.isOn = true
    //得到ToggleGroup
    ToggleGroup togg = this.GetComponent<ToggleGroup>( );
    //通过迭代器得到toggleGroup中选中的Toggle
    foreach(Toggle tog in togg.ActiveToggles())
    ```

  - **监听事件**
    - 需要函数 （函数必须无返回值，有一个bool参数）
    - 直接拖动（一定要选上面动态的方法）静态则不能变化bool
    - 代码
      ```csharp
      tog.onValueChange.AddListener(函数名);
      //匿名函数
      tog.onValueChange.AddListener((参数b)=>
      {

      });
      ```

- **ImputField**
  - 输入字段，处理玩家文本输入
  - Placeholder是提示输入的<br>text是输入的内容
  - **参数**
    - TextComponent关联输入内容文本组件
    - Text当前输入内容
    - Character Limit 输入字符的长度最大值
    - ContentType限制类型
    - LineType 行类型<br>SingleLine单行模式<br>Multi Line Submit自动空行<br>Multi Line NewType可以按回车空行
    - PlaceHolder关联初始显示的组件
    - Caret Blink Rate光标闪烁速率
    - Caret Width光标宽
    - Custom Caret Coler自定义光标颜色
    - Read Only只读不能改
  - 代码控制
    ```csharp
    InputField inf = this.GetComponent<InputField>();
    inf.text = "123"',引用UnityEngine.UI
    ```

  - **监听**
    - 有两套监听组件<br>OnValueChange<br>和<br>OnEndEdit<br>使用的函数必须无返回值，有string参数
- **Slider**
  - 由背景图，进度条，滑动块组成
  - **参数**
    - FillRect填充的进度条图形
    - HandleRect滑动块图形都不要改
    - Dricton 方向
    - minValue，maxValue，value最小最大值，当前值
    - WholeNumber 只能整数变化
  - 代码控制
    ```csharp
    Slider s = this.GetCompoment<Slider>();
    s.value 得到值
    ```

  - **监听**
    - s.OnValueChange(函数)<br>函数必须无返回值，一个浮点数的参数
- **Scrollbar**
  - 滚动条，一般是配合ScrollView滚动视图使用
  - **参数**
    - HandleRect图形对象，不要改
    - Direction方向
    - Value初始位置值
    - Size 滚动块大小
    - Number Of Steps允许可以滚动多少次
  - **代码控制**
    - 老套路，可以改sb.size 和sb.value
  - **监听**
    - 有onValueChange
    - 必须无返回值，有浮点数参数表示value
- **ScrollView**
  - 内部的脚本叫做ScrollRect<br>创建后自带两个滚动条，可以选择删掉
  - **参数**
    - Content作为显示对象父对象决定，滚动条范围和他有关
    - Horizontal<br>Vertical 是否能水平，垂直拖动
    - **movementType 滚动类型**
      - Elastic常用 回弹效果<br>Easticity回弹系数，越大越难回来
      - Clamped夹紧，无法移除范围
    - **Iertia惯性**
      - 松开鼠标还有惯性
      - DecelerationRate 减速率0没有惯性，1没有阻力
    - ScrollSensitivity鼠标中键移动速率
    - ViewPort 可视范围视口大小
    - **Visibility可见模式**
      - permanent永久显示
      - AutoHide  Content小就隐藏
      - AutoHideAndExpandViewport 不仅隐藏还会顶满ViewPort（常用）
    - Spacing 滚动条和Viewport间隔空间
  - 删了滚动条要置空Scrollbar，还要手动调整视口
  - 代码控制
    ```csharp
    ScrollRect sr = this.GetComponent<ScrollRect>();
    sr.contnet.sizeDelta += new Vector2(300,300); //额外增加Content大小（x + 300,y + 300）如果不用+=而用=则是赋值
    //Content常作为内容的父对象
    sr.normalizePosition = new Vector2(0,0.5f);//修改显示位置 范围是0，1
    ```

  - **监听**
    - onChangeValue方法<br>传入 Vector2 表示当前拖入位置，范围0到1
- **dropDown**
  - 下拉列表<br>Label当前选择的内容<br>Arrow箭头图片<br>Teplate选择单
  - **参数**
    - Template关联的下拉列表对象
    - CaptionText关联显示当前选择内容的图片
    - AlphaFadeSpeed下拉列表淡入淡出速度，越小越快
    - Options存在的选项列表
    - Value 列表选择的索引值
    - CaptionImage ItemImage都传入空图片<br>之后就能在Options传入Sprite精灵图
  - 代码
    ```csharp
    Dropdown dd = this.GetComponent<Dropdown>();
    dd.value //得到索引
    dd.options[dd.value] 得到索引对应元素
    //dd.option是一个Dropdown.OptionData的List类 
    //可以点出text（字符串信息），image（图片信息）
    dd.options.Add(new Dropdown.OptionData("123")); //添加选项
    ```

  - **监听**
    - onValueChange的方式<br>传入Int参数，无返回值

### 1.4 图集制作

主要包括：

- 减少DrawCall，提高性能
- **DrawCall**
  - CPU通知GPU的意思<br>即CPU准备好渲染数据，通知GPU渲染的过程<br>多次传输文件速度满，单次传输同等大小的文件速度就快，压缩的意义
  - UI层降低DrawCall 小图合成大图
- **Unity自带打图集方法**
  - 允许使用图集

    如下图所示：

    ![](/img/xmind/unityUGUI/04.png)

  - create-&gt;2D-&gt;Sprite-&gt;sprite atlas 创建图集
  - Allow Rotation自动旋转<br>Tight Packing 刨掉空白<br>都不要勾选<br>在Object for Packing中加入Sprite图<br>最后点PackPreview生成图集
  - stats中的Batches可以当作是DC的次数
    ![](/img/xmind/unityUGUI/05.png)

  - 在一个图集的多个图之间（位置重叠，层数也重叠）插入其他图，会打断批处理（Image和Text都会打断）
  - 代码加载

    示例代码如下：

    ```csharp
    SpriteAtlas sa = Resource.Load<SpriteAltas>("位置");
    sa.GetSprite("图片名");//从图集中载入指定的图
    应用UnityEngine.U2D
    ```

## 2. 进阶知识

最后整理进阶知识。

### 2.1 事件监听接口

主要包括：

- 所有控件只有常用事件监听<br>事件监听接口可以提供长按，双击，拖动等效果
- **常用事件接口**
  - 接口名-接口需实现函数名-功能

    如下图所示：

    ![](/img/xmind/unityUGUI/06.png)

- 不常用事件接口
  ![](/img/xmind/unityUGUI/07.png)

- **实现事件接口**
  - 1.引用命名空间UnityEventSystems，在脚本类（带Mono）中基础对应接口<br>2.实现接口中方法<br>3.将脚本挂在相应UI控件中
- **PointEvenData类 （父类是BaseEvenData）**
  - pointerId 鼠标左右中键点击鼠标的ID 通过他判断是哪个键点击
  - position鼠标当前位置 屏幕坐标系左下角0，0
  - pressPosition 按下的时候指针位置
  - delta 鼠标移动增量
  - clickCount 连击次数
  - clickTime 点击时间
  - pressEventCamera 最后一个OnPointerPress按下事件关联的摄像机
  - enterEventCamera 最后一个OnPointerPress进入事件关联的摄像机
- 不太好管理，比较麻烦

### 2.2 EventTrigger事件触发器

- EventTrigger组件，集成了所有事件监听接口<br>对任意gameObject右键安装组件
- **如何使用**
  - **拖曳脚本关联**
    - 建一个Eventrigger 然后在AddNewEventType上创建监听事件（需要参数BaseEventData）<br>我们可以用里氏替换把BaseEvenData as成PointEventData
  - 代码添加

    示例代码如下：

    ```csharp
    1.将外面的EventTrigger传入进来
    EventTrigger et;
    2.新建监听对象
    EventTrigger.Entry entry = new EventTrigger.Entry();
    3.声明事件类型
    entry.eventID = EventTriggerType.PointerUp;
    4.监听函数关联
    entry.callback.AddListener(函数带参数EventData);
    5.将对象加入到et列表中
    et.trigger.Add(entry);
    ```

### 2.3 屏幕坐标转UI相对坐标

- RectTransformUtility类有很多静态方法可以将屏幕空间上的点转成UI本地坐标点
- 常用于拖拽,相比于直接改偏移位置，表现形式更好

示例代码如下：

```csharp
RectTrasformUtility.ScreenPointToLocalPointInRectangle(
	this.transform.parent as RectTransform,
	eventData.position,
	eventData.enterEventCamera,
	out nowPos);
//参数1：相对父对象，参数2：屏幕点，参数3：摄像机，参数4：最终得到的点
//eventData是PointEventData类对象
//写在事件函数中

this.transform.localPosition = nowPos;
//修改位置
```

### 2.4 遮罩

主要包括：

- 在不改变图片的时候部分显示图片
- 在父对象上添加Mask组件，所有子对象都会遮罩<br>1.想要被遮罩的Image需要勾选Maskable<br>2.只要父对象添加了Mask组件，所有UI子对象都会被遮罩<br>3.遮罩父对象图片的制作，不透明的地方显示，透明的地方被遮罩
- ShowmaskGraphic 是否显示父对象遮罩用的图片

### 2.5 模型和粒子显示在UI前

主要包括：

- 直接用摄像机渲染3D物体<br>之前Canvas讲过
- **将3D物体显示在图片上，通过图片显示**
  - 类似小地图的形式，用特定的摄像机画到Render Texture<br>之后用RawImage来显示Render Texture
  - 浪费性能，最好场景上只有一个模型
- **粒子特效**
  - 可以改变粒子特效的排序层，可以始终显示在图前面

### 2.6 异性按钮

- 图片形状不是矩形的按钮
- **如何准确的点击**
  - 按钮响应点击是自下而上的，我们可以用多个子对象，这些子对象可以是图片和文字<br>我们可以用多个透明的的按钮作为图片子对象来拼出不规则按钮，按钮变色要联系到父对象图片

  示例代码如下：

  ```csharp
  通过代码改变图片透明度响应阈值
  第一步 修改图片参数，开启Read/Write Enable开关
  第二部：修改图片响应阈值（当像素点alpha小于该值，就不会被射线检测）
  img.alphaHitTestMinimumThreshold = 0.1f;
  内存消耗高
  ```

### 2.7 CanvasGroup

主要包括：

- 画布组
- 整体控制面板的淡入淡出，隐藏
- **为面板添加CanvasGroup组件**
  - **参数**
    - Alpha 整体透明度
    - Interactable 整体启用禁用设置
    - Blocks Raycasts 整体射线检测设置
    - Ignore Parent Groups是否忽略父级CanvasGroup作用

### 2.8 自动布局组件

主要包括：

- 自动布局控制组件 + 布局元素 = 自动布局
- 布局元素有多个属性，一般来说不会改，可以用手动添加LayoutElement组件修改
- 所有自动布局组件一定是加到ScrollView内部的Content上
- **水平和垂直布局组件**
  - Horizontal Layout Group水平<br>Vertical Layout Group垂直
  - 把他们放到父对象中，子对象可以自动布局
  - Padding左右上下偏移位置
  - Spacing 子对象的间距
  - ChildAlignment九宫格对其
  - UseChildScale是否控制子对象缩放
  - Child Force Expand是否强制子对象扩展以填充可用空间（平均分配）
- **网格布局组件**
  - Grid Layout Group
  - CellSize 每个格子的大小
  - Spacing 格子间隔
  - Start Corner第一个元素所在位置
  - Start Axis 沿哪个轴放
  - Child Alignment 格子对其方式
  - **Constraint 行列约束**
    - Flexible灵活模式
    - Column固定列
    - Row固定行
- **内容大小适配器**
  - Content Size Fitter
  - 一般在Text上用，自动修改容器大小
  - Horizontal Fit水平自适应<br>Vertical Fit竖直自适应
  - prefectSize 可以自动增加长宽
- **宽高适配器**
  - Aspect Ratio Fitter
  - **AspectMode适配模式**
    - None 不让矩形适应宽高比<br>Width Controls Height 根据宽度自动调整高度<br>Height Controls Width 根据高度自动调整宽度<br>Fit in Parent 自动适应父对象（有黑边）<br>Envelope Parent 自动适应父对象 （有裁剪）
