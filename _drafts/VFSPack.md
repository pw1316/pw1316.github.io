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


