---
layout: page
title: UnityEcs
date: 2024-08-26 17:19:51 +0800
mdate: 2024-08-26 17:19:51 +0800
---

# 1 World

## 1.1 System

继承自 ComponentSystemBase

```
ComponentSystemGroup -> ComponentSystem -> ComponentSystemBase
JobComponentSystem-> ComponentSystemBase
SystemBase -> ComponentSystemBase
```

整体两类：Group(ComponentSystemGroup) 和 System(ComponentSystem/JobComponentSystem/SystemBase)

Group用来当作ComponentSystemBase的容器；System用来实现功能

三个特殊的Group：InitializationSystemGroup/SimulationSystemGroup/PresentationSystemGroup

这三个Group会被添加到引擎的PlayerLoop里，对应Unity的几个生命周期：

- InitializationSystemGroup 对应 Initialization
- SimulationSystemGroup 对应 Update
- PresentationSystemGroup 对应 PreLateUpdate
