---
layout: page
title: 研究之美
date: 2019-01-23 15:27:39 +0800
mdate: 2019-12-20 17:24:05 +0800
---

## Before All

**约定** 任意集合$$S$$上的二元关系$$\circ$$左右操作数可以是$$S$$的子集：\\
元素元素：$$ a \circ b $$，保持不变。\\
集合元素：$$A \circ b \Leftrightarrow (A = \varnothing) \lor (\forall a \in A: a \circ b)$$。\\
集合集合：$$A \circ B \Leftrightarrow (A = \varnothing) \lor (B = \varnothing) \lor (\forall a \in A, b \in B: a\circ b)$$。

**定义1** “数”的定义。定义集合$$\mathcal{S}$$，集合内的元素$$x$$满足$$x = (x_L, x_R)$$；其中$$x_L \subset \mathcal{S}$$，$$x_R \subset \mathcal{S}$$，$$x_L \ngeq x_R$$（参考**约定**以及**定义2**）。集合$$\mathcal{S}$$内的元素，称为“数”。

**定义2** “小于等于”的定义。定义$$x \leq y \Leftrightarrow x_L \ngeq y \land y_R \nleq x$$；同时定义$$y \geq x \Leftrightarrow x \leq y$$。其中$$x \in \mathcal{S}$$，$$y \in \mathcal{S}$$。

## Day 1

**定义3** “0”的定义。定义$$0\Leftrightarrow(\varnothing,\varnothing)$$。显然$$0\in\mathcal{S}$$（**定义1**）。

**推论1** $$0\leq{0}$$。

> 证明：\\
> 令$$x = 0$$，$$y = 0$$\\
> 则$$x_L = \varnothing$$，$$y_R = \varnothing$$（**定义3**）\\
> 则$$x_L \ngeq y \land y_R \nleq x$$（**约定**）\\
> 则$$x \leq y$$（**定义2**），即$$ 0 \leq 0$$。

## Day 2

**定义4** “1”和“-1”的定义。定义$$1 \Leftrightarrow (\{0\}, \varnothing)$$，$$-1 \Leftrightarrow (\varnothing, \{0\})$$。显然$$1 \in \mathcal{S}$$，$$-1 \in \mathcal{S}$$（**定义1**）。

**推论2** 任取集合$$\mathcal{S}$$的非空子集$$L$$，$$R$$，令$$x = (L, \varnothing)$$，$$y = (\varnothing, R)$$；则$$x \in \mathcal{S}$$，$$y \in \mathcal{S}$$且$$y \leq x$$。

> 证明：\\
> 由于$$x_L = L$$，$$x_R = \varnothing$$，$$y_L = \varnothing$$，$$y_R = R$$\\
> 则$$x_L \ngeq x_R$$，$$y_L \ngeq y_R$$，$$y_L \ngeq x \land x_R \nleq y$$\\
> 则$$x \in \mathcal{S}$$，$$y \in \mathcal{S}$$（**定义1**），$$y \leq x$$（**定义2**）。

**推论3** $$-1 \lt 0$$，$$0 \lt 1$$，$$-1 \lt 1$$。

> 证明：\\
> 首先$$a \lt b \Leftrightarrow a \leq b \land b \nleq a$$。因而分两部分分开证明\\
> (1.) 左边$$-1 \leq 0$$，$$-1 \leq 1$$，$$0 \leq 1$$（**推论2**）。\\
> \\
> (2.) 右边假设$$0 \leq -1$$\\
> 则$$\varnothing \ngeq -1 \land \{0\} \nleq 0$$（**定义2**），左侧显然成立（**约定**）\\
> 则$$\{0\}\nleq0$$，即$$0 \nleq 0$$，与**推论1**矛盾\\
> 因此$$ 0 \nleq -1$$。\\
> \\
> 综上$$-1 \lt 0$$。同理可得$$0 \lt 1$$，$$-1 \lt 1$$。

## Day 3

**定理1** 自反性。$$\forall{x}\in\mathcal{S}:x\leq x$$。

> 证明：归纳法。\\
> (1.) 初始条件：$$0 \leq 0$$（**推论1**）。\\
> \\
> (2.) 递推假设：$$x \in \mathcal{S}$$满足$$\forall x' \in (x_L \cup x_R): x' \leq x'$$。\\
> \\
> (3.) 归纳：假设$$x \nleq x$$\\
> 则$$\exists x_l \in x_L: x_l \geq x$$或$$\exists x_r \in x_R: x_r \leq x$$（**定义2**）\\
> 则$$\exists x_l \in x_L: x_L \ngeq x_l \land {x_l}_R \nleq x$$或$$\exists x_r \in x_R: {x_r}_L \ngeq x \land x_R \nleq x_r$$（**定义2**）\\
> 则$$\exists x_l \in x_L: x_L \ngeq x_l$$或$$\exists x_r \in x_R: x_R \nleq x_r$$\\
> 则$$\exists x_l \in x_L: \forall x' \in x_L: x' \ngeq x_l$$或$$\exists x_r \in x_R: \forall x' \in x_R: x' \nleq x_r$$（**约定**）\\
> 第一项存在反例$$x' = x_l$$，第二项存在反例$$x' = x_r$$（步骤(2.)条件），与假设矛盾\\
> 因此$$x \leq x$$。\\
> \\
> 综上$$\forall{x}\in\mathcal{S}:x\leq x$$。

**定理2** $$\forall x \in \mathcal{S}: x_L \leq x \land x_R \geq x$$。

> 证明：首先是$$x_L \leq x$$，如果$$x_L = \varnothing$$则显然成立（**约定**），因此只考虑非空情形。\\
> 归纳法。\\
> (1.) 初始条件：$$0_L \leq 0$$（**约定**）。\\
> \\
> (2.) 递推假设：$$\forall x_l \in x_L: {x_l}_L \leq x_l$$。\\
> \\
> (3.) 归纳：假设$$\exists x_l \in x_L: x_l \nleq x$$\\
> 则$$\exists x_l \in x_L: (\exists {x_l}_l \in {x_l}_L: {x_l}_l \geq x) \lor (\exists x_r \in x_R: x_r \leq x_l)$$（**定义2**）\\
> 则$$\exists x_l \in x_L, {x_l}_l \in {x_l}_L: {x_l}_l \geq x$$（**定义1**）\\
> 则$$\exists x_l \in x_L, {x_l}_l \in {x_l}_L: \forall x' \in x_L: x' \ngeq {x_l}_l$$（**定义2**）\\
> 存在反例$$x' = x_l$$（步骤(2.)条件），与假设矛盾\\
> 因此$$x_L \leq x$$。\\
> \\
> 综上$$\forall x \in \mathcal{S}: x_L \leq x$$。同理可得$$\forall x \in \mathcal{S}: x_R\geq{x}$$。

**定理3** 传递性。$$\forall x \in \mathcal{S}, y \in \mathcal{S}, z \in \mathcal{S}, x \leq y, y \leq z: x \leq z$$。

> 证明：记辅助函数$$d(x) = max(d(x_L), d(x_R)) + 1$$，$$d(X) = max(\forall x \in X: d(x))$$。初始条件$$d(\varnothing) = 0$$；因此$$d(x) \geq d(0) = d(\varnothing) + 1 = 1$$。\\
> 反证法。\\
> 假设$$\exists x \in \mathcal{S}, y \in \mathcal{S}, z \in \mathcal{S}, x \leq y, y \leq z: x \nleq z$$；则：\\
> (1) 由$$x \leq y$$可得$$x_L \ngeq y$$（**定义2**）\\
> (2) 由$$y \leq z$$可得$$z_R \nleq y$$（**定义2**）\\
> (3) 由$$x \nleq z$$可得$$\exists i \in x_L: i \geq z$$或$$\exists j \in z_R: j \leq x$$（**定义2**）\\
> (4) 由(1)(3)可得$$i \ngeq y$$；由(2)(3)可得$$j \nleq y$$\\
> (5) 由$$d(x)$$的定义可得$$d(x) \geq d(x_L) + 1 \geq d(i) + 1$$，$$d(z) \geq d(z_R) + 1 \geq d(j) + 1$$\\
> \\
> 综合(1)(2)(3)(4)得到$$y \leq z, z \leq i, y \nleq i$$或$$j \leq x, x \leq y, j \nleq y$$。$$(x, y, z)$$与$$(y, z, i)$$（或$$(j, x, y)$$）具有相同的性质。如果记$$a_n = (x, y, z)$$，$$S_n = d(x) + d(y) + d(z)$$；则$$a_{n + 1} = (y, z, i)$$（或$$a_{n + 1} = (j, x, y)$$），$$S_{n + 1} = d(y) + d(z) + d(i)$$（或$$S_{n + 1} = d(j) + d(x) + d(y)$$）\\
> 则$$S_n \geq S_{n + 1} + 1$$\\
> 则$$\forall k \in \mathcal{Z^+}: S_n \geq S_{n + k} + k$$\\
> 则取$$k = S_n$$（$$S_n \geq 3 d(0) = 3 \gt 0$$）可得$$0 \geq S_{n + k}$$，与$$S_{n + k} \geq 3 d(0) = 3$$矛盾\\
> 因此$$\forall x \in \mathcal{S}, y \in \mathcal{S}, z \in \mathcal{S}, x \leq y, y \leq z: x \leq z$$。

**定理4** 完全性。$$\forall x \in \mathcal{S}, y \in \mathcal{S}, x \nleq y: y \leq x$$。

> 证明：由$$x \nleq y$$可得$$(\exists x_l \in x_L: x_l \geq y) \lor (\exists y_r \in y_R: y_r \leq x)$$（**定义2**）\\
> 由**定理2**可得$$x_l \leq x$$，$$y \leq y_r$$\\
> 由$$y \leq x_l \land x_l \leq x$$可得$$y \leq x$$（**定理3**）\\
> 由$$y \leq y_r \land y_r \leq x$$可得$$y \leq x$$（**定理3**）\\
> 综上$$\forall x \in \mathcal{S}, y \in \mathcal{S}, x \nleq y: y \leq x$$。

**定理4.1** $$\forall x \in \mathcal{S}, y \in \mathcal{S}: x \nleq y \Leftrightarrow y\lt x$$。

> 证明：\\
> 充分性：已知$$x \nleq y$$；由**定理4**可得$$y \leq x$$；则$$y \leq x \land x \nleq y$$，即$$y \lt x$$。\\
> 必要性：已知$$y \lt x$$，即$$y \leq x \land x \nleq y$$；则显然$$x \nleq y$$。

**定理2.1** $$\forall x \in \mathcal{S}: x_L \lt x \land x_R \gt x$$。

> 证明：由**定理1**可得$$x \leq x$$\\
> 则$$x_L \ngeq x \land x_R \nleq x$$（**定义2**）\\
> 因此$$x_L \lt x \land x_R \gt x$$（**定理4.1**）。

**定理3.1** $$\forall x \in \mathcal{S},y \in \mathcal{S},z \in \mathcal{S}, x \lt y, y \leq z: x \lt z$$。

> 证明：反证法。\\
> 假设$$\exists x \in \mathcal{S},y \in \mathcal{S},z \in \mathcal{S}, x \lt y, y \leq z: x \geq z$$\\
> 则$$y \leq x$$（**定理3**）\\
> 则$$x \nless y$$（**定理4.1**），与假设矛盾\\
> 因此$$\forall x \in \mathcal{S},y \in \mathcal{S},z \in \mathcal{S}, x \lt y, y \leq z: x \ngeq z$$\\
> 即$$\forall x \in \mathcal{S},y \in \mathcal{S},z \in \mathcal{S}, x \lt y, y \leq z: x \lt z$$（**定理4.1**）。

**定理3.2** $$\forall x \in \mathcal{S},y \in \mathcal{S},z \in \mathcal{S}, x \leq y, y \lt z: x \lt z$$。

> 证明：同**定理3.1**。

**定义5** 反对称相等定义。定义$$x \equiv y \Leftrightarrow x \leq y \land y\leq x$$（区别于$$=$$）。其中$$x \in \mathcal{S},y \in \mathcal{S}$$。

**定理5** $$\forall x \in \mathcal{S}, Y_L \subset \mathcal{S}, Y_R \subset \mathcal{S}, Y_L \lt x \lt Y_R, z = (x_L \cup Y_L, x_R \cup Y_R): z \equiv x$$。

> 证明：由**定理2.1**可得$$x_L \lt x$$，$$z \lt z_R$$\\
> 则$$x_L \cup Y_L \lt x$$，$$z \lt x_R$$，$$z \lt Y_R$$\\
> 即$$z_L \lt x$$，$$z \lt x_R$$\\
> 则$$z_L \ngeq x$$，$$x_R \nleq z$$（**定理4.1**）\\
> 则$$z \leq x$$（**定义2**），同理$$x \leq z$$\\
> 则$$z \equiv x$$（**定义5**）。

> **定义5**和**定理5**使得任意$$x \in \mathcal{S}$$都可以进行以下化简表示：$$x = (x_L, x_R) \equiv (\{max(x_l)\}, \{min(x_r)\})$$。为方便，写时省略集合符号，即$$(max(x_l), min(x_r))$$，而如果为空集，维持原来表示。

**定理6** 定义一个集合序列$$\mathcal{N_k}$$，$$k \in \mathcal{Z^+}$$。初始$$\mathcal{N_1} = \{0\}$$。递推关系如下：不妨令$$\mathcal{N_k} = \{x_1, x_2, ..., x_m\}$$满足$$x_1 \lt x_2 \lt ... \lt x_m$$；定义集合$$\mathcal{\Delta N_k} = \{x' = (x'_L, x'_R) \| x'_L \subset \mathcal{N_k}, x'_R \subset \mathcal{N_k}, x' \not\equiv \mathcal{N_k}, x'_i \not\equiv x'_j (i \neq j)\}$$；令$$\mathcal{N_{k+1}} = \mathcal{N_k} \cup \mathcal{\Delta N_k}$$。则$$\mathcal{\Delta N_k} = \{(\varnothing, x_1), (x_i, x_{i+1}), (x_m, \varnothing)\}$$，其中$$i \in [1, m - 1]$$。

> 证明：归纳法。\\
> (1.) 初始条件：$$\mathcal{\Delta N_0} = \mathcal{N_1} = \{0\}$$，$$\mathcal{\Delta N_1} = \{(\varnothing, 0),(0, \varnothing)\}$$。\\
> (2.) 递推假设：集合$$\mathcal{N_k} = \{x_1,x_2,...,x_m\} = \bigcup_0^{k - 1} \Delta \mathcal{N_i} $$，且$$x_1 \lt x_2 \lt ... \lt x_m$$，$$\mathcal{\Delta N_i}$$满足定理的结论。\\
> (3.) 归纳：根据**定理5**，得到$$\mathcal{\Delta N_k} \subset \{(x_i, x_j) \| 0 \leq i \lt j \leq m + 1\}$$（左侧空集记为$$x_0$$，右侧空集记为$$x_{m + 1}$$）。\\
> 当$$j - i \geq 2$$时，$$\forall x_l, i \lt l \lt j:(\exists o \lt k:x_l \in \Delta N_o)$$\\
> 利用**定理3**中的辅助函数得到$$d(x_l) = o + 1$$[1]\\
> 取$$x_l = argmin_x(d(x_{i+1}), d(x_{i+2}), ..., d(x_{j-1}))$$\\
> 根据$$\mathcal{\Delta N}$$的定义，$$\forall i, j \geq i: \mathcal{N_i} \cap \mathcal{\Delta N_j} = \varnothing$$\\
> 则$$x_{i+1}, x_{i+2}, ..., x_{l-1} \notin {x_l}_L$$，$$x_{l+1}, x_{l+2}, ..., x_{j-1} \notin {x_l}_R$$\\
> 而$${x_l}_L \lt x_l$$，$${x_l}_R \gt x_l$$\\
> 则$${x_l}_L \leq x_i$$，$${x_l}_R \geq x_j$$\\
> 因此$$(x_i, x_j) \equiv (\{x_i\}\cup {x_l}_L,\{x_j\}\cup {x_l}_R) \equiv x_l$$（**定理8**，$$x_i \lt x_l \lt x_j$$）\\
> 从而$$\mathcal{\Delta N_k} \subset \{(x_i, x_{i+1}) \| 0 \leq i \leq m\}$$\\
> 又因为$$x_0 \lt (x_0, x_1) \lt x_1 \lt (x_1, x_2) \lt x_2 ...$$（**定理2.1**，**定理3**）\\
> 因此$$\mathcal{\Delta N_k} = \{(x_i, x_{i+1}) \| 0 \leq i \leq m\}$$。

> [1]：在递推假设下。$$\forall x_i \in \mathcal{N_k}: d(x_i) = k$$其中$$i$$是奇数（归纳可证），因此$$\forall x \in \mathcal{\Delta N_k}: d(x) = k + 1$$

**定义6** 加法定义。定义$$x + y \Leftrightarrow ((x_L + y) \cup (y_L + x), (x_R + y) \cup (y_R + x))$$。其中$$x \in \mathcal{S}, y \in \mathcal{S}$$。

------------------------

鸽了

**推论4** 加法封闭。$$\forall x \in \mathcal{S}, y \in \mathcal{S}: x + y \in \mathcal{S}$$。

> 证明：

**推论5** $$\forall x \in \mathcal{S}: x + 0 \equiv x$$

> 证明：归纳法。\\
> (1.) 初始条件：$$0 + 0 = 0$$。\\
> (2.) 递推假设：$$\forall x \in \mathcal{S}: x_L + 0 \equiv 0, x_R + 0 \equiv 0$$。\\
> (3.) 归纳：$$x + 0 = (x_L + 0, x_R + 0) \equiv (x_L, x_R) = x$$。

## Day 4

**定义7** 相反数定义。定义$$\forall x \in \mathcal{S}: -x \Leftrightarrow (-x_R, -x_L)$$。（$$-x \in \mathcal{S}$$，归纳可证）。

**定义8** 减法定义。给定$$x,y\in\mathcal{S}$$，$$x-y\Leftrightarrow x+(-y)$$。

**定理7** 加减互逆。$$\forall x,y,z\in\mathcal{S},x+y=z:z-y=x$$。

> 证明：TODO

**推论5.1** $$\forall y\in\mathcal{S}:y=argmin_x(\forall x_i,y_L\lt x_i\lt y_R:d(x_i))$$。

> 证明：令$$argmin_x(\forall x_i,y_L\lt x_i\lt y_R:d(x_i))\equiv x$$，由于$$d(x_L)\lt d(x)$$，因此$$x_L=\varnothing\lor\forall x_l\in x_L:(\exists y_l\in y_L:y_l \geq x_l\lor\exists y_r\in y_R:x_l\geq y_r)$$，而根据已知条件，$$x_L\lt x\lt y_R$$，因此$$x_L=\varnothing\lor\forall x_l\in x_L:(\exists y_l\in y_L:y_l \geq x_l)\Rightarrow\exists y_l\in y_L:y_l \geq x_L\Rightarrow x_L\lt y$$。同理可得$$x_R\gt y$$。因此有$$y=(y_L\cup x_L,y_R\cup x_R)=x$$。

**定理8** $$\forall x\in\mathcal{S},x\gt 0:x+1=(x_L+1,x_R+1)$$。

- **引理8.1** $$\forall x\in\mathcal{S}:x\lt x+1$$。
- > 证明：假设原命题不成立，那么$$\exists x\in\mathcal{S}:x\geq x+1$$，根据定义2，$$\exists x\in\mathcal{S}:{(x+1)}_L\ngeq x$$，根据定义6，$$\exists x\in\mathcal{S}:x\ngeq x$$，这与定理4矛盾，因此假设不成立，原命题成立。
- **引理8.2** $$\forall x\in\mathcal{S},x_L\neq\varnothing:\exists x_l\in x_L:x\leq x_l+1$$
- > 证明：TODO

> 证明：DOTO
