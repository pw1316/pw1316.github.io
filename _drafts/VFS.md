---
layout: page
title: VFS.md
date: 2024-11-28 20:02:44 +0800
mdate: 2024-11-28 20:02:44 +0800
---

# 分块

文件存储最小单位 1K 作为一块，文件的占用只能是整数个块

# 结构

- xxx.idx 索引部分
- xxx.i.part 拆 part 存储实际内容

# 索引

1. 分了几个part
2. 一共有多少文件
3. 所有文件的元信息

## 文件描述

记录元信息

- 在哪个 part 里
- 内容起始块索引
- 文件名有多大
- 文件内容有多大
- 文件名 (Hash or index)

- 边下边玩？A资源正在使用中，被更新了
- 资源依赖
- 资源归属：首包(SA)、分包1(Patch)，分包2(Patch)
- 覆盖安装（强更）：首包资源更新，如何最小限度处理分包资源
- 覆盖安装（非强更）：老包和新包不同的处理Patch方式保证一致
- 普通更新

加载资源？
发起调用-> new TaskOp -> find Task? Create -> BundleTask? Dep BundleTask? -> FileTask -> SA(VFS)/Resource/Patch
异步
FileTaskDone -> BundleTaskDone -> Asset
异步
AssetLoaded -> TaskDone -> TaskOpDone

加载普通文件？
CoreChunkUncompressHelperNative -> SA(VFS)/Resource/Patch -> buffer

EnumResType.High/Low 这个资源在打包的时候可能会产生对应的Low版本
EnumDlcType.High/Low/None 这个资源本身是属于高配还是低配还是公共

==========

ABBuildInfo: -> build.info
构建时间
bundleName->resType(High/Low)->ABFileInfo
rawFileName->resType(High/Low)->RawFileInfo
assetPath->AssetFileInfo?


ResVersion -> nowTime精确到ms

# 引用关系

Shader引用不算常规引用，单独记录引用了Shader的资源(不区分引用了哪个Shader)

- BuildMap:
  - path->(dependingPaths, filteredByEntry) 唯一，如果相同路径被不同的Entry包含了，算在第一次访问的Entry里
- BuildReverseMap:
  - path->dependedPaths
- ShaderRefMap:
  - paths

# AB合并

- 如果某个资源assetA只被单一assetB引用，并且被引用的资源会进包，那assetB会被合并到assetA的bundle里(assetA可能也是某个资源的唯一引用，继续往下找)
- Shader的变体和Shader打到一起

BuildMap转AssetBundleInfo
Entry里有规则Rules，根据规则，决定tag，packType(按文件or按目录打包)
- AssetBundleInfo
  - tag,packType
  - assetBundleName 名字

构建反向引用
AssetBundleInfo->assetPaths

删除不进包的资源(Assets/Res/Common/Configs/bundle_filter_list.json)

构建 AssetBundleItem

- assetBundleName XXX.bundle
- assetNames : 资源路径
- addressableNames: 资源路径（不知道和上面的有什么区别，目前就是个Copy）
- assetBundleChecksum: assetBundleName的Hash(AssetBundle的接口，扩展的)

AB合并 assetBundleChecksum 相同的AB，把资源合到一起；然后移除不包含资源的AB

移除重复的资源？会有么

构建 AssetBuildItem

- isAssetBundle
- resName
- resChecksum
- assetNames : 资源路径
- addressableNames: 资源路径（不知道和上面的有什么区别，目前就是个Copy）

构建引擎结构 AssetBundleBuild

- LowRes
- 多语言 ForceRebuild
- bundleName->ResType->ABFileInfo

ResType打Bundle的时候是否有生成对应的Low版本（LowShader，贴图会有MipMapStrip）
DlcType决定Bundle里所有的资源的原始路径是High还是Low还是公共(所有路径取并集)

ResType需要和DlcType匹配

- 如果DlcType是High，那么删掉ResType=Low的Info
- 如果DlcType是Low，那么删掉ResType=High的Info
- 如果属于公共的，那么ResType=High

主Patch MinorPatch

patchVersion是打patch的时间戳