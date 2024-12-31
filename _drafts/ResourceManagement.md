---
layout: page
title: ResourceManagement.md
date: 2024-11-28 20:02:44 +0800
mdate: 2024-11-28 20:02:44 +0800
---

# 相关路径

- patchPath: 指的是运行时可读写的资源目录，用来存放不进包的资源
- resourcePath: TODO
- streamingAssetPath: 指的是只读的资源目录，一般而言，包体相关的信息会放在这里

一般而言，Windows 下 patchPath 推荐放根目录，其它平台就放在各自的 data 目录

特别地，编辑器下有模拟包体加载的需求，所以需要特殊指定上述目录

# 包体相关的配置

## 版本号

配置文件为`<streamingAssetPath>/version.bin`，记录包体的 SVN 版本

## 客户端配置

配置文件为`<streamingAssetPath>/game.json`，主要记录更新相关的内容

- enableUpdater: 是否允许更新，这个配置主要作用是，不过不允许更新，后续下载文件的URL都会是空的
- versionUrls, patchUrls, pkgUrls, reInstallPkgUpdateUrl, SixHorseListUrl: 各类文件的下载地址只有允许更新才会有效
- quickPatchUrls: 内部使用的快速下载 Patch

## 资源配置

配置文件为`<any_path>/build.info`，包体内有一份，各类Patch目录里也有一份。主要记录信息如下：

- ResManifestHeader
  - version 读取器版本，资源的序列化和反序列化依赖这个版本，需要客户端和资源匹配
  - gameVersion 资源对应的包体 SVN 版本(不是资源的版本，是适用的基准包的版本)
  - patchVersion
  - minorPatchVersion
- ResLoadManifestVO
  - bundles/rawfiles 文件描述
  - syncBundles/syncRawFiles 标记这些文件是从包体里复制的

如果 version 不匹配会强制进入修复客户端的流程

# EarliestPatch(EP)

用来热更C#(InjectFix和部分Lua文件)

## 基准包信息

以下信息会在打基准包的时候写入代码内

- patchVersion: 代码版本
- patchListServerIP: 拉取EP文件列表的地址
- patchFileServerIP: 拉取EP文件的地址

## Patch信息

根目录 `<patchPath>/misc_p/`

- misc.txt: 里面记录了与当前EP匹配的基准包代码版本，基准包更新后代码内的 patchVersion 会和这个文件里的值不相等，此时需要重新拉取EP
- misc_l/*: Lua EP
- misc_c/*: C# EP

## 内网挟持

测试的时候需要重定向下载EP的地址

1. 打包的时候额外输出一个文件 `<streamingAssetPath>/local_config.txt`
2. 在所有更新流程结束，正式进入游戏之前把包体内的文件拷贝到 `<patchPath>/misc_p/local_config.txt`
3. version.bin 这个文件用来标记是否需要重新执行上述拷贝
4. 下次启动时会用 `<patchPath>/misc_p/local_config.txt` 里的配置替代 patchListServerIP 和 patchFileServerIP

## 下载

先用 patchListServerIP 去请求文件列表

需要提供

- patchVersion: 基准包代码版本
- 平台: C# 的 InjectFix 需要区分平台

文件列表的每个条目结构如下:

```C#
class PatchInfo {
    string Type;        // misc_l/misc_c 决定是Lua的还是C#的
    string SubType;
    string FileName;    // 文件名
    string RemoteUrl;   // 如果是绝对路径，直接访问；如果是相对路径，域名用 patchFileServerIP
    string Md5;         // 校验本地文件 & 避免重复下载
    string ResVersion;
}
```

# Patch

PC要谨防多开!!!

1. 只允许一个进程执行强制更新的 Patch，其余进程需要等待
2. 只允许一个进程执行预下载的 Patch，其余进程跳过预下载

## 更新记录

配置文件为`<patchPath>/Patch/version.info`，相关版本信息

通过客户端配置内的 versionUrls 获取

最终得到的配置是一个数组，每个条目代表一个更新记录

```C#
class VersionInfo{
    ulong minV; // 起始版本，包含
    ulong maxV; // 结束版本，不包含
    string resV; // <patchVersion>p<minorPatchVersion> 用来检查本地 Patch 的资源配置能不能匹配
    string xResV;
    string resC;
    string xResC;
    string soResC;
    int reInstall = 0; // 0(default) 表示普通更新，1 表示可选换包，2 表示强制换包
    bool activateLogInUpdate = true;

    // 可以覆盖 game.json
    string[] patchUrls;
    string[] pkgUrls;
    string reInstallPkgUpdateUrl;
    string SixHorseListUrl;
    // 可以覆盖 game.json

    bool enableXdeltaPre; // 是否支持差量预下载
    string preResV;
}
```

客户端会根据自身的 gameVersion(来自于 version.bin)去数组里查找合适(`minV <= gameVersion < maxV`)的条目，然后从条目中取具体配置

## PatchInfo

配置文件为`<patchPath>/<Any>Patch/patch.info`，各类 Patch

## SO Patch

资源配置为`<patchPath>/SoPatch/sobuild.info`

PatchInfo为`<patchPath>/SoPatch/SoPatch.info`

生效目录为`<patchPath>/binaryPatch/`

1. 以 VersionInfo 里的 resV 为准，做版本比对，决定是否需要下载 PatchInfo
  - 如果本地不存在资源配置，则必定需要下载
  - 如果本地资源配置的版本(patchVersion+minorPatchVersion)和 VersionInfo 不一致，则需要下载
2. 下载下来的 PatchInfo 和本地资源配置比较
  - 如果本地已经有文件 Patch 过了，会把这些文件的 Patch 状态同步到 PatchInfo
3. 把当前的 PatchInfo 保存为新的资源配置
4. 重新读一遍新的资源配置，并读取配置内的 AB 信息和 rawFile 信息
5. 检查所有状态为 UNKONW 的 rawFile 的 MD5
  - 如果检查不通过，标记未 Patch 状态，需要后续下载
  - 如果检查通过，标记已 Patch 状态
  - 如果发生异常，流程中断
6. 下载上一步校验未通过的文件，下载完成后执行 MD5 检查
7. 文件拷贝 `<patchPath>/SoPatch/AssetsExtra/binaryPatch/*` -> `<patchPath>/binaryPatch/*`
8. 重启游戏

## Patch

资源配置为`<patchPath>/Patch/build.info`

PatchInfo为`<patchPath>/Patch/patch.info`

1. 和 SO Patch 1 一致
2. 删除废弃的 Patch
  - 覆盖安装后，新的基准包里有的资源，要标记为废弃
  - 如果有新 Patch
    - 新 Patch 里没有这个文件，就会标记删除
    - 新 Patch 里有这个文件且这个文件有更新，就会标记删除
  - 如果开了差量更新，需要删除的文件不会被删掉，而是会被复制到 `<patchPath>/DPatch/`
3. 和 SO Patch 2,3,4 一致
4. 资源配置有更新，里面的资源状态可能有变化，重新删除废弃文件
5. 开场视频单独下载并重播

## PrePatch 预下载

资源配置为`<patchPath>/PrePatch/build.info`

PatchInfo为`<patchPath>/PrePatch/patch.info`

## 更新流程

1. 检查本地 Patch 是否损坏(看客户端能否支持 Patch/build.info文件)
2. 修复客户端(如果必要)
3. 初始化
   1. 载入 game.json
   2. 载入包体内的 build.info
4. 拉取更新记录
5. 更新 SO Patch
6. 更新 Patch

目录结构

- <patchPath>/Patch/
  - patch.info
  - build.info
  - version.info 更新记录，用来查询资源版本
- <streamingAssetPath>/
  - game.json 客户端的信息
  - build.info
  - version.bin 基准包的 SVN 版本号，理论上里面的内容和 build.info 里的 gameVersion 一致

# 打包

## 配置

XML格式

- AssetBundleBuild 资源Mapping
  - BuildClass 类名
  - BuildMap 配置文件
- Bundles AB部分
  - StreamingAssets 带进基础包里的
    - Filter
      - Path[]
        - Suffix[] exclude=true/false
        - File[] exclude=true/false
    - Sync
      - Path[]
        - Suffix[] exclude=true/false
        - File[] exclude=true/false
  - Resources 和包体绑定的不更新的资源
    - ... 和 StreamingAssets 一致，但没有 Sync 部分
  - ExtraRes[] name=dlcName 分包用的
    - ... 和 StreamingAssets 一致，但没有 Sync 部分
- RawFiles 普通文件部分
  - ... 和 Bundles 一致
- VFSPaths 需要打VFS的路径，目前只有 StreamingAsset支持
  - File[]
- NumRawPaths 用 Hash 作为目录存放的普通文件
  - File[]
- CompressPaths 要压缩的文件
  - File[]

## 目录结构

- Build/
  - Output/ 这里是最终的打包结果
    - <TargetName>/
      - Log/
      - AppRes/ 基础包信息在这里
      - Patch/ Patch信息在这里，打Patch的时候需要用AppRes里的信息来比对
      - Version.info 版本信息，gameVersion/patchVersion/minorVersion
  - Assets/ 这里是输出的打包好的资源，必定全量
    - <Platform>/
      - Bundles/
        - lowres/
        - Bundles 这是 Unity引擎的 AssetBundleManifest，可以获取AB的依赖等信息
        - Bundles.info 这个是 ResManifestVO 但是里面只有 m_allBundles 和 m_allRawFiles 有意义，别的都是默认值，和 Build.info 里面的内容没实际差别
      - RawFiles
      - Build.info

## 资源构建

资源分为两类，用不同的描述类来表示

- AssetBundle: ABFileInfo
- 普通文件: RawFileInfo

上面两个结构用 ProtoBuf 序列化用来存储打包结果

几个特殊字段

- ResFileStatus mode 标记这个资源是新增/修改/删除
- ResAssetClassify classify 标记资源存储位置 SA/Resource/Patch
- fileVersion 资源版本，其实就是打包的字符串时间戳
- isMinorPatch/isBinaryPatch
- resType/dlcTypes 高低配
- extraNames 这个是用来标记分包的，一个资源可以属于多个分包

ResType: 资源本身区分高低配，一般是在其它地方里有同名文件

- AB: Shader和贴图会自动生成Low版本，生成到 lowres 目录下的同名 AB
- RawFile: LowAssetExtra 里有相对于 AssetExtra 的同名文件(RawFileInfo里记录的还是AssetExtra开头，但是打包的时候会从LowAssetExtra取文件)

DlcType: 根据文件路径决定它属于高配资源还是低配资源还是公共资源

- AB: 包含的所有原始文件路径的DlcType，向上取
- RawFile: 文件本身路径的DlcType

ResType和DlcType需要匹配

```C#
DlcType fileDlcType = getDlcTypeByRule(filePath);

//  不区分高低配的资源
assets[assetName][ResType.High] = { resType = ResType.High, dlcType = fileDlcType };

// 区分高低配的资源
assets[assetName][ResType.High] = { resType = ResType.High, dlcType = DlcType.High }; // fileDlcType 里包含 DlcType.High 才会存在
assets[assetName][ResType.Low] = { resType = ResType.Low, dlcType = DlcType.Low }; // fileDlcType 里包含 DlcType.Low 才会存在
```

### Build.info 缓存

这个文件缓存了资源打包的结果

```C#
class BundlesBuildInfo {
  public DateTime buildTime;
  public Dictionary<string, SortedDictionary<EnumResType, ABFileInfo>> bundles;
  public Dictionary<string, SortedDictionary<EnumResType, RawFileInfo>> rawFiles;
}
```

### 资源Mapping AssetBundleBuild

配置文件为XML格式

- packcfg
  - bundleNodes
    - node path,packType,include/exclude,proceduralFilter
      - rule[] packType,filter,tag
  - rawNodes
    - ... 和 bundleNodes 一致

packType: 打包类型

- file 按文件单独打
- folder 整个目录出一个 AB；如果是 node 里的那目录就是 path；如果是 rule 里的，需要在filter 的正则里自自行加括号标记(这个正则最前面会自动补一个左括号，所以需要在正则里加右括号，按照正则的规则 group1 是AB所在的目录)
- subfolder 每个子目录出一个AB；根目录也要在 filter 的正则里自行加括号标记

include: AssetDatabase.FindAssets 的规则

exclude: 正则

filter: 正则，如果 packType 是 folder/subfolder 的话前面会自动补左括号，在适当的位置自行加右括号，匹配结果的 group1 作为打包目录

### 根据资源Mapping 生成AB引用关系

- 正向引用 assetPath -> (dependingAssetPaths, MapEntry) MapEntry代表这个文件的 Mapping规则(XML里的node节点)，如果多个 Entry 包括了这个路径，则按照遍历顺序以第一个 Entry为准
- 反向引用 assetPath -> depandedAssetPaths
- Shader引用 assetPaths 实际是引用了 Shader 的所有文件路径集合

这一步会根据 node 里的 include 和 exclude 进行路经筛选，不包含 ProcedureFilter

引用关系是 AssetDataBase 指定的引用关系，有以下处理：

- Shader不计入引用关系，但是单独记录所有引用了Shader的文件

### 过滤生成每个文件的 AB 信息 (AssetBundleInfo)

- ProcedureFilter 过滤掉不需要的文件
- AB合并，被且仅被一个文件(A)引用的文件(B)，B文件会被打进A文件所在的AB中
- Shader的变体会被打到Shader本身所在的AB中

### ProcedureFilter

接口 IProceduralFilterStrategy

- CustomFilterStrategy 传入自定义过滤器 Func<string, bool>
- CollectionFilterStrategy
  - 收集器 ProceduralCollector
  - 收集器参数 ProceduralCollectorArg
  - 收集结果 CollectResult
  - 结果变动的事件 Action<CollectResult>

### 合并 AB 信息 AssetBundleItem

```C#
class AssetBundleItem {
  string assetBundleName; // XXX.bundle
  ulong assetBundleChecksum; // assetBundleName 的 Hash，具体计算是扩展了 AssetBundle来的
  List<string> assetNames; // 资源路径
  List<string> addressableNames; // 资源路径（目前和上面的是一回事）
}
```

- 去掉一些文件，配置在 Assets/Res/Common/Configs/bundle_filter_list.json
- 把 Hash 相同给的 AB 合并成一个 AB
- 资源去重，空 AB 移除

### 通用资源描述格式 AssetBuildItem

```C#
class AssetBundleItem {
  bool isAssetBundle; // AB 是 true，普通文件是 false，生成规则是类似的
  string resName;
  ulong resChecksum;
  List<string> assetNames; // 如果是普通资源这里只包含一个文件
  List<string> addressableNames;
}
```

### 构建

AB是魔改的 AssetBundle 看不到，略过，但是最后会生成 AssetBundleManifest 文件，后续要用

保存 BundlesBuildInfo 到路径 `Build/Assets/<Platform>/Build.info`

里面的 ABFileInfo 和 RawFileInfo 不包含分包信息

保存 ResManifestVO 到路径 `Build/Assets/<Platform>/Bundles/Bundles.info` 这个是用 Writer 保存的，运行时反序列化用

里面的数据只有 allBundles(ABFileInfo[]) 和 allRawFiles(RawFileInfo[]) 有意义，并且不包含分包信息

- ABFileInfo 来源于 AssetBundleManifest 里的数据，包括所有 AB 的路径，AB依赖
- RawFileInfo 直接来自于文件本身

## 分包

根据 XML 里的配置把 BundlesBuildInfo 里记录的所有资源做分包

DlcType筛选规则：

- None: 直接通过，但是如果资源同时具有高配信息和低配信息，取的是 ResType == ResType.High 的那个
- High: 取 dlcType != DlcType.Low 的那个(High+Low的也算)
- Low: 取 dlcType == DlcType.Low 的那个(High+Low的不算)

分包规则：

- ALL -> APP + Extra
- APP -> StreamingAssets + Resource
- StreamingAssets
- Resource
- Extra

StreamingAssets/Resource:

按照XML里配置的目录取 ABFileInfo/RawFileInfo 筛选规则为 DlcType.None，赋予 extraName = "app"

Extra:

XML里配置了每个 extraName 的筛选目录，每个资源可能属于多个分包，所以需要合并 extraName 成一个数组

先按 extraName 的目录筛选，app和binaryPatch直接用 DlcType.None 规则，其余的用 DlcType.High 和 DlcType.Low 分别筛选一次

合并 extraName 的时候按照 resType 分开合并

同一份资源只允许出现在 StreamingAssets、Resource、Extra 的其中一个，不允许重复出现

## 构建主包

只包含 StreamingAssets 分包下的资源

默认走 VFS，但是路径里有空格的维持原样。VFS文件：nshm 索引，nshm.xxxx.vfc 数据文件

IOS下 shaderBundle 分包的高配资源也算主包资源

保存 ResManifestVO 结构，有效字段：

- gameVersion
- streamingBundles
- streamingRawFiles
- syncBundles
- syncRawFiles
- dlcsDict 只有 app 且 dlcType 固定 None

保存的 ABFileInfo 和 RawFileInfo 里的 dlcTypes 固定为 EnumDlcType.High | EnumDlcType.Low 比较特殊

ProtoBuf序列化的路径 `Build/Output/<TargetName>/AppRes/Build.info` 给打包用的

MicroInfo序列化的路径 `Build/Output/<TargetName>/AppRes/StreamingAssets/Build.info` 带进包里的

gameversion单独保存到路径 `Build/Output/<TargetName>/AppRes/StreamingAssets/version.bin`

## 构建 Patch

StreamingAssets 分包下的资源，放进 streamingBundles/streamingRawFiles

Extra 分包下的资源，放进 patchBundles/patchRawFiles

保存 ResManifestVO 结构，有效字段：

- gameVersion 和对应的主包 ResManifestVO 的版本一致
- streamingBundles/streamingRawFiles
- syncBundles/syncRawFiles
- patchBundles/patchRawFiles
- dlcsDict app 的 status 是 NotPatched，其余是 Idle。app和binaryPatch的dlcType是None，其余High/Low各一份
