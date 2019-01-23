---
layout: page
title: 研究之美
date: 2019-01-23 15:27:39 +0800
mdate: 2019-01-23 15:27:39 +0800
showbar: false
---

## Before All

**定义1** “数”的定义。“数”构成了集合$$x\in N$$，“数”由两个集合组成$$x\equiv(L,R)$$，这两个集合中的元素也是“数”$$L,R\subset N$$，不存在这样的数$$i,j$$同时满足：$$i\in L$$，$$j\in R$$，$$i\geq j(j\leq i)$$。符合上述定义的元素称为“数”。上述定义简写为$$L\ngeq R$$。

**定义2** “小于等于”的定义。给定两个“数”$$i,j$$，如果既不存在“数”$$k$$同时满足：$$k\in i_L$$，$$k\geq j$$，也不存在“数”$$l$$同时满足$$l\in j_R$$，$$l\leq i$$，则称$$i\leq j(j\geq i)$$。上述定义简写为$$i_L\ngeq j\land j_R\nleq i$$。

## Day 1

**定义3** $$0\equiv(\varnothing,\varnothing)$$。

**定理1** $$0$$是“数”。

> 证明：$$0_L\equiv\varnothing\ngeq\varnothing\equiv0_R$$，因而$$0_L\ngeq 0_R$$，符合定义1

**定理2** $$0\leq 0$$。

> 证明：$$0_L\equiv\varnothing\ngeq 0$$，$$0_R\equiv\varnothing\nleq 0$$，符合定义2

## Day 2

**定义4** $$1\equiv(\{0\},\varnothing)$$，$$-1\equiv(\varnothing,\{0\})$$。

**定理3** $$1$$和$$-1$$都是“数”。

> 证明：对于$$1$$，$$\{0\}\ngeq\varnothing$$；对于$$-1$$，$$\varnothing\ngeq\{0\}$$。两者都符合定义1

**定理4** $$x\equiv(L,\varnothing)$$和$$y\equiv(\varnothing,R)$$都是“数”，且$$y\leq x$$，其中$$L$$，$$R$$为任意“数”集。

> 证明：同定理3

**定理5** $$-1\lt 0$$，$$0\lt 1$$，$$-1\lt 1$$

> 证明：因为$${-1}_L\equiv\varnothing\ngeq 0$$，$$0_R\equiv\varnothing\nleq -1$$，符合定义2，因而$$-1\leq 0$$；又因为根据定理2，$$-1_R\equiv\{0\}\geq 0$$，因而$$0\nleq -1$$。综上所述，$$-1\lt 0$$。同理可得$$0\lt 1$$。而根据以上结果，$$1_L\equiv\{0\}\geq -1$$，不符合定义2，因而$$1\nleq-1$$，所以有$$-1\lt 1$$。

## Day 3

**定理6** 如果$$x,y,z$$都是“数”，且$$x\leq y$$，$$y\leq z$$，则$$x\leq z$$

> 证明：假设存在三个“数”$$x,y,z$$，满足$$x\leq y$$，$$y\leq z$$，$$x\nleq z$$，根据定义2，可以得到：$$x_L\ngeq y$$，$$y_R\nleq x$$，$$y_L\ngeq z$$，$$z_R\nleq y$$，$$\exists i\in x_L:i\geq z\lor\exists j\in z_R:j\leq x$$。对于最后一个条件，存在两种情况，如果是前者，则得到$$y\leq z$$，$$z\leq i$$，$$y\nleq i$$，于是$$y,z,i$$必满足和$$x,y,z$$一样的性质，同理第二种情况下可以得到新的三个“数”$$j,x,y$$。记$$d(x)$$表示“数”$$x$$内包含的空集数量，$$d(X)$$表示集合$$X$$内的空集数量（如果$$X$$本身就是空集，记为$$1$$）.