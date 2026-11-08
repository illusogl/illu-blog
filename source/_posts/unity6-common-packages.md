---
title: "Unity 6 常用包清单"
date: 2026-11-08 18:20:00
categories:
  - "Unity"
tags:
  - "Unity"
  - "小工具"
---

> 适用版本：Unity 6.6（6000.6.0f1）  ai根据当前项目写的检查列表
> 版本号来源：Unity 6.6 官方 Released Packages 列表  
> 说明：✅ = unity6 3D默认项目已安装；➕ = 未安装但常用

<!-- more -->

---

## 渲染

| 包 ID | 版本 | 说明 | 状态 |
|---|---|---|---|
| com.unity.render-pipelines.universal | 17.6.0 | URP 通用渲染管线 | ✅ |
| com.unity.render-pipelines.high-definition | 17.6.0 | HDRP 高清渲染管线 | ➕ |
| com.unity.shadergraph | 17.6.0 | Shader Graph | ➕ |
| com.unity.visualeffectgraph | 17.6.0 | VFX Graph | ➕ |
| com.unity.postprocessing | 3.5 | 后处理（内置管线用） | ➕ |

## 2D 系列

| 包 ID | 版本 | 说明 | 状态 |
|---|---|---|---|
| com.unity.2d.animation | 16.0 | 2D 骨骼动画（含 2D IK） | ➕ |
| com.unity.2d.spriteshape | 16.0 | Sprite Shape | ➕ |
| com.unity.2d.tilemap.extras | 9.0 | Tile Palette 编辑器、笔刷 | ➕ |
| com.unity.2d.psdimporter | 15.0 | PSD/PSB 导入（骨骼贴图） | ➕ |
| com.unity.2d.aseprite | 6.0 | Aseprite 导入 | ➕ |
| com.unity.2d.pixel-perfect | 6.0 | 像素完美相机 | ➕ |
| com.unity.2d.tooling | 4.0 | 6.6 新增 2D 工具整合包 | ➕ |

## 动画与镜头

| 包 ID | 版本 | 说明 | 状态 |
|---|---|---|---|
| com.unity.timeline | 6.6.0 | Timeline（版本号随编辑器版本，2022 时是 1.8.x） | ✅ |
| com.unity.cinemachine | 3.x | 智能相机 | ➕ |
| com.unity.animation.rigging | 1.4.x | 程序化骨骼绑定 / IK | ➕ |

## AI 与导航

| 包 ID | 版本 | 说明 | 状态 |
|---|---|---|---|
| com.unity.ai.navigation | 2.0 | NavMesh 寻路（NavMeshSurface / NavMeshAgent） | ✅ |
| com.unity.ai.inference | 2.6 | Sentis，本地神经网络推理 | ✅ |
| com.unity.ai.assistant | 2.20 | Unity Assistant 编辑器助手 | ✅ |
| com.unity.behavior | 1.0 | 行为树 | ➕ |
| com.unity.ml-agents | 4.1 | 强化学习 | ➕ |

## 输入与 UI

| 包 ID | 版本 | 说明 | 状态 |
|---|---|---|---|
| com.unity.inputsystem | 1.20 | 新版输入系统 | ✅ |
| com.unity.ugui | 2.6 | uGUI（**TextMeshPro 已并入此包**，不再单独安装） | ✅ |
| com.unity.modules.uielements | 内置 | UI Toolkit（运行时 + 编辑器 UI） | ✅ |

## 多人 / 网络

| 包 ID | 版本 | 说明 | 状态 |
|---|---|---|---|
| com.unity.netcode.gameobjects | 2.x | Netcode for GameObjects（NGO） | ➕ |
| com.unity.transport | 2.x | 底层网络传输（UTP） | ➕ |
| com.unity.multiplayer.tools | 2.2 | 多人调试工具 | ➕ |
| com.unity.services.multiplayer | 2.4 | 官方服务器托管服务 | ➕ |

## XR / AR

| 包 ID | 版本 | 说明 | 状态 |
|---|---|---|---|
| com.unity.xr.arfoundation | 6.6 | AR Foundation | ➕ |
| com.unity.xr.openxr | 1.18 | OpenXR | ➕ |
| com.unity.xr.interaction.toolkit | 3.6 | XR 交互工具包 | ➕ |
| com.unity.xr.hands | 1.9 | 手部追踪 | ➕ |
| com.unity.xr.meta-openxr | 2.6 | Quest 专用 OpenXR | ➕ |

## 工作流 / 编辑器工具

| 包 ID | 版本 | 说明 | 状态 |
|---|---|---|---|
| com.unity.addressables | 4.1 | 资源管理 / 热更 | ➕ |
| com.unity.splines | 2.9 | 样条线工具 | ➕ |
| com.unity.probuilder | 6.1 | 编辑器内建模 | ➕ |
| com.unity.formats.fbx | 5.1 | FBX 导出 | ➕ |
| com.unity.localization | 1.5 | 多语言本地化 | ➕ |
| com.unity.recorder | 5.1 | 录屏 / 录帧 | ➕ |
| com.unity.memoryprofiler | 1.1 | 内存分析 | ➕ |
| com.unity.terrain-tools | 5.3 | 地形笔刷扩展 | ➕ |
| com.unity.test-framework | 1.8 | 测试框架 | ✅ |
| com.unity.visualscripting | 1.9 | 可视化脚本（Bolt） | ✅ |
| com.unity.collab-proxy | 2.13 | Unity Version Control | ✅ |
| com.unity.ide.rider / com.unity.ide.visualstudio | 3.0 / 2.0 | IDE 集成 | ✅ |

## 服务 / 其他常用

| 包 ID | 版本 | 说明 |
|---|---|---|
| com.unity.services.authentication | — | 账号登录 |
| com.unity.services.analytics | — | 数据分析 |
| com.unity.services.cloudsave | — | 云存档 |
| com.unity.mobile.notifications | 2.5 | 移动推送 |
| com.unity.services.vivox | 16.12 | 语音聊天 |
| com.unity.adaptiveperformance | 内置模块 | 自适应性能 |

---

## 备忘

- Unity 6 里 `com.unity.textmeshpro` 已废弃并合并进 `com.unity.ugui`，老项目升级后删除 TMP 单独依赖即可。
- 新项目模板默认自带：AI Navigation、Input System、URP、Timeline、uGUI、Visual Scripting、Unity Version Control。
- 2D IK（`com.unity.2d.ik`）已合并进 `com.unity.2d.animation`，不再单独安装。
- 大多数包可在 Package Manager → **Unity Registry** 直接搜索安装。
- `com.unity.pipeline` 是 Unity Production Pipeline 的**编辑器自动化包**（供 Unity CLI 驱动编辑器），不是渲染管线，别混淆。
- 当前项目 manifest 路径：`Packages/manifest.json`。
