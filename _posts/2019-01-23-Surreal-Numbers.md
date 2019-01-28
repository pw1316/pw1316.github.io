---
layout: page
title: 研究之美
date: 2019-01-23 15:27:39 +0800
mdate: 2019-01-29 00:03:05 +0800
showbar: false
---

## Before All

**约定** 二元关系的其中一端为集合时，为真的条件包括集合为空。即$$A \circ b\Leftrightarrow A=\varnothing\lor(\forall a\in A:a\circ b)$$，$$A\circ B\Leftrightarrow A=\varnothing\lor B=\varnothing\lor(\forall a\in A,b\in B:a\circ b)$$。

**定义1** “数”的定义。“数”$$x$$构成了集合$$\mathcal{S}$$，“数”由两个集合组成$$x\Leftrightarrow(x_L,x_R)$$，这两个集合中的元素也是“数”$$x_L,x_R\subset \mathcal{S}$$，并且满足$$\nexists i,j:i\in x_L\land j\in x_R\land i\geq j$$，即$$x\in \mathcal{S}\Leftrightarrow x_L\ngeq x_R$$。

**定义2** “小于等于”的定义。给定$$i,j\in\mathcal{S}$$，如果$$(\nexists k\in i_L:k\geq j)\land(\nexists l\in j_R:l\leq i)$$，则称$$i\leq j$$（或$$j\geq i$$），即$$i\leq j\Leftrightarrow i_L\ngeq j\land j_R\nleq i$$。

## Day 1

**定义3** 初始“数”的定义。$$0\Leftrightarrow(\varnothing,\varnothing)$$。$$0_L\ngeq 0_R$$符合定义1，因此$$0$$是一个数。

**定理1** $$0\leq 0$$。

> 证明：$$0_L\ngeq 0$$，$$0_R\nleq 0$$，根据定义2即可证明。

## Day 2

**定义4** 第二日新增“数”的定义。$$1\Leftrightarrow(\{0\},\varnothing)$$，$$-1\Leftrightarrow(\varnothing,\{0\})$$。$$1_L\ngeq 1_R,-1_L\ngeq -1_R$$，符合定义1，因此$$1,-1$$均是数。

**定理2** 给定$$x\equiv(L,\varnothing),y\equiv(\varnothing,R)$$，则$$x,y\in\mathcal{S}$$，且$$y\leq x$$。

> 证明：$$x_L\ngeq x_R,y_L\ngeq y_R$$，且$$y_L \ngeq x,x_R\nleq y$$根据定义1和定义2即可证明。

**定理3** $$-1\lt0,0\lt1,-1\lt1$$。

> 证明：根据定理2可得$$-1\leq0,-1\leq1,0\leq1$$。根据定理1，$$0\geq 0$$，而$$0\in -1_R$$，因此$$0\nleq -1$$，因此$$-1\lt 0$$。同理可得$$0\lt 1$$。再根据上述已知结果$$0\geq-1$$，而$$0\in1_L$$，因此$$0\nleq -1$$，因此$$-1\lt1$$。

## Day 3

**定理4** 自反性。$$\forall x\in\mathcal{S}:x\leq x$$。

> 证明：归纳法。(1.)$$0\leq 0$$。(2.)假设$$x\in\mathcal{S}$$满足$$x_L=\varnothing\lor\forall x_l\in x_L:x_l\leq x_l$$且$$x_R=\varnothing\lor\forall x_r\in x_R:x_r\leq x_r$$。如果$$x\nleq x$$，则$$\exists x_l\in x_L:x_l\geq x$$或$$\exists x_r\in x_R:x_r\leq x$$。如果前者成立，则$$x_L\neq\varnothing\land x_L\ngeq x_l$$，与假设矛盾；同理如果后者成立也与假设矛盾，因此$$x\leq x$$。

**定理5** $$\forall x\in\mathcal{S}:x_L\leq x\land x_R\geq x$$。

> 证明：归纳法。(1.)$$0_L\leq0\land0_R\geq0$$(2.)由于$$x_L=\varnothing$$时显然有$$x_L\leq x$$，$$x_R=\varnothing$$时显然有$$x_R\geq x$$，因此只考虑非空的情况。假设$$x\in\mathcal{S}$$满足$$\forall x_l\in x_L:({x_l}_L\leq x_l\land{x_l}_R\geq x_l)$$且$$\forall x_r\in x_R:({x_r}_L\leq x_r\land{x_r}_R\geq x_r)$$。如果$$x_L\nleq x$$，则$$\exists x_l\in x_L:x_l\nleq x$$，则$$\exists {x_l}_l\in {x_l}_L:{x_l}_l\geq x$$或$$\exists x_r\in x_R:x_r\leq x_l$$。由于$$x\in\mathcal{S}\Leftrightarrow x_L\ngeq x_R$$，因此$$x_L\nleq x\Rightarrow\exists {x_l}_l\in {x_l}_L:{x_l}_l\geq x\Rightarrow\exists {x_l}_l\in {x_l}_L:x_L\ngeq {x_l}_l$$，这和假设矛盾，因此$$x_L\leq x$$。同理$$x_R\geq x$$。

**定理6** 传递性。$$\forall x,y,z\in\mathcal{S},x\leq y,y\leq z:x\leq z$$。

> 证明：定义1和定义3说明所有“数”都是基于$$0$$递归创造出来的，假设每天会使用已知“数”组合作为左右集创造新“数”，记$$d(x)$$表示$$x$$是在第几天被创造出来的，记$$d(X)=max(\forall x\in X:d(x))$$（$$d(\varnothing)=0$$），于是有$$d(x)=max(d(x_L),d(x_R))+1$$。显然有$$d(x)\geq1$$以及$$\forall i\in x_L\lor i\in x_R:d(i)+1\lt d(x)$$。回到原命题，假设原命题不成立，即$$\exists x,y,z\in\mathcal{S},x\leq y,y\leq z:x\nleq z$$，则$$\exists i\in x_L:i\geq z\lor\exists j\in z_R:j\leq x$$，如果前者成立，则$$\exists i\in x_L,y\leq z,z\leq i:y\nleq i$$；同理，如果后者成立，则$$\exists j\in z_R,j\leq x,x\leq y:j\nleq y$$。可以看出无论是$$y,z,i$$，还是$$j,x,y$$，都拥有和$$x,y,z$$相同的性质，因此可以继续重复上述步骤。根据$$d(x)$$的性质，有$$d(x)+d(y)+d(z)\geq d(y)+d(z)+d(i)+1$$，且$$d(x)+d(y)+d(z)\geq d(j)+1+d(x)+d(y)$$，因此可以得到一个递推式：$$S_n\geq S_{n+1}+1$$，其中$$S_n=d(x_n)+d(y_n)+d(z_n)$$且满足$$x_n\leq y_n,y_n\leq z_n,x_n\nleq z_n$$。上述递推式具有更一般的形式$$S_n\geq S_{n+k}+k$$，若$$S_n=M$$，取$$k=M$$，得$$S_{n+M}\leq 0$$。注意到$$d(x)\geq 1$$，因此$$S_{n+M}\geq 3$$，存在矛盾，所以最初的假设不成立，原命题成立。

**定理7** 完全性。$$\forall x,y\in\mathcal{S},x\nleq y:y\leq x$$。

> 证明：假设原命题不成立，即$$\exists x,y\in\mathcal{S},x\nleq y:y\nleq x$$，则利用定义2，有$$\exists x,y\in\mathcal{S},((\exists x_l\in x_L:x_l\geq y)\lor(\exists y_r\in y_R:y_r\leq x)):y\nleq x$$。利用定理6，有$$\exists x,y\in\mathcal{S}:((\exists x_l\in x_L:x_l\nleq x)\lor(\exists y_r\in y_R:y_r\ngeq y))$$。这与定理5矛盾，因此假设不成立，原命题成立。

**推论7.1** $$\forall x,y\in\mathcal{S}:x\nleq y\Leftrightarrow y\lt x$$。

> 证明：已知$$y\leq x\land x\nleq y\Leftrightarrow y\lt x$$，定理7说明$$x\nleq y$$蕴含$$y\leq x$$，因此$$x\nleq y\Leftrightarrow y\lt x$$。

**推论5.1** $$\forall x\in\mathcal{S}:x_L\lt x\land x_R\gt x$$。

> 证明：定理4表明$$x_L\ngeq x$$，$$x_R\nleq x$$，利用推论7.1即可证明。

**推论6.1** $$\forall x,y,z\in\mathcal{S},x\lt y,y\leq z:x\lt z$$。

> 证明：假设$$\exists x,y,z\in\mathcal{S},x\lt y,y\leq z:x\geq z$$，根据定理6，有$$y\leq x$$这与已知条件$$x\lt y$$矛盾，因此假设不成立，原命题成立。

**推论6.2** $$\forall x,y,z\in\mathcal{S},x\leq y,y\lt z:x\lt z$$。

> 证明：同推论6.1

**定义5** 反对称性。给定$$x,y\in\mathcal{S}$$，$$x=y\Leftrightarrow x\leq y\land y\leq x$$。这表示$$x$$和$$y$$替换使用时不会改变结果，但是两者不一定相等。

**定理8** 给定$$x\in\mathcal{S}$$，任取$$Y_L,Y_R\subset\mathcal{S}$$满足$$Y_L\lt x\lt Y_R$$，令$$z\equiv(x_L\cup Y_L,x_R\cup Y_R)$$，则有$$z=x$$。

> 证明：根据推论5.1，$$x_L\lt x\land z\lt z_R$$，因此有$$x_L\cup Y_L\lt x\land z\lt x_R$$，因此$$z\leq x$$。同理可得$$x\leq z$$，由定义5可知$$x=z$$。

**定理9** 给定集合$$N\subset\mathcal{S}$$，满足$$N=\{x_1,x_2,...,x_m\}$$，且$$x_1\lt x_2\lt...\lt x_m$$，表示某天一共存在的两两相异的“数”，则在下一天仅会新创造以下$$m+1$$个两两相异的“数”$$x'$$满足$$\forall x\in N:x'\neq x$$，且这些新“数”组成的集合$$\Delta N=\{(\varnothing,\{x_1\})\}\cup\{(\{x_i\},\{x_{i+1}\})\|1\leq i\leq m-1\}\cup\{(\{x_m\},\varnothing)\}$$。

> 证明：归纳法。(1.)$$N_1=\{0\}$$，$$\Delta N_0=\{(\varnothing,\{0\}),(\{0\},\varnothing)\}$$。(2.)假设集合$$N_k=\{x_1,x_2,...,x_m\}$$是从$$N_1$$开始按照命题条件创造的，且$$x_1\lt x_2\lt...\lt x_m$$。根据定理8，$$(x_L,x_R)=(\{max(x_l)\},\{min(x_r)\})$$，因此$$\Delta N_k=\{(\varnothing,\{x_i\})\}\cup\{(\{x_i\},\{x_j\})\|i\lt j\}\cup\{(x_i,\varnothing)\}$$。为了方便，记$$\varnothing\rightarrow\{x_0\}$$，$$\varnothing\rightarrow\{x_{m+1}\}$$，于是，$$\Delta N_k=\{(\{x_i\},\{x_j\})\|0\leq i\lt j\leq m+1\}$$。当$$j-i\geq2$$时，考虑“数”列$$x_{i+1},x_{i+2},...,x_{j-1}$$，根据假设它们必然是在某一天被创造的：$$\forall x_l,i\lt l\lt j:(\exists!o\lt k:x_l\in \Delta N_o)$$（$$\Delta N_0=N_1$$），因此$$d(x_l)=o+1$$。取$$x_l\equiv argmin_x(d(x_{i+1}),d(x_{i+2}),...,d(x_{j-1}))$$。根据假设，如果$$d(x_i)\leq d(x_j)$$，那么$$x_i$$的创造时间一定比$$x_j$$早，那么$$x_i$$的左右集都不会递归地包含$$x_j$$，因此$$x_{i+1},x_{i+2},...,x_{l-1}\notin{x_l}_L$$。又因为$${x_l}_L\lt x_l$$，因此$${x_l}_L\leq x_i$$。同理$${x_l}_R\geq x_j$$。根据定理8，$$(\{x_i\},\{x_j\})=(\{x_i\}\cup {x_l}_L,\{x_j\}\cup {x_l}_R)=({x_l}_L,{x_l}_R)\equiv x_l$$。注意到当$$i=0$$或$$j=m+1$$时，$$x_l\leq\varnothing$$以及$$x_l\geq\varnothing$$依然成立。上述证明还说明了符合条件的$$x_l$$是唯一的，否则就有$$(\{x_i\},\{x_j\})\lt(\{x_i\},\{x_j\})$$，而这是不成立的。因此$$\Delta N_k=\{(\{x_i\},\{x_{i+1}\})\|0\leq i\leq m\}$$。

定理9说明了新“数”只会出现在两端或两相邻“数”之间，第$$k$$天会产生$$2^{k-1}$$个新“数”。

**定义6** 加法定义。给定$$x,y\in\mathcal{S}$$，$$x+y\Leftrightarrow((x_L+y)\cup (y_L+x),(x_R+y)\cup (y_R+x))$$

**定理10** $$\forall x\in\mathcal{S}:x+0=x$$

> 证明：归纳法。(1.)$$0+0=0$$，(2.)$$x+0=(x_L+0,x_R+0)$$。

## Day 4

**定义7** 相反数定义。给定$$x\in\mathcal{S}$$，$$-x\Leftrightarrow(-x_L,-x_R)$$。

**定义8** 减法定义。给定$$x,y\in\mathcal{S}$$，$$x-y\Leftrightarrow x+(-y)$$。

**定理11** 加减互逆。$$\forall x,y\in\mathcal{S},x+y=z:z-y=x$$。

> 证明：TODO

**推论8.1** 给定“数”$$x\equiv(L,R)$$，取“数”$$x\equiv argmin(\forall x_i,y_L\ngeq x_i\ngeq y_R:d(x_i))$$，则$$x=y$$

> 证明：TODO
