---
title: "Unity核心_2_动画"
date: 2026-11-04 18:20:03
categories:
  - "Unity"
tags:
  - "XMind转换"
  - "Unity"
  - "Animator"
---

> 这篇「Unity核心_2_动画」笔记是过去思维导图笔记的ai转换版。

## 1. 动画基础

这一节先整理动画基础。

### 1.1 Animation

主要包括：

- **打开Animation**
  - Windows-&gt; Animation-&gt;Animation
- Animationc窗口可以在Unity内部制作动画1<br>原理 在固定时间点对象挂载脚本的变化<br>播放时 将制作动画时记录的数据在固定时间点改变
- **面板功能**
  - **面板左侧**
    - 从左至右：<br>1.预览模式（开关）<br>2.录制模式（开关）打开后预览模式默认开启<br>3.回到动画开头<br>4.上一关键帧（快捷键：键盘逗号）<br>5.播放动画（快捷键：键盘Alt+逗号）<br>6.下一关键帧（快捷键：键盘句号）<br>7.回到动画结尾（快捷键：键盘Alt+句号）<br>8.当前处于第几帧

      如下图所示：

      ![](/img/xmind/Unity核心_动画/01.png)

    - Dopesheet：关键帧模式<br>Curves：曲线模式
      ![](/img/xmind/Unity核心_动画/02.png)

    - 从左至右：<br>按选择筛选<br>添加关键帧<br>添加事件
      ![](/img/xmind/Unity核心_动画/03.png)

  - **面板右侧**
    - 动画时间轴面板<br>当编辑动画时，会在该面板上编辑关键帧等信息
      ![](/img/xmind/Unity核心_动画/04.png)

- **编辑动画**
  - 选中要加动画的gameObject，在Animation上Create，会给一个动画文件一个动画状态机，一个Animator脚本
  - **面板变化**
    - **左侧面板**
      - 多出一个可以选择当前动画的下拉列表<br>可以在这里创建新动画和切换动画
        ![](/img/xmind/Unity核心_动画/05.png)

      - 多出一个可以添加变化属性的按钮<br>在这里你可以任意添加你想要在动画中变化的脚本变量
        ![](/img/xmind/Unity核心_动画/06.png)

    - **右侧面板**
      - 时间轴可以拖动<br>注意：<br>时间轴上的单位为n秒n帧<br>一格代表一帧（并不是秒）
      - 选择关键帧右键
        ![](/img/xmind/Unity核心_动画/07.png)

        - Add Key：添加关键帧<br>Delete Key：删除关键帧<br>Clamped Auto：切线模式，自动设置切线<br>Auto：旧版切线模式，和Clamped Auto基本类似，主要用于老动画系统，建议不使用除非是老动画<br>Free Smooth：自由设置切线<br>Flat：切线设置为水平<br>Broken：单独控制左右曲线切线<br>Free：自由设置<br>Linear：直线<br>Constant：常量切换<br>Weighted：权重切换
  - **动画文件界面参数**
    - Loop Time：是否是循环动画（在动画结尾时重新开始）<br>Loop Pose：无缝循环运动<br>Cycle Offset：循环动画在其他时间开始时的周期偏移
      ![](/img/xmind/Unity核心_动画/08.png)

    - **按右边1三个点可以进入Debug**
      - 我们可以在SampleRate中修改1秒有多少帧，上面给的是60<br>wrapMode可以修改展示模式，有循环等
        ![](/img/xmind/Unity核心_动画/09.png)

- **老动画系统**
  - **参数相关**
    - Animation：默认播放的动画<br>Animations：该动画组件可以控制的所有动画<br>Play AutoMatically：是否一开始就自动播放默认动画<br>Animate Physics：动画是否与物理交互<br>Culling Type：决定什么时候不播放动画<br>Always Animate：始终播放<br>Based On Renderers：基于默认动画姿势剔除
      ![](/img/xmind/Unity核心_动画/10.png)

    - Default：读取设置得更高的默认重复模式<br>Once：播放一次就停止<br>Loop：从头到尾不停循环播放<br>PingPong：从头到尾从尾到头不停播放<br>ClampForever：播放结束会停在最后一帧，并且会一直播放最后一帧（相当于状态不停止），表现效果和Once一样，但是逻辑处理上不同
      ![](/img/xmind/Unity核心_动画/11.png)

  - 在gameObject中插入Animation组件后Unity会自动1采用老动画系统
  - 代码控制

    示例代码如下：

    ```csharp
    先得到Animation脚本
    Animation ani = this.GetComponent<Animation>();
    //播放动画
    animation.Play("动画名");
    // 淡入播放，会从当前状态变化成目标动画，不会强行回到动画开头状态
    animation.CrossFade("动画名")；
    //前一个放完再放下一个
    animation.PlayQueue("动画名");
    animation.CrossFadeQueue("动画名");//带淡入
    //停止所有动画
    animation.Stop();
    //动画是否在播放
    if(animation.IsPlaying("动画名"))
    //播放模式的设置
    animation.warpMode = WrapMode.Loop;
    设层级权重
    animation["动画名"].layer = 1;
    animation["动画名"].weight = 1;
    ```

    - 动画事件，可以在Animation窗口创建事件<br>事件可以用一个可以有参无返回的函数，当动画播到事件时会自动执行函数

### 1.2 有限状态机

- 简称状态机<br>表示角色在有限个状态里自由切换的行为

### 1.3 Animator

- **在物体上直接创建动画附带一个状态机<br>也可以在Project中手动创建**
  - **左侧面板**
    - Layers：动画层级页签，为动画添加更多的层级，层级高的动画播放会覆盖层级低的<br>Parameters：参数页签，为动画状态机添加控制状态切换的参数<br>眼睛图标：显隐左侧面板

      如下图所示：

      ![](/img/xmind/Unity核心_动画/12.png)

  - **右侧面板**
    - 网格化布局区域：<br>主要用于编辑状态之前的切换关系<br>1.窗口中的每一个矩形表示一个状态<br>2.窗口中的每一个箭头表示一个切换条件<br>矩形说明：<br>默认三大矩形：<br>绿色Entry矩形：进入状态机流程<br>红色Exit矩形：退出状态机流程<br>Any State：任意状态，代表状态机中的任意状态<br>人为添加矩形：<br>橙色矩形：一开始的默认状态动画，和Entry相连<br>表示一开始播放的动画<br>灰色矩形：自己添加的某一种动作状态
      ![](/img/xmind/Unity核心_动画/13.png)

  - **添加状态**
    - 右键添加空状态，把动画拖入就能使用
  - **添加连线**
    - 右键第一个
    - 右键1第二个设为默认动画
  - **条件**
    - 在Parameters中可以多创建几个条件，右键箭头在右侧Conditions中可以添加条件
    - hasExitTime是完成动作后才会变
- **代码控制**
  - **参数相关**
    - Controller：对应的动画控制器（状态机）<br>Avatar：对应的替身配置信息（之后讲解3D模型时详细讲解）<br>Apply Root Motion：是否启用动画位移更新<br>UpdateMode：更新模式（一般不修改它）<br>Normal：正常更新<br>Animate Physics：物理更新<br>Unscaled Time：不受时间缩放影响<br>Culling Mode：裁剪剔除模式<br>Always Animate：始终播放动画，即使在屏幕外也不剔除<br>Cull Update Transforms：摄像机没有渲染该物体时，停止位置、IK的写入<br>Cull Completely：摄像机没有渲染物体时，整个动画被完全禁用
      ![](/img/xmind/Unity核心_动画/14.png)

  示例代码如下：

  ```csharp
  //先得到Animator
  Animator ani =  this.GetComponent<Animator>();
  //通过条件转换
  ani.SetFloat("条件名",1.3f);
  //得到条件值
  ani.GetFloat("条件名",1.3f);
  //直接换
  ani.Play("条件名");
  ```

### 1.4 序列帧动画

- 在一定时间内不停播放不同图片实现动画
- 方法<br>创建一个空物体，加入新动画脚本<br>修改动画Debug中的帧间隔时间接着把所有需要的序列帧图片全选拖入动画中，

### 1.5 2D骨骼动画

主要包括：

- 1.使用2D Animation制作（要在PackageManager下载1）<br>2.使用Spine制作
- 单张图片骨骼

  如下图所示：

  ![](/img/xmind/Unity核心_动画/15.png)

    - Reset Pose<br>将角色骨骼和关节恢复到原始位置
    - Sprite Sheet：<br>图集显示
    - Copy<br>复制当前选择的数据
    - Paste<br>粘贴复制数据
  ![](/img/xmind/Unity核心_动画/16.png)

    - **Bone<br>骨骼相关**
      - Preview Pose<br>预览模式，可以预览动作并不会真正的改变设置
      - Edit Bone<br>编辑骨骼，可以改变骨骼的位置、长度、方向、名称等等
      - Create Bone<br>创建骨骼
      - Split Bone<br>拆分骨骼，将一个骨骼一分为二
    - **Geometry<br>蒙皮相关<br>蒙皮决定了骨骼主要控制哪一部分**
      - Auto Geometry<br>自动蒙皮
        ![](/img/xmind/Unity核心_动画/17.png)

          - OUtline Detail<br>边缘细节，值越大，轮廓越细致
          - Alpha Tolerance<br>阿尔法公差值，控制蒙皮细节
          - Subdivide<br>细化程度，控制蒙皮细节
          - Weights<br>是否自动设置权重，一般勾选
      - Edit Geometry<br>编辑蒙皮
      - Create Vertex<br>创建顶点
      - Create Edge<br>创建边线
      - Split Edge<br>拆分边，用一个新的顶点分离一个边
    - **Weights<br>权重相关<br>决定了当骨骼动时如何印象顶点和边**
      - Auto Weights<br>自动赋予权重
      - Weight Slider<br>编辑顶点和边的权重
        ![](/img/xmind/Unity核心_动画/18.png)

          - Mode：计算模式<br>Add And Subtract：加减法<br>Grow And Shrink：增长和收缩<br>Smooth：平滑
          - Bone：设置权重的骨骼
          - Normalize：标准化设置
          - Amount：数量级
          - Vertex Weight：顶点权重<br>对应的骨骼
      - Weight Brush<br>用笔刷赋予权重
        ![](/img/xmind/Unity核心_动画/19.png)

          - Size：笔刷大小
          - Hardness：笔刷强度，越大效果越明显
          - Step：步数
      - **Bone Influence<br>选择骨骼用的Sprite**
        - 主要用于在psb图片中使用<br>骨骼控制点的图片关联
          ![](/img/xmind/Unity核心_动画/20.png)

  ![](/img/xmind/Unity核心_动画/21.png)

    - **Visibility<br>切换选定精灵或骨骼的可见性**
      - 左侧拖动条<br>控制编辑时骨骼透明度
      - 右侧拖动条<br>控制编辑时权重透明度
      - 下方列表<br>浏览各骨骼名和骨骼层级信息
- **图集骨骼编辑**
  - 设置sprite为图集模式，对图片进行切片
  - 编辑图集
  - 最后在场景创建根对象在GameObject中设置父子关系
- **使用骨骼**
  - 为对象加入组件Sprite Skin 点击生成骨骼就能拿来做关键帧了
- psb文件编辑骨骼信息
  ![](/img/xmind/Unity核心_动画/22.png)

    - Extrude Edges：图片边缘延伸网格
    - Import Hidden：是否导入psb文件中隐藏的图层
    - Moszic：启用后，将图层生成Sprite，并将他们合并成单个纹理
    - Character Rig：是否使用人物已经绑定的骨骼
    - Use Layer Grouping：使用psb文件中的层分组
    - Pivot：轴心点位置
    - Reslice：从导入层重新生成Sprite，并清除对Sprite的任何更改，只有启用Moszic后又用
    - Keep Duplicate Name：让Sprite名称保留PSB文件中的名字
- **IK**
  - Ik（反向动力学）可以让子骨骼移动父骨骼
  - 在PackageManager中引入（合并到2D Animation中）
  - **使用**
    - 为父对象添加脚本IKManager2D
    - 为产生反向的骨骼末端添加空物体作为默认位置
  - IK Solvers：IK解算器，在这里添加IK<br>Weight：权重，当有多个IK控制同一点时权重会影响控制的百分比<br>Restore Default Pose：回复默认位置
    ![](/img/xmind/Unity核心_动画/23.png)

    - Chain（CCD）：可以自定义影响N个关节点，不能反向<br>Chain（FABRIK）：可以自定义影响N个关节点，可以反向<br>Limb：只会影响3个关节点
      ![](/img/xmind/Unity核心_动画/24.png)

  - Effector：默认的IK点位置<br>Target：会根据IK点位置生成真正的IK点对象<br>Flip：反向<br>Constrain Rotation：约束旋转程度<br>Solve from Default Pose：从默认姿势进行求解计算<br>Weight：权重
    ![](/img/xmind/Unity核心_动画/25.png)

  - Chain Length：IK影响的骨骼数量<br>Iterations：算法运行的次数<br>Tolerance：容错程度<br>Velocity：速度
    ![](/img/xmind/Unity核心_动画/26.png)

- **换装**
  - 换装的一个方法是把所有需要的装备先画好然后隐藏<br>需要先开启导入隐藏资源的选项
  - 需要在资源中创建SpriteLibrary Asset，把图集中Asset资源拖进来<br>接着在游戏中创建对象，根目录要带有Sprite Library<br>关键图层腰带Sprite Resolver用来换图
  - 代码修改

    示例代码如下：

    ```csharp
    SpriteResolver sr;//引用命名空间UnityEngine.Experimental.U2D.Animation
    //sr.GetCategory() 获取当前部位的默认类别名
    sr.SetCatgoryAndLable(sr.GetCatgory(),"Log名称")；
    ```

    ```csharp
    好用的方法
    用一个字典<string，SpriteResolver>存
    用SpriteResolver[] srs = this.GetComponentsInChildren<SpriteResolver>();,然后遍历数组赋值给字典，键为srs[i].Get Category(),值为srs[i]
    ```

- **spine**
  - **Spine骨骼动画参数相关**
    - **知识点**
      - 骨骼数据文件
        ![](/img/xmind/Unity核心_动画/27.png)

          - SkeletonData JSON:骨骼数据文件
          - Scale：缩放大小
          - Skeleton Data Modifiers：骨骼数据修改器
          - Blend Mode Materizls：混合模式材质
          - Apply Additive Material：是否使用叠加材质
          - Additive Materials：叠加材质
          - Multiply Materials：相乘材质
          - Screen Materials：屏幕材质
          - Atlas Assets：图集资源
          - **Mix Settings：混合设置**
            - Animation State Data：动画状态数据<br>Default Mix Duration：默认混合持续时间
            - Add Custom Mix：添加自定义混合（可以指定某两个动画之间的持续时间）
        - Preview：预览
          ![](/img/xmind/Unity核心_动画/28.png)

          - Animations：动画
          - Setup Pose：设置姿势（还原到默认姿势）
          - Create Animation Reference Assets：创建动画参考资源
          - Slots：插槽相关（一个部位有多张图片构成，可以在这预览）
          - SkeletonMecanim：骨骼机制<br>Controller：关联动画控制器<br>SkeletonMecanim是SkeletonAnimation的替代品，它不是必须的
        - Skin：蒙皮选择
          ![](/img/xmind/Unity核心_动画/29.png)

      - 脚本组件
        ![](/img/xmind/Unity核心_动画/30.png)

          - SkeletonData Asset：<br>关联的骨骼动画信息
          - Animation Name：<br>当前播放的动画名
          - Loop：<br>是否循环
          - Initial Skin：<br>初始蒙皮<br>美术在制作时可能有几套蒙皮<br>一般情况下只有一套 不需要修改
          - Time Scale：<br>时间缩放，值越大动画播放的越快
          - Root Motion：<br>是否添加根运动的脚本<br>一般情况下不添加
        ![](/img/xmind/Unity核心_动画/31.png)

          - Initial Flip X/Y：初始翻转X和Y
          - **Update When Invisible：不可见时是否更新**
            - Nothing：不更新<br>Only Animation Status：仅动画状态<br>Only Event Timelines：仅事件<br>Everything Except Mesh：除了网格其它都更新<br>Full Update：更新所有
              ![](/img/xmind/Unity核心_动画/32.png)

          - Use Single Submesh：使用单个子网格
          - Fix Draw Order：固定提取顺序
          - Immutable Triangles：不变三角形
          - Clear State On Disable：禁用时清楚状态
          - Separator Slot Names：分隔符插槽名称
          - Z Spacing：Z间距
          - **Vertex Data：顶点数据**
            - PMA Vertex Colors：PMA顶点颜色
            - Tint Black：淡黑色
            - Add Normals：添加法线
            - Solve Tangents：求解切线
          - Add Skeleton Utility：添加骨骼公共程序
        ![](/img/xmind/Unity核心_动画/33.png)

          - Show Bone Names：显示骨骼名字
          - Show Paths：显示路径
          - Show Shapes：显示形状
          - Show Constraints：显示约束条件
          - ScaleX/Y：XY的缩放
          - RGBA：颜色
          - Bone：骨骼<br>Show Bone Names：显示骨骼名字
          - Slots：插槽
          - Constraints：约束条件
          - Draw Order and Separators：提取顺序和分离器相关
          - Events：事件
          - **Data Counts：数据数量**
            - Bones：骨骼数量
            - Slots：插槽数量
            - Skins：蒙皮数量
            - Events：事件数量
            - IK Constraints：IK约束数量
            - Transform Constraints：位置约束数量
            - Path Constraints：路径约束数量

### 1.6 3D模型导入

主要包括：

- 一般推荐模型为fbx，要求z轴为面朝向，y为头顶，x为右侧
- Model页签

  如下图所示：

  ![](/img/xmind/Unity核心_动画/34.png)

    - Scene<br>场景相关设置
      ![](/img/xmind/Unity核心_动画/35.png)

      - Scale Factor<br>当模型中的比例不符合项目中的预期比例时<br>可以修改此值来改变该模型的全局比例<br>Unity的物理系统希望游戏世界中的1米在导入模型文件中为1个单位
      - Convert Units<br>启用可将模型文件中定义的模型比例转换为Unity的比例<br>不同的格式的比例如下<br>.fbx .max .jas = 0.01<br>.3ds = 0.1<br>.mb .ma .lxo .dxf .blend .dae = 1
      - Import BlendShapes<br>是否允许Unity随网格一起导入混合形状<br>当导入包含混合形状的网格时，将使用Skinned MeshRenderer组件<br>注意：<br>1.导入混合形状发现需要在FBX文件中具有平滑组<br>2.如果想要导入具有法线的混合形状<br>把下方的Blend Shape Normals属性设置为Import，将使用FBX文件的发现<br>或者<br>把下方的Blend Shape Normals属性设置为Calculate，Unity使用相同的逻辑来计算网格和混合形状上的法线
      - Import Visibility<br>是否导入可见性<br>开启后可以从FBX文件中读取可见性属性。<br>比如模型动作里 有些动作是要隐藏模型形象的，开启后才会生效<br>一些3D建模软件对可见性属性不支持或者有限制<br>比如Maya和Blender就对可见性有限制<br>所以一般这个选项要根据你使用的建模软件决定<br>一般可以不勾选
      - Import Cameras<br>是否导入摄像机<br>是否把FBX文件中的摄像机也导入，但是Unity支持FBX中摄像机的部分属性，比如正交或透视，是否支持动画，物理属性，远近裁剪面等等<br>一般不勾选
      - Import Lights<br>是否导入光源<br>支持的光源类型<br>全局光、聚光灯、方向光、面光源<br>支持的光源属性<br>范围、颜色、强度、角度<br>一般不使用
      - Preserve Hierarchy：<br>始终创建一个显示预制体根<br>通常在导入的时候，FBX会将模型中的空根节点进行优化去掉它<br>但是如果多个FBX文件中包含同一层级的空跟对象，可以勾选它来保留他们<br>主要作用是：比如有两个fbx文件，1包含骨骼和网格，2只包含骨骼动画。如果不启用它导入2，那么Unity将剥离根节点，会让层级不匹配让动画不能正常播放
      - Sort Hierarchy By Name<br>在层级窗口中根据名字排序子物体<br>如果不启用，会保留FBX文件中定义的层级顺序
    - Meshes<br>网格相关设置
      ![](/img/xmind/Unity核心_动画/36.png)

      - Mesh Compression<br>网格压缩<br>设置压缩比级减小网格的文件大小<br>提高压缩比会降低网格的精度<br>调整该参数可以优化游戏包的大小
        ![](/img/xmind/Unity核心_动画/37.png)

        - Off：不使用压缩
        - Low：低压缩比
        - Medium：中等压缩比
        - High：高压缩比
      - Read/Write Enabled<br>是否开启读写网格信息<br>如果开启，Unity将网格数据传给GPU后，在CPU中还会保留可寻址内存，意味着我们可以通过代码访问网格数据进行处理<br>如果不开启，Unity将网格数据传个GPU后，会将CPU中的可寻址内存中网格数据删除，我们无法再得到网格数据<br>开启时，会增加内存占用，关闭时，可以节约运行时内存使用量<br>何时开启？<br>1.需要在代码中读取或写入网格数据<br>2.需要运行时合并网格<br>3.需要使用网格碰撞器时<br>4.需要运行时使用NavMesh构建组件来烘焙NavMesh时<br>等等
      - **Optimize Mesh<br>确定三角形在网格中列出的顺序以提高GPU性能**
        - Nothing：无优化
        - Everything：对顶点以及多边形顶点索引进行重新排序
        - Polygon Order：仅对多边形重新排序
        - Vertex Order：仅对顶点重新排序
      - Generate Colliders<br>生成碰撞器<br>启用后会自动附加网格碰撞器的情况下导入你的网格<br>建议不移动的环境几何体可以开启它，但是需要移动的几何体建议不要开启它
    - Geometry<br>几何体相关设置
      ![](/img/xmind/Unity核心_动画/38.png)

      - Keep Quads<br>保留四边形<br>启用后，Unity不会将4个顶点的多边形转为三角形<br>当使用曲面细分着色器时可能需要启用此选项，因为四边形的曲面周色漆比多边形的效率更高<br>Unity 可以导入任意类型的多边形（三角形到 N 边形）。顶点数量超过四个的多边形将始终转换为三角形，无论此设置如何。<br>如果一个网格有四边形和三角形（或者转换为三角形的 N 边形），那么 Unity 会创建两个子网格来分离四边形和三角形。每个子网格要么只包含三角形，要么只包含四边形。
      - Weld Vertices<br>合并在空间中共享相同位置的顶点，前提是这些顶点总体上共享相同的属性（UV，法线，切线等等）<br>开启后相当于会通过减少网格的总数量来优化网格的顶点计数<br>一般都开启，除非你想有意保留这些重复顶点，之后想通过代码去获取他们来进行处理
      - Index Format<br>网格索引缓冲区的大小
        ![](/img/xmind/Unity核心_动画/39.png)

        - 一般都选择16bits，Auto可以会默认选择16bits<br>只有在必要时使用32bit<br>16bits即通用又节约内存
      - Legacy Blend Shape Normals<br>启用后会基于Smoothing Angle值来计算法线
      - Normals<br>定义如何计算法线
        ![](/img/xmind/Unity核心_动画/40.png)

        - Import：从文件中导入法线，如果文件中不包含发现信息，将使用Calculate模式计算法线
        - Calculate：根据Normals Mode、Smoothness Source和Smoothing Angle属性来计算发现
        - None：不计算法线
      - Blend Shape Normals<br>定义如何为混合形状计算法线<br>只有当Legacy Blend Shape Normals禁用时出现
        ![](/img/xmind/Unity核心_动画/41.png)

      - Normals Mode<br>计算法线的模式，只有当上方的Normals设置为Import和Calculate才会出现
        ![](/img/xmind/Unity核心_动画/42.png)

        - Unweighted Legacy：2017.1版本之前计算法线的方式，如果是在该版本之前导入的所有FBX模型，默认设置为该模式
        - Unweighted：法线不加权重
        - Area Weighted：法线按照图面面积加权重
        - Angle Weighted：法线按照每个图面上的顶角加权重
        - Area And Angle Weighted：法线按照每个图面上的图面面积和顶角加权重，这是默认选项
      - Smoothness Source<br>如何确定平滑，哪些边应该平滑，哪些应该粗糙<br>只有当Legacy Blend Shape Normals 禁用时出现
        ![](/img/xmind/Unity核心_动画/43.png)

        - Prefer Smoothing Groups：尽可能使用模型文件中的平滑组
        - From Smoothing Groups：仅使用模型文件中的平滑组
        - From Angle：使用Smoothing Angle值来确定哪些边应该是平滑的
        - None：不拆分硬边的任何顶点
      - Smoothing Angle<br>控制是否为硬边拆分顶点<br>通常，值越大，产生的顶点越少<br>仅当Normals设置为Calculate时才可用<br>注意：此设置仅用于非常光滑的或者非常复杂的模型，否则，最好在3D建模软件中手动平滑然后导入，始终建议建模的时候就做好，更加准确
      - Tangents<br>定义如何导入或计算顶点切线<br>仅当Normals设置为Calculate或Import时，此属性才可用
        ![](/img/xmind/Unity核心_动画/44.png)

        - Import：如果Normals设置为Import，则从FBX文件中导入顶点切线，如果网格没有切线，那么将无法使用法线贴图着色器
        - Calculate Legacy：使用旧版算法计算切线
        - Calculate Legacy With Split Tangents：使用旧版算法计算切线，并在UV图表上进行拆分。如果网格上的接缝碰坏了法线贴图光照，请使用此属性
        - Calculate Mikktspace：使用米克特空间计算切线
        - None：不导入顶点切线，网格没有切线，则无法使用法线贴图着色器
      - Swap UVs：在网格中交换UV通道。如果漫反射纹理使用光照贴图中的UV，请使用此选项
      - Generate Lightmap UVs：为光照贴图创建第二个UV通道
- **Rig页签**
  - **面板基础信息**
    - Animation Type<br>动画类型
      ![](/img/xmind/Unity核心_动画/45.png)

      - None<br>不存在动画<br>主要用于一些环境静态模型
        ![](/img/xmind/Unity核心_动画/46.png)

      - Humanoid<br>人形模型<br>一般情况下，有头和四肢（一个头两条腿两只手）为人形<br>人形模型需要使用Avatar化身系统<br>绑定人主要关节的映射关系
        ![](/img/xmind/Unity核心_动画/47.png)

        - Avatar Definition：选择获取Avatar定义的位置<br>No Avatar：没有化身系统信息<br>Create From This Model：根据此模型创建Avatar化身信息<br>Copy from Other Avatar：指向另一个模型上设置的Avatar化身信息
          ![](/img/xmind/Unity核心_动画/48.png)

        - Source：复制另一个具有相同骨架的Avatar化身信息以导入其动画剪辑<br>使用Copy From Other Avatar时才有
          ![](/img/xmind/Unity核心_动画/49.png)

        - Configure...：打开Avatar化身配置<br>使用Create From This Model时才有
          ![](/img/xmind/Unity核心_动画/50.png)

        - Skin Weights：设置影响单个顶点的最大骨骼数量<br>Standard（4 Bones）：使用最多4个骨骼来产生影响。默认值，处于对性能考虑，建议使用此设置<br>Custom：设置自定义的最大骨骼数，选择后会出现下方的两个选项<br>Max Bones/Vertex：定义每个顶点的最大估个数，值越大性能消耗越大<br>Max Bone Weight：设置考虑骨骼权重的最低阈值，权重计算时将忽略小于此值的内容
          ![](/img/xmind/Unity核心_动画/51.png)

        - Optimize Game Objects：在Avatar化身系统和Animator动画组件中删除和存储所导入角色的游戏对象骨骼层级信息。如果启用会出现下方的Extra Transforms to Expose选项。角色将使用Unity动画系统的内部骨架，可以提高动画角色的性能
          ![](/img/xmind/Unity核心_动画/52.png)

        - Extra Transforms to Expose：要公开的骨骼层级，在下方打钩将公开该骨骼层级信息<br>放大镜：通过名称搜索对应骨骼信息<br>Toggle All：全选或者反选<br>Collapse All：全部折叠<br>Expand All：全部展开
      - Generic<br>通用模型，非人形模型<br>不是标准的人形模型，可以是任意形状，可能有8只腿两个头等等<br>这种模型主要需要设置骨骼根节点
        ![](/img/xmind/Unity核心_动画/53.png)

        - Root Node：选择用于此Avatar的根节点的骨骼（仅当选择Create From This Model才会出现）
      - Legacy<br>旧版动画类型<br>与Unity3.x及更早版本导入和使用动画<br>一般不使用
        ![](/img/xmind/Unity核心_动画/54.png)

        - Generation：动画导入方法<br>Don't Import：不导入动画<br>第2~4个选项：已禁用，勿使用<br>Store in Root（New）：导入动画将其存储在模型的根节点中
          ![](/img/xmind/Unity核心_动画/55.png)

  - **Avatar化身信息设置**
    - Mapping：关节映射信息设置<br>Muscles&amp;Settings：肌肉和设置
      ![](/img/xmind/Unity核心_动画/56.png)

      - Mapping<br>我们需要在这个页签对模型关节进行映射设置<br>因为人物动画无非就是改变这些关节的角度
        ![](/img/xmind/Unity核心_动画/57.png)

          - 身体<br>头部<br>左右手<br>关节映射信息设置
        - 关节点映射关系
          ![](/img/xmind/Unity核心_动画/58.png)

        ![](/img/xmind/Unity核心_动画/59.png)

          - Clear：清空映射<br>AutoMap：自动映射<br>Load：从文件中读取<br>Save：保存映射信息
            ![](/img/xmind/Unity核心_动画/60.png)

          - Reset：重置姿势<br>Sample Bind-Pose：绑定姿势示例<br>Enforce T-Pose：强制T姿势
            ![](/img/xmind/Unity核心_动画/61.png)

      - **Muscles&amp;Settings**
        - Muscle Group Preview<br>肌肉群预览<br>可以在这里预览在不同姿势的旋转变化<br>用来观察之前的关联映射关系是否合理<br>主要起到预览作用
          ![](/img/xmind/Unity核心_动画/62.png)

        - Per-Muscle Settings<br>肌肉设置<br>用于设置各骨骼在旋转时的范围限制<br>因为如果不设置限制，在一些极限角度时会非常奇怪<br>我们可以在这里单独设置限制范围
          ![](/img/xmind/Unity核心_动画/63.png)

        - Additional Settings：高级设置<br>可以设置手脚的扭转和伸展值<br>一般不会修改他们<br>其中Translation DoF比较重要<br>如果启用，将启用人形角色的移动动画<br>如果禁用，Unity仅使用旋转对骨骼进行动画化<br>但是启用后，会提升性能消耗，因为动画需要执行额外步骤来重定向人形动画，除非动画包含角色某些骨骼的动画式移动才会启用<br>一般情况下禁用即可
          ![](/img/xmind/Unity核心_动画/64.png)

        - 重置所有设置
          ![](/img/xmind/Unity核心_动画/65.png)

- **Animation页签**
  - 动画和模型资源通常是分开导出的
  - **基础信息设置**
    - 不包含动画剪辑的模型
      ![](/img/xmind/Unity核心_动画/66.png)

    - 包含动画剪辑的模型
      ![](/img/xmind/Unity核心_动画/67.png)

      - Import Constraints：从此资源导入约束<br>启用后，Unity会自动添加相应的约束组件将其关联到正确的游戏对象
      - Import Animation：从此资源导入动画<br>如果禁用，下面的都没有，并且不会导入任何动画
      - Bake Animations：通过反向动力学（IK）或模拟创建的动画以便推进运动关键帧，仅用于Maya、3Dmax和Cinema4D文件
      - Anim.Compression：导入动画时使用的压缩类型<br>Off：禁用动画压缩，在导入时Unity不会减少关键帧数量，效果最好性能较低，文件较大，运行时内存占用也大。通常不建议使用<br>Keyframe Reduction：减少冗余关键帧，仅适用于Generic通用动画类型<br>Keyframe Reduction and Compression：减少关键帧并在文件中存储动画时压缩关键帧，会影响文件大小，但是内存大小和Keyframe Reduction相同，仅适用于Legacy旧版动画类型<br>Optimal：让Unity决定如何压缩，仅适用Generic通用和Humanoid人形动画类型
        ![](/img/xmind/Unity核心_动画/68.png)

      - Rotation Error：设置旋转曲线压缩容错度（百分比），原始旋转值和减小值之间的最小角度<br>Position Error：设置位置曲线压缩容错度（百分比）<br>Scale Error：设置缩放曲线压缩容错度（百分比）<br>如果原始值和消减值之间的差小于原始值乘以容错百分比，会删除关键帧<br>这些内容仅在Keyframe Reduction或Optimal压缩时可用
      - Animated Custom Properties：导入你指定为自定义用户属性的任何FBX属性
    - 动画剪辑选择列表<br>在这里我们可以看到所有的动画剪辑<br>可以通过+或-来新增剪辑或者删除所选的剪辑<br>在这里选择一个动画剪辑后<br>我们可以在下方编辑具体的相关属性信息
      ![](/img/xmind/Unity核心_动画/69.png)

  - **动画剪辑属性基本设置**
    - 动画剪辑属性
      ![](/img/xmind/Unity核心_动画/70.png)

      - 动画剪辑名称<br>可编辑修改
        ![](/img/xmind/Unity核心_动画/71.png)

      - 时间轴<br>Start动画剪辑的开始帧<br>End动画剪辑的结束帧<br>我们可以在时间轴中定义每个动画剪辑的帧范围
        ![](/img/xmind/Unity核心_动画/72.png)

      ![](/img/xmind/Unity核心_动画/73.png)

        - **Loop Time：播放动画剪辑时是否循环播放，到结尾时重新开始**
          - **Loop Pose：无缝循环运动**
            - Loop Match：循环匹配
          - Cycle Offset：循环动画在其他时间开始时的周期偏移
        - **Root Transform Rotation：根位置的角度相关**
          - Bake Into Pose：将根旋转烘焙到骨骼移动，禁用此选项将存储为根运动
          - Based Upon：根旋转的基础<br>Original：保持源文件中的原始旋转<br>Root Node Rotation：使用根节点的旋转（仅适用Generic通用动画类型）<br>Body Orientation：保持上半身朝前（仅适用于Humanoid人形动画类型）
          - Offset：根旋转偏移（单位：度）
        - **Root Transform Position（Y）：根垂直位置（Y轴方向）**
          - Bake Into Pose：将垂直根运动烘焙到骨骼移动。禁用此选项将会存储为根运动
          - Based Upon（at Start）：垂直方向根位置的基础<br>Original：保持源文件中的垂直位置<br>Root Node Position：使用垂直根位置（仅适用Generic通用动画类型）<br>Center Of Mass：保持质心与根位置对其（仅适用Humanoid人形动画类型）<br>Feet：保持双脚与根变换位置对齐（仅适用Humanoid人形动画类型）
          - Offset：垂直根位置偏移
        - **Root Transform Position（XZ）：根水平位置（XZ平面）**
          - Bake Into Pose：将水平根运动烘焙到骨骼移动。禁用此选项将会存储为根运动
          - Based Upon：水平根位置的基础<br>Original：保持源文件中的水平位置<br>Root Node Position：使用水平根位置（仅适用Generic通用动画类型）<br>Center Of Mass：保持与根位置对其（仅适用Humanoid人形动画类型）
        - Mirror：在此剪辑中进行左右镜像（仅Humanoid人形动画类型才显示）
        - Additive Reference Pose：启用后可以设置附加动画层基础参考姿势的帧。在时间轴中可以看到蓝色标记<br>附加动画层：在动画控制器（状态机）中可以添加新的动画层<br>Pose Frame：当启用参考姿势帧时，该项就是选择的具体是哪一帧
    - ans = max(ans,1);
  - 动画剪辑属性其它设置
    ![](/img/xmind/Unity核心_动画/74.png)

      - 曲线可以配合Animator作为参数，通过加入曲线值可以利用他标记重要的点<br>可以修改曲线的名字，名字就类似参数名<br>可以通过加减来添加或删除曲线信息
        ![](/img/xmind/Unity核心_动画/75.png)

        - 曲线中的值X轴代表标准化时间（0~1）代表动画的开始和结尾<br>Y轴的值可以根据需求自己设置<br>也可以使用下方提供的预设曲线
          ![](/img/xmind/Unity核心_动画/76.png)

      - 动画事件<br>类似之前我们学习的Animation窗口中的动画事件<br>可以在这里为动画剪辑添加一个事件，当动画播放到事件处时会自动找对象脚本中的同名函数<br>当我们希望在动画某一时刻进行逻辑处理时非常常用<br>比如某一时刻进行伤害判断
        ![](/img/xmind/Unity核心_动画/77.png)

      - 动画遮罩<br>主要作用是当播放该动画时，可以指定哪一部分或者哪些骨骼排除在外不受动作影响<br>Humanoid（人形动画的快捷设置）<br>我们分别可以控制<br>头、左右臂、左右手、左右腿、根等<br>点击他们让他们变成红色，就代表做该动作时不影响该部位<br>Transform（明确指定哪些骨骼关节点不受影响）
        ![](/img/xmind/Unity核心_动画/78.png)

      - 当导入的动画剪辑包含根运动时<br>我们可以在这里手动设置特定骨骼关节点作为我们的根运动节点<br>展开后看到的都是骨骼关节节点
        ![](/img/xmind/Unity核心_动画/79.png)

      - 当我们导入动画出现问题，看到黄色的警告符号时<br>你可以将 Generate Retargeting Quality Report 选中<br>Unity会帮我们生成更多的有关重定向问题的具体信息<br>我们便可以看到具体的一些问题<br>只有看到警告动画不正确时才启用，可以帮助我们排查问题
        ![](/img/xmind/Unity核心_动画/80.png)

  - **预览窗口**
    - 动画预览
      ![](/img/xmind/Unity核心_动画/81.png)

      - 动画剪辑名称
        ![](/img/xmind/Unity核心_动画/82.png)

      - IK：是否开启脚步反向动力学预览<br>2D：2D模式预览<br>箭头：是否显示轴心和质心辅助图标
        ![](/img/xmind/Unity核心_动画/83.png)

      - 切换预览操作的游戏对象
        ![](/img/xmind/Unity核心_动画/84.png)

      - 播放暂停键<br>时间轴（可拖动预览）
        ![](/img/xmind/Unity核心_动画/85.png)

      - 播放速度
        ![](/img/xmind/Unity核心_动画/86.png)

      - 播放状态标记<br>秒、百分比、帧编号显示当前播放到的位置
        ![](/img/xmind/Unity核心_动画/87.png)

      - 可以为资源添加标签Tag
        ![](/img/xmind/Unity核心_动画/88.png)

      - AB包相关设置，AB包知识时会讲解
        ![](/img/xmind/Unity核心_动画/89.png)

- Material页签
  ![](/img/xmind/Unity核心_动画/90.png)

    - Material Creation Mode：<br>定义希望Unity如何为模型生成或导入材质
      ![](/img/xmind/Unity核心_动画/91.png)

      - None：不使用此模型中嵌入的任何材质，改用Unity的默认漫反射材质
      - Standard：导入时，Unity使用默认规则来生成材质
      - Import via MaterialDescription（Experimental）：导入时，Unity使用FBX文件中嵌入的材质描述来生成材质。<br>与Standard相比，该方法结果更准确，并且支持更广泛的材质类型。
    - sRGB Albedo Colors：是否在伽马空间中使用反射率颜色<br>对于使用线性颜色控件的项目，禁用此选项<br>如果上面的选项选择的是<br>Import via MaterialDescription（Experimental）该属性不可用
    - Location：定义如何访问材质和纹理
      ![](/img/xmind/Unity核心_动画/92.png)

      - Use Embedded Materials：将导入的材质保持在导入的资源中
      - Use External Materials（Legacy）：将导入的材质提取为外部资源。旧版材质处理方式，适用于2017.1或更早的Unity版本创建的项目
    - Extract Textures/Materials：当选择Use Embedded Materials后会出现的内容。这两个按钮可以提取导入的资源中嵌入的所有材质和纹理。<br>如果没有需要提取的子资源，这两个按钮会显示为灰色
      ![](/img/xmind/Unity核心_动画/93.png)

    - Naming：定义材质的命名规则
      ![](/img/xmind/Unity核心_动画/94.png)

      - By Base Texture Name：使用导入材质的漫反射纹理名称来命名材质。如果未将漫反射纹理分配给材质，Unity将使用导入材质的名称
      - From Model's Material：使用导入材质的名称来命名材质
      - Model Name + Model's Material：使用模型文件的名称与导入材质的名称相结合来命名材质
    - Search：定义在使用Naming选项定义的名称时查找现有材质的位置规则
      ![](/img/xmind/Unity核心_动画/95.png)

      - Local Materials Folder：在本地Materials材质子文件夹（模型文件所在的同一文件夹）中查找现有材质
      - Recursive-Up：在所有父文件夹（一直向上追溯到Assets文件夹）中所有Materials子文件夹中查找现有材质
      - Project-Wide：在所有Unity项目文件夹中查找现有材质
    - 重新映射的材质<br>如果找到了，Unity会自动关联<br>如果没有找到，我们可以手动进行关联
      ![](/img/xmind/Unity核心_动画/96.png)

### 1.7 3D模型使用

- **3D动画的使用**
  - 将模型拖入场景<br>将模型添加Animator脚本<br>为其创建AnimatorController状态机<br>将想要的动作拖入状态机中<br>编辑状态机<br>代码控制状态切换
  - 状态参数

    如下图所示：

    ![](/img/xmind/Unity核心_动画/97.png)

      - Motion：分配给此状态的动画剪辑
      - Speed：动画的默认速度
      - Multiplier：控制速度的乘数，如果要使用需要勾选的Parameter选中配合的参数float类型
      - Motion Time：运动的时间，如果要使用需要勾选的Parameter选中配合的参数float类型
      - Mirror：是否为状态生成镜像，仅适用于人形动画，如果要配合参数使用选中旁边的Parameter关联参数，参数是bool类型
      - Cycle Offset：循环偏移时间，如果要配合参数使用选中旁边的Parameter关联参数，参数是float类型
      - Foot IK：是否遵循Foot IK，适用于人形人形动画
      - Write Defaults：AnimatorStates 是否为其运动执行未动画化的属性写回默认值。
      - Solo：仅播放该过渡
      - Mute：禁用过渡
      - Solo和Mute如果一起选择，Mute优先执行
      - Add Behaviour：添加状态机行为脚本，之后会专门讲解
  - **连线参数**
    - 动作和动作之间连线
      ![](/img/xmind/Unity核心_动画/98.png)

        - 可以在这里为动画过渡改名，如果不改<br>对应的名字就是<br>"某一状态名"-&gt;"某一状态名"
          ![](/img/xmind/Unity核心_动画/99.png)

        - Has Exit Time：是否有退出时间，如果勾选，当切换动画时，动画一定是播放到下方的Exit Time（百分比）的时间时才过渡到下一个动画
        - Exit Time：退出时间，当选择上方的Has Exit Time时，该值决定了过渡生效的确切时间。该值可以大于1，如果小于1，比如0.85，表示当动画播放到了85%的动画时，就会过渡。如果大于1，比如4.5，那么动画将循环4.5次后过渡到下一个动画
        - Fixed Duration：选中后，下方的Trnaition Duration过渡持续时间将以秒为单位解读过渡时间，如果不选中，则以百分比解读过渡时间
        - Transition Duration(s/%)：过渡持续时间，相当于从该状态切换到下一状态的过渡动画持续的时间，对应下方两个蓝色箭头包裹区域
        - Transition Offset：过渡到目标状态的起始播放的时间偏移。如果是0则从目标状态开头开始播放，如果是0.5则从目标状态的一半开始播放<br>你可以理解为切入下一个状态的切入点
        - Interruption Source：该过渡中断的情况
          ![](/img/xmind/Unity核心_动画/100.png)

          - None：不在添加任何过渡
          - Current State：将当前状态过渡排队
          - Next State：使下一个状态的过渡进行排队
          - Current State Then Next State：将当前状态的过渡和下一个状态的过渡都依次排队
          - Next State Thne Current State：将下一状态的过渡和当前状态的过渡依次排队
        - Ordered Interruption：当前过渡是否可在不考虑顺序的情况下被其它过渡中断<br>选中时，找到有效过渡或当前过渡时，会中断<br>不选中时，找到有效过渡，会中断
        - Conditions：过渡条件<br>如果没有过渡条件，只会考虑Exit Time
    - AnyState和动作之间连线
      ![](/img/xmind/Unity核心_动画/101.png)

        - **Can Transition To self：是否可以过渡到自己**
          - 需要取消勾选防抖
        - Preview source state：预览各种过渡状态<br>可以查看从任意状态切换到当前状态的过渡效果
- **分层动画和遮罩**
  - 分层能够快速实现人物在不同状态有不同动画
  - 遮罩能够减少动画数量，比如人物站立，跑步，蹲下11都要开枪动画，我们可以只做上半身的开枪，然后遮罩给三个时期，节约资源
  - 做法：<br>Layer中点＋新建动画层<br>设置动画层参数<br>设置状态机（结合遮罩是默认为NULL）<br>根据需求创建遮罩
  ![](/img/xmind/Unity核心_动画/102.png)

    - Weight：权重，当动画同时播放时，如果选择的是叠加状态，会根据权重决定叠加的比例
    - **Mask：动画遮罩，该层动画全部都会受该遮罩的影响**
      - Avata Mask在Project创建
    - Blending：混合方式<br>Override：覆盖方式，播放该层动画时忽略其他层信息<br>Additive：叠加方式，会和其它层动画叠加播放
      ![](/img/xmind/Unity核心_动画/103.png)

    - Sync：是否同步其它层<br>主要用于直接从另一个层复制状态过来，在该层中进行修改<br>适用于比如正常状态下有待机走路跑步等等动作，但是受伤状态下动作会改变，可以利用同步层方便我们进行编辑<br>选择后会多一个Source Layer表示你要复制哪一层的状态
      ![](/img/xmind/Unity核心_动画/104.png)

    - Timing：当选中Sync同步其它层时，该参数激活<br>选中，会采用折中方案调整同步层上的动画时长（基于权重计算）<br>不选中，动画时长将使用原始层做为母版
    - IK Pass：反向动力学，之后讲解IK的时候再讲解
  - 代码设置权重

    示例代码如下：

    ```csharp
    animator = this.GetComponent<Animator>();
    animator.SetLayerWeight(animator.GetLayerIndex("Layer名字")，1)；
    ```

- **动画1D混合**
  - 游戏角色通常在两个或多个动画间混合<br>例如混合行走和奔跑动作
  - 在Animator Contorller 窗口 右键-&gt;CreateState -&gt; From New Blend Tree<br>双击点进去
  ![](/img/xmind/Unity核心_动画/105.png)

    - Parameter<br>参数，用于控制混合的参数，在参数列表中的参数
    - 蓝色图像<br>可以在这里控制n个动画的阈值
    - Motion<br>关联的动画列表，可以用鼠标改变顺序
    - Threshold<br>对应动作的临界阈值 当等于这个值时动作权重最大（完全播放该动作）<br>这个值可以完全自由控制，数值范围不定
    - 控制动作的播放速度
      ![](/img/xmind/Unity核心_动画/106.png)

    - 是否镜像动作
      ![](/img/xmind/Unity核心_动画/107.png)

    - Automate Thresholds<br>是否自动设置阈值，它会在取值范围内平均分<br>一般可以取消勾选我们手动控制更准确
    - Compute Thresholds<br>计算阈值的方式<br>会从动画剪辑的根运动中获去数据<br>Speed：速度<br>Velocity X、Y、Z：xyz上的分速度<br>Angular Speed（Rad 、Deg）：角度或者弧度表示的角速度<br>举例：<br>比如你的动画剪辑行走动画时Speed速度是1.5个单位每秒<br>慢跑是2.3个单位每秒，快跑是4个单位每秒，阈值就会根据这些值来进行设置进行混合
      ![](/img/xmind/Unity核心_动画/108.png)

    - Adjust Time Scale<br>调整时间刻度<br>Homogeneous Speed：均匀速度<br>Reset Time Scale：重置时间刻度
      ![](/img/xmind/Unity核心_动画/109.png)

- **动画2D混合**
  - 有两个参数控制动画混合
  - **种类**
    - 2D Simple Directional 2D简单定向模式 运动表示不同方向时候使用，如前后左右走<br>2D Freeform Directional 2D自由形式定向模式 在一个方向还能有多种动作如跑，走<br>2D Freeform Cartesian 2D自由形式笛卡尔坐标11模式 运动不表示不同方向 比如向前走不拐弯 向前跑不拐弯 向前后左拐<br>Direct 直接模式 一般是做表情动作
- **动画子状态机**
  - 在状态机里还有状态机
  - Animator窗口右键  Create Sub State Machine
  - **子状态机和外部的连接方式**
    - 选择状态机 会跑到选择状态机的默认状态<br>选择状态会回到上一层状态的指定状态
- **动画IK控制**
  - 1.在状态机层级开启IK Pass
  ```csharp
  在继承mono类中定义了一个函数OnAnimatorIK
  void OnAnimatorIK(int layerIndex)
      {

      }
  ```

  - **头部IK<br>ani,SetLookAtWeight()**
    - 相关参数
      ![](/img/xmind/Unity核心_动画/110.png)

  - ani.SetLookAtPosition(Vector3)
  - 身体IK
    ![](/img/xmind/Unity核心_动画/111.png)

  - OnAnimatorIK在Update之后LateUpdate之前调用，会在状态机处理完和动画处理完后调用，OnAnimatorIK专门处理Ik在OnAnimatorMove处理动画移动和根运动回调逻辑
- **动画目标匹配**
  - 实现位移自动匹配距离的效果
  - 使用步骤<br>1.找到动作关键点位置信息（起跳点，落地点1，简单理解就是产生位移的动画表现部分）<br>2.将关键信息传入MatchTargetAPI中
  ![](/img/xmind/Unity核心_动画/112.png)

    - 类型:Vector3,Vector3,AvatarTarget枚举， MatchTargetWeightMask（Vector3，float），float，float
    - 目标位置和角度就是结束是的位置角度<br>骨骼位置就是角色哪个部分对其目标点<br>权重就是要对其成什么样<br>开始时机和结束时机就是动画开始位移和结束位移占据动画的百分比位置1
    - 注意<br>1.要开Apply Root Motion即骨骼位移<br>2.必须保证动画已经切换到目标动画，且不能是过渡阶段<br>（将动画匹配写成事件，在动画非过渡状态且还没进入开始百分比是调用）
- **状态机行为脚本**
  - 特殊的脚本，继承指定基类<br>可以为Animator Controller状态机窗口中某状态添加脚本，进行特殊的功能<br>播放声音，特效，检测逻辑
  - 继承StateMachineBehaviour基类
    ![](/img/xmind/Unity核心_动画/113.png)

- 复用状态机
  ```c
  Project窗口 Create->Animator Override Controller;
  上面放入状态机，在每个状态放动画
  ```

### 1.8 角色控制器

主要包括：

- 角色控制器可以让角色受制于碰撞，不会被刚体牵制<br>不加控制器 会在斜坡往下滑，不加约束情况可能被撞飞
- 家了控制器可以不用加刚体<br>可以被碰撞检测。射线检测，触发器检测
- 添加Character Controller

  如下图所示：

  ![](/img/xmind/Unity核心_动画/114.png)

    - Slope Limit<br>坡度度数限制，大于该值的斜坡上不去
    - Step Offset：台阶偏移值，单位为米，低于这个值的台阶才能上去，该值不能大于角色控制器的高度
    - Skin Width：皮肤的宽度，两个碰撞体可以穿透彼此最大的皮肤宽度，较大的值可以减少抖动，较小的值可能导致角色卡住，建议设置为半径的10%
    - MinMoveDistance：最小移动距离，大多数情况下为0，可以用来减少抖动
- 代码相关

  示例代码如下：

  ```csharp
  是否接触地面
  (得到iCharacterController)
  if(cc.isGrounded) // 如果解除了返回true
  //受重力移动
  cc.SimpleMove（Vector3）
  //不受重力移动
  cc.Move（Vector3）
  ```

  ```csharp
  void OnControllerColliderHit(ControllerColliderHit hit)
  {
  }
  //用来检测碰撞
  触发器还是用以前的
  ```
