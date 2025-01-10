---
layout: page
title: 全面VFS
date: 2024-11-28 20:02:44 +0800
mdate: 2024-11-28 20:02:44 +0800
---

# 背景

目前项目使用了 AssetBundle + RawFiles 的形式来打包资源

AssetBundle 有一定的构建规则，会将一部分散资源合并到一起，具体规则在 `dev/client/nshm/BuildConfigure/config.xml` 里

# 分包规则

目前项目有分包规则，把资源分类，主要用来支持：按需下载以及及时清理磁盘占用

目前分为几类：

- 基础包，打进APK里的
- 核心，必须下载，不能删除
- 可选下载，不能删除
- 可选下载，可以删除

目前分包规则比较复杂，有一个配置文件`ResPatchRule.xml`，感觉需要一个简洁的版本

1. 打包侧分的规则：读的配置文件，每个分包单元为DLCVO，具体每个RawFile/AssetBundle可以属于不同的DLCVO
2. Patch: 每个 DLCVO 在配置侧有自己的名字，可以和DLCVO一样，也可以不一样，形成双射 Patch <=> DLCVO
3. 两条配置链，显示用的 一级配置 DLC -> Patch；二级配置 SubDLCGroup -> SubDLC -> Patch
4. 特殊规则，不在界面上显示的可删除 DLC 被归类到“其它”这个 SubDLCGroup 里
5. 表里不能包含所有的 Patch，剩下没归类的每个 Patch 动态分配独立的 SubDLC

上述是规则的简单描述，放到代码里实现有点复杂

- DLC 和 SubDLC 拆了两个概念，多套数据结构，表也是不一样的，但是最后底层又是访问一样的数据
- 虽然分开配置了，但是两者又有耦合 DLC 里的部分数据又会并到 SubDLCGroup 里

PC端上述功能不使用；Android和IOS才使用

# Patch 规则

资源结构为 Manifest + Data

Manifest 记录当前版本下的所有文件以及基本信息（Patch状态，所处位置，下载的时候在哪个子文件内等等）

Data为实际的数据，以VFS或者散文件的形式存在磁盘里，资源管理器会通过 Manifest 找到每个资源的 Data

目前打资源有三种方式

- AppRes：只有 app 这个DLCVO的资源，走VFS合并，带在基础包里的。有一个 gameVersion 标记它的版本
- Patch：全部资源的信息，不走VFS，本地是散的，网站上是合并后的，下载下来需要解压。gameVersion 和 AppRes 匹配，额外有个 PatchVersion 标记版本
- MinorPatch：和 Patch 做比对，包含所有有变动的文件，也是合并下载，本地解压。gameVersion，PatchVersion 和 Patch匹配，额外有个 MinorPatchVersion 标记版本

这里有个可能会影响后续开发的兼容性相关的设计：

AppRes 里资源具体是什么根本不重要，重要的是 gameVersion。由于 Patch 包含了全部资源信息，Patch 又是散的，目前只要能正确拉到 Patch 的 Manifest 就行

PC：gameVersion 最新；AppRes 任意版本；Patch 兼容最新 gameVersion
Android：gameVersion 任意版本；AppRes 和 gameVersion 匹配；Patch 兼容所有 gameVersion
IOS：和 Android 类似，但是可以支持强制换包；Patch 兼容到最近的一个强制包的 gameVersioin

# 痛点分析

目前项目是用极小的文件粒度换来了极为自由的更新方式，因为可以精确到单个文件，完全可以按需下载，也不需要关注当前客户端的资源到底是哪个版本

代价就是 Patch 目录里的文件很松散，会有额外开销（这部分目前手头没有实测数据，可能需要一点支持，不过为了方便后续数据压缩加密，是可以考虑把文件合并的）

## 移动端

目前安卓包数据大小 24G，正常大小，但是目前有一个分包资源清理的功能，看了一下目前的 ResPatchRule 并不能严格限制某个资源一定在某个分包里

## PC端




这样做的好处是：

- 能从任意版本更新到最新
- 粒度细，流量小
- 无用空间可以及时清理

这样做的问题是：

- 粒度太细了，可能会有IO瓶颈（有很多小于1K的文件）
- 不同客户端的情况不一样，需要下载的文件各不相同，不好对资源进行合并

参考了一下其它项目的一些做法：

- 米家的(原神，绝区零)：直接把所有资源按Block划分，Patch就是保证每个Block处于最新，原(平均50MB，应该有极个别资源特殊的所以大小会偏小)，绝区零平均4M一块
- 前司星球重启：全部用VFSPackage，用挂载的方式决定资源具体从哪个文件加载，Patch文件是直接留在本地的

不过这两个都是不支持可选删除资源的，在保证现有功能的前提下，应该在平衡流量和包体的情况下对文件进行合并

目前打包以及下载的时候本来就有合并文件的机制，但是下载完之后会解压回散文件

# DLC





## 配置

配置文件在`ResPatchRule.xml`

- StreamingRule: 基准包规则，分包名字为`streaming`
- KernelRules: DLC规则，分包名字为name属性

规则：

- 支持属性：
  - branch: 分支
  - name: 分包名字，如果是基准包则无效(固定为`streaming`)
  - meargeToStreaming: 这个DLC规则下的资源并入基准包
- 支持规则节点:
  - Tags/Scene/Bundles/RawFiles：按不同节点有不同的资源筛选机制

规则节点：

- Includes：name属性表示 Tag名/场景名/资源路径(前缀)，filter属性表示额外的正则筛选，directlyFolder属性
- Excludes：filter属性表示正则剔除

## 资源 Mapping

ProcedureFilter 可以充当筛选器，也可以充当收集器，如果筛选器继承自 CollectionFilterStrategy 就表示它可以做资源收集（筛选的时候，没收集到的就被筛掉）

收集结果分为带章节数据和不带章节数据

- 章节：`<category>/<sceneName>/chapters/<chapterName>/...`
- 非章节：`<category>/<sceneName>/<customName>/...`

category 资源分类，分包的时候用
sceneName 对应分包规则的Scene节点的名字
chapterName 用来作为分包名字的一部分
customName 为收集器的自定义名字，非章节模式下只用来统计

不同收集器汇总：`All/<sceneName>/<category>/chapters/<chapterName>/...`

- 章节：`All/<sceneName>/<category>/chapters/<chapterName>/...`
- 非章节：`All/<sceneName>/<category>/<customName>/...`

## 收集方式

1. 按规则节点：
  - Scene：筛选出来的场景分到这个分包里，场景所属的分包唯一，归属到优先级最高的分包里（基准包最高，DLC按照xml里的配置顺序）
  - Bundles/RawFiles：筛选出来的资源分到这个分包里
2. 按Tag：
  - ResCollect: Bundles的推广
    - ResourcesStatistics.csv 这个文件记录了一些具体文件的信息，包括场景，等级，任务ID
    - 该Tag支持includeScenes属性，支持配置一些场景名，从上面的csv里筛选对应场景的资源，额外添加到 Bundles 规则节点里
  - LevelSceneRes：Scene的推广
    - 有些场景配了解锁等级
    - 该Tag支持Min和Max两个属性，标记等级范围，解锁等级在范围内的场景会额外添加到 Scene 规则节点里

## 收集步骤

1. root 分支的规则，所有资源
  1. 资源分包唯一
2. 每个带规则的场景的章节资源 category=sgui/controller/bank 归入 core 分支
  1. root 处理过的以 root 为准
  2. 基准包里的资源不能放到 DLC 里
  3. DLC 里的资源可以属于不同的 DLC，分包名`<dlcName>/<chapterName>`
3. core 分支的规则，所有资源
  1. root、core的章节资源，以前述为准
  2. 资源分包唯一
4. 每个带规则的场景的章节资源 category=fasion/vehicle 归入 fasion 分支
  1. root 处理过的以 root 为准
  2. 基准包里的资源不能放到 DLC 里
  3. DLC 里的资源可以属于不同的 DLC，分包名`<dlcName>/<chapterName>`
  4. core 里处理过的依然可以处理（章节/分支规则都可以）
5. 每个带规则的场景的章节资源 category=movie/bank 归入 task 分支
  1. root、core，以前述为准
  2. 基准包里的资源不能放到 DLC 里
  3. DLC 里的资源可以属于不同的 DLC，分包名`<dlcName>/<chapterName>`
  4. fasion 里处理过的依然可以处理
6. 没指定 branch 的规则，下面所有资源，统一归入 trunk 分支
  1. root、core，以前述为准
  2. 资源分包唯一
7. 没规则的场景，下面所有资源归入 trunk 分支
  1. root、core、6里的，以前述为准
  2. 可以属于不同的 DLC，分包名`Scene/<sceneName>`
8. 带规则的 fasion2 场景的章节资源 category=fasion 归入 fasion 分支
  1. ？？？
9. 剩下的，打出来的但是没任何分包规则的资源，分包名`UnknownRes`

```
CloudPatch是啥
GenerateNotInRuleSceneDlc 这个函数没有 CloseChapterMode，规则7里的资源不会并进 trunk 分支
fasion2 是干啥的？？？前面不是跑过一遍了么，还有个bad smell，这里 close 完了上面 trunk 没close的资源会被归进 fashion
```

# 如何做 Patch

1. 客户端修复：Patch备份，删SOPatch，删Patch，删PrePatch
2. SoPatch：基准包里没有，在打Patch的时候这部分分离了，已经有merge file机制，而且需要拷贝到binaryPatch目录生效，不处理
3. Patch：patch+minor

需要处理的机制：

- 覆盖安装，Patch 文件在新包是在基准包里的(hash如果不一样，反正要patch，这里不管)
- 兼容XDelta，如果开了XDelta，要删除的文件备份，否则直接删
- 高低配切换：High/Low分离，高低配文件要直接删
- 新Patch下来，老文件会直接删掉
- 视频单独处理
- 客户端修复：没问题的文件直接拷贝回来
- 边下边玩：部分资源是在需要的时候才下载的，这个时候会下载到PlayingPatch目录里，并且Manifest会标记这个文件是边下边玩的，下一次启动的时候才会并入Patch目录

新Patch

- 覆盖安装，已有 Patch 文件已经进入基准包的要删除
- 新Patch，已有 Patch 文件不存在了，或者文件变动了

- 基准包: VFS + File
- Patch: VFS DLC要支持分包
- MinorPatch：相较于 Patch，变动部分
- XDelta：需要提供Old分支，额外导出xpatch.info

#
