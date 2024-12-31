---
layout: page
title: ClientReview
date: 2024-11-13 15:25:22 +0800
mdate: 2024-11-13 15:25:22 +0800
---

# 启动流程

1. 安卓会找这个文件 <persistantData>/il2cpp.load，如果存在，把文件内容改为文本"200"
2. 初始化 EarliestPatch
3. 执行 C# 的 EarliestPatch
4. 初始化 InitSceneResource [See](#initsceneresource)
5. 初始化 Localization (标记一下客户端所在的地区，供上层逻辑使用，这个标记是硬编码在C#代码里的)
6. 初始化 MonoObject [See](#monoobject)
7. 播闪屏视频 [See](#startvideocontroller)
8. 打开第一个界面 [See](#initui)
9. 安卓包需要等闪屏视频结束
10. 播放背景视频 [See](#initui)
11. 检查网络通不通(到这一步为止都是不需要网络的，EP没网络也不算失败，但是后面的东西就要网络了，所以这里要检查)
  - 阻塞，直到网络恢复前不会执行后续代码
  - 恢复后重新初始化一下 EarliestPatch，并执行 C# 的 EarliestPatch
12. 执行 Patch

# InitSceneResource

用于管理刚进游戏什么也没有的时候需要的资源，包括开场界面，更新界面，相关弹窗等

这部分资源在打包的时候是单独一个 AssetBundle 放在特定路径下，理论上也不做 Patch:

- 资源路径: <Application.dataPath>/Resources/<relative_path>.<ext>
- AssetBundle 路径: <Application.streamingAssetsPath>/bin/Data/initscene.bundle

而这个管理器做的事也仅仅是做一层封装，主要是为了区分编辑器与包体

- 编辑器走 Resource.Load()
- 包体内走 AssetBundle.LoadAsset()

# MonoObject

主要有以下功能:

- 委托启动阶段的所有 Update，包括各种文件下载器以及资源管理
- 管理协程，启动阶段除了入口协程(InitSceneEntry.Start)以外，所有协程都是挂在这个 MonoBehaviour 上的
- IOS 和 Android 在切后台的时候需要额外给 CDN 管理器发通知，特殊处理下

# StartVideoController

闪屏视频管理器，对应的 Object 资源在 InitSceneResource 里

需要注意的问题:

- 播放在 Patch 之前，所有改动下次更新才生效
- Patch 的过程中，视频也能继续播，所以如果本次启动本身就在播放 Patch 后的视频，那这个文件就不能被更新，所以需要创建一份副本来解决冲突问题
- 需要处理副本文件的版本控制

考虑上述问题后，最终流程如下:

1. 额外引入一个 version.bin 文件，放在和视频同级的目录里(这个文件不在 Patch 列表里)
2. 如果 version.bin 存在，则执行一次副本文件的创建；此外，基准包的更新会让副本文件强制失效
3. 播放视频，优先选择副本文件，不存在的话再选择包体内的
4. Patch 结束后，比较副本文件和 Patch 文件的差异(包括新增，删除，修改)，如果有差异，创建 version.bin 文件(以便下次启动进行替换)

# InitUI

这里有个背景视频，需要注意的问题与解决方案和 [StartVideoController](#startvideocontroller) 一致

## 正式启动

这里分两个任务：

- m_CheckSpaceRoutine：检查启动过程中磁盘够不够
- m_UpdateRoutine：执行启动逻辑

因为启动的过程中可能需要下载一些文件，所以需要时刻确认空间是否够如果不够是引导退出游戏级别的

这里的够不够是逻辑值，不是实际的磁盘使用，外部通过设置一个flag标记逻辑上够不够的，flag则是外部读磁盘计算

### 下载锁

PC端有多开问题，可以开多个进程，所以更新文件前要加锁，防止多进程竞争

- 普通资源下载，必须持有下载锁，否则卡住
- 预加载资源下载，持有预下载锁的进程标记为Master，其余进程标记为Slave

- PatchManager (VFSLoader!!! Wrap了GacCore里的接口，这里设置StreamingAssetPath)
- MonoObject（这里怎么又初始化一遍，空跑了，无事发生）
- TcDownloadManager，OnUpdate托管给MonoObject
- FileOperationManager，OnUpdate托管给MonoObject

### PatchManager

- <patchPath>/
  - Patch/
    - bundles/ - AB 资源
    - rawfiles/ - 纯文件 例如开场视频
    - HistoryInstall/
    - patch.info
    - build.info
    - version.json VersionFileList [参见](#VersionFileList)
  - SoPatch/
    - rawfiles/AssetExtra/binaryPatch/
    - sobuild.info
  - OldPatch/
  - PlayingPatch/
  - SyncPlayingPatch/
  - binaryPatch/
  - CloudPatch/
- <streamingAssetPath>/
  - version.bin SVN版本号 TODO，谁的版本号？
  - build.info
  - game.json 客户端的版本信息

#### VersionFileList

记录所有游戏内容的更新信息

信息，在客户端的game.json里会记录取Version的地址，返回的是一个列表，记录每个更新的起始版本和结束版本

```C#
class VersionFileInfo {
  // 灰度测试
  float grayScale;
  string grayHash;
  VersionFileInfo grayInfo;

  ulong minV; // 起始版本
  ulong maxV; // 结束版本
}
```

#### build.info

资源打包的信息，所有资源需要对应的读取器，需要保证资源对应的读取器版本是客户端支持的

- 基础包 <streamingAssetPath>/build.info
- Patch <patchPath>/Patch/build.info
- SOPatch <patchPath>/SoPatch/sobuild.info

如果Patch里的读取器版本客户端不支持，就需要修复客户端（这个修复不重新下载SOPatch）

```
[I4] headerSize 因为patchVersion是个字符串，变长的
[U4] version 读取器版本
[U1] patchStatus
[U8] gameVersion 基准包有version.bin文件，运行时会覆盖掉这里build.info里的值
[St] patchVersion 字符串
[U4] minorPatchVersion
[I4] numAB
[I4] numRaw
[B1] hasApplyModify
```

客户端修复Flag(PatchManager.REPAIR_CLIENT)

- 0 无需修复
- 1 需要修复
- 2 需要修复但是SOPatch不会删除

修复流程：

1. 备份，把所有Patch目录下的文件复制到OldPatch
2. 删除SOPatch下面的所有内容（可以选择不删）
3. 删除Patch下面的所有内容
4. LuaJIT镜像文件（TODO未知）


