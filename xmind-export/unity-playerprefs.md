# unity playerprefs

## 知识点

### 基础

- PlayerPref是unity自带存储读取类
- 存储
  ```csharp
  类似键值对
  键：string
  值：int float string 对应3种api
  ```

  ```csharp
  PlayerPrefs.SetInt("myAge" , 18);
  PlayerPrefs.Setfloat("myHeight" , 180.4f);
  PlayerPrefs.Setstring("myName" , "aaa");
  ```

  - 只能存内存，游戏结束自动存硬盘<br>游戏奔溃或强行关机则不会存储
  ```csharp
  PlayerPrefs.Save( );
  手动存档，防丢
  ```

  - 如果不同类型用同一键名存储 会进行覆盖
- 读取
  - 只要Set了，会查找内存和本地的读取,没有返回默认值
  ```csharp
  int age = PlayerPrefs.GetInt("myAge" , 100); //如果找不到，返回第二个参数为默认值
  ```

  - 判断重复
    - PlayerPrefs.HasKey("MyAge")
    - 用来判断有没有存数据，用来覆盖
- 删除
  - PlayerPrefs.DeleteKey("MyAge");
  - 删所有
    - PlayerPrefs.DeleteAll(  );

### 存储位置

- Win
  - PlayerPrefs 存储在<br>HKCU\\Software\\\[公司名称\]\\\[产品名称\] 项下的注册表中<br>其中公司和产品名称是 在“Project Settings”中设置的名称。
  - win + r运行 regedit<br>HKEY\_CURRENT\_USER<br>SOFTWARE<br>Unity<br>UnityEditor<br>公司名称<br>产品名称
- android
  - /data/data/包名/shared\_prefs/pkg-name.xml
- ios
  - /Library/Preferences/\[应用ID\].plist

## 额外知识点

### 反射小补充

- 如果父类装子类<br>判断一个对象能否为另一个对象分配空间
  - Type a = typeof(类名)；<br>Type b = typeof(类名)；<br>if（a.IsAssignableFrom(b)）
  - 如果a是b的父类，创建b就有a的内容，可以给a分配空间
    ```csharp
    就可以
    A a = Activator.CreateInstance(b) as A;
    用b的快速实例化创建a对象
    ```

- 通过反射获取泛型类型
  ```csharp
  Type type = typeof(List<string>)
  type.GetGenericArguments( );
  得到泛型是什么
  ```
