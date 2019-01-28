---
layout: page
title: 研究之美
date: 2019-01-23 15:27:39 +0800
mdate: 2019-01-28 20:51:31 +0800
showbar: false
---

## Before All

**约定** 二元关系的其中一端为集合时，为真的条件包括集合为空。即$$A \circ b\Leftrightarrow A=\varnothing\lor(\forall a\in A:a\circ b)$$，$$A\circ B\Leftrightarrow A=\varnothing\lor B=\varnothing\lor(\forall a\in A,b\in B:a\circ b)$$。

**定义1** “数”的定义。“数”$$x$$构成了集合$$\mathcal{S}$$，“数”由两个集合组成$$x\Leftrightarrow(x_L,x_R)$$，这两个集合中的元素也是“数”$$x_L,x_R\subset \mathcal{S}$$，并且满足$$\nexists i,j:i\in x_L\land j\in x_R\land i\geq j$$，即$$x\in \mathcal{S}\Leftrightarrow x_L\ngeq x_R$$。

**定义2** “小于等于”的定义。给定两个“数”$$i,j$$，如果$$(\nexists k\in i_L:k\geq j)\land(\nexists l\in j_R:l\leq i)$$，则称$$i\leq j$$（或$$j\geq i$$），即$$i\leq j\Leftrightarrow i_L\ngeq j\land j_R\nleq i$$。

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

**定理4** $$\forall x\in\mathcal{S}:x\leq x$$。

> 证明：归纳法。(1.)$$0\leq 0$$。(2.)假设$$x\in\mathcal{S}$$满足$$x_L=\varnothing\lor\forall x_l\in x_L:x_l\leq x_l$$且$$x_R=\varnothing\lor\forall x_r\in x_R:x_r\leq x_r$$。如果$$x\nleq x$$，则$$\exists x_l\in x_L:x_l\geq x$$或$$\exists x_r\in x_R:x_r\leq x$$。如果前者成立，则$$x_L\neq\varnothing\land x_L\ngeq x_l$$，与假设矛盾；同理如果后者成立也与假设矛盾，因此$$x\leq x$$。

**定理5** $$\forall x\in\mathcal{S}:x_L\leq x\land x_R\geq x$$。

> 证明：归纳法。(1.)$$0_L\leq0\land0_R\geq0$$(2.)假设$$x\in\mathcal{S}$$满足$$x_L=\varnothing\lor\forall x_l\in x_L:({x_l}_L\leq x_l\land{x_l}_R\geq x_l)$$且$$x_R=\varnothing\lor\forall x_r\in x_R:({x_r}_L\leq x_r\land{x_r}_R\geq x_r)$$。TODO已知$$x_L$$非空，且$$\forall x_l\in x_L,x_{lL}\neq\varnothing,x_{ll}\in x_{lL}:x_{ll}\leq x_l$$，那么首先$$x$$是个“数”，根据定义1得到$$\forall x_l\in x_L:x_R\nleq x_l$$。其次，如果$$x_{lL}$$为空，则$$\varnothing\ngeq x$$，因而根据定义2有$$\forall x_l\in x_L:x_l\leq x$$；如果$$x_{lL}$$非空，假设$$\exists x_l\in x_L:x_l\nleq x$$，那么定义2的两个条件$$x_{lL}\ngeq x$$，$$x_R\nleq x_l$$至少有一个不满足，但是由于第二个条件必然成立，所以可以得到$$\exists x_l\in x_L,x_{ll}\in x_{lL}:x_{ll}\geq x$$，再根据定义2，$$\exists x_l\in x_L,x_{ll}\in x_{lL}:x_L\ngeq x_{ll}$$，这与前提条件$$x_{ll}\leq x_l$$矛盾，假设不成立，因此$$\forall x_l\in x_L:x_l\leq x$$。由(1.)和(2.)归纳可得$$\forall x_l\in x_L:x_l\leq x$$；同理，$$\forall x_r\in x_R:x_r\geq x$$。

**定理8** 如果$$x,y,z$$都是“数”，且$$x\leq y$$，$$y\leq z$$，则$$x\leq z$$

> 证明：假设存在三个“数”$$x,y,z$$，满足$$x\leq y$$，$$y\leq z$$，$$x\nleq z$$，根据定义2，可以得到：$$x_L\ngeq y$$，$$y_R\nleq x$$，$$y_L\ngeq z$$，$$z_R\nleq y$$，$$\exists i\in x_L:i\geq z\lor\exists j\in z_R:j\leq x$$。对于最后一个条件，存在两种情况，如果是前者，则得到$$y\leq z$$，$$z\leq i$$，$$y\nleq i$$，于是$$y,z,i$$必满足和$$x,y,z$$一样的性质，同理第二种情况下可以得到新的三个“数”$$j,x,y$$。记$$d(x)=max(\max_l(d(x_l)),max_r(d(x_r)))+1$$，因此$$\forall x_l\in x_L:d(x_l)\leq d(x)-1$$，$$\forall x_r\in x_R:d(x_r)\leq d(x)-1$$。代入上面三个“数”得到$$d(x)+d(y)+d(z)\geq d(y)+d(z)+d(i)+1$$，$$d(x)+d(y)+d(z)\geq d(j)+d(x)+d(y)+1$$，而$$y,z,i$$或$$j,x,y$$又可以重复上述方式得到新的三个“数”。因此更一般地，$$d(x)+d(y)+d(z)\geq d(a)+d(b)+d(c)+k$$，其中$$x\leq y$$，$$y\leq z$$，$$x\nleq z$$，$$a\leq b$$，$$b\leq c$$，$$a\nleq c$$，$$k$$为任意整数。注意到$$min(d(x))=d(0)=max(0,0)+1=1$$，因此$$d(a)+d(b)+d(c)\geq 3$$。然而如果$$d(x)+d(y)+d(z)=n$$，取$$k=n$$，得到$$d(a)+d(b)+d(c)\leq 0$$，矛盾，因此符合条件的$$x,y,z$$不存在。

**定理9** 如果$$x\nleq y$$，那么必有$$y\leq x$$

> 证明：假设$$x\nleq y,y\nleq x$$，利用定义2展开$$x\nleq y$$，得到$$(\exists x_l\in x_L:x_l\geq y)\lor(\exists y_r\in y_R:y_r\leq x),y\nleq x$$；利用定理8，把$$y\nleq x$$代入，得到$$(\exists x_l\in x_L:x_l\nleq x)\lor(\exists y_r\in y_R:y_r\ngeq y)$$，这与定理7矛盾，假设不成立，因此$$x\leq y$$和$$y\leq x$$至少有一个会成立。

**定理10** $$x\nleq y$$等价于$$y\lt x$$

> 证明：已知$$y\leq x,x\nleq y\Leftrightarrow y\lt x$$，定理9说明$$x\nleq y$$蕴含$$y\leq x$$，因此$$x\nleq y\Leftrightarrow y\lt x$$。

**定理7+** 给定一个“数”$$x$$，如果$$x_L$$非空，则$$\forall x_l\in x_L:x_l\lt x$$；如果$$x_R$$非空，则$$\forall x_r\in x_R:x_r\gt x$$。

> 证明：定理6表明$$x_L\ngeq x$$，$$x_R\nleq x$$，利用定理10的结论即可证明。

**定理11** 给定$$x,y,z$$都是“数”，如果$$x\lt y$$，$$y\leq z$$，则$$x\lt z$$；如果$$x\leq y$$，$$y\lt z$$，则$$x\lt z$$

> 证明：假设$$z\leq x$$，根据定理8，$$y\leq x$$；但是已知$$x\lt y$$，根据定理10，$$y\nleq x$$，矛盾，假设不成立，因此$$z\nleq x$$，根据定理10得$$x\lt z$$。第二条同理

**定理12** 给定$$x\equiv(L,R)$$是一个“数”，任意取两个“数”集$$Y_L,Y_R$$满足$$Y_L\lt x\lt Y_R$$，则$$z\equiv(x_L\cup Y_L,x_R\cup Y_R)=x$$。其中$$a=b$$表示$$a\leq b\land b\leq a$$

> 证明：根据定理7+，$$x_L\lt x$$，且$$z\lt x_R\cup Y_R$$因而$$x_L\cup Y_L\lt x$$，且$$z\lt x_R$$，根据定义2和定理10，得到$$z\leq x$$。同理可得$$x\leq z$$，因此$$x=z$$

**定理13** 给定“数”集$$N=\{x_1,x_2,...,x_m\}$$，满足$$x_1\lt x_2\lt...\lt x_m$$，则仅使用这$$m$$个数，只能得到$$m+1$$个新的“数”$$x'$$满足$$\forall x\in N:x'\neq x$$，且这些新“数”为：$$(\varnothing,\{x_1\}),(\{x_i\},\{x_{i+1}\}),(\{x_m\},\varnothing)$$

> 证明：(1.)初始集合$$N_1=\{0\}$$，新“数”集合$$\Delta N_0=\{(\varnothing,\{0\}),(\{0\},\varnothing)\}$$，满足条件。(2.)假设“数”集$$N_k=\{x_1,x_2,...,x_m\}$$是由满足条件的方式生成的，且$$x_1\lt x_2\lt...\lt x_m$$。根据定理12，$$(\{x_{i_1},x_{i_2},...\},\{x_{j_1},x_{j_2},...\})=(\{max(x_i)\},\{min(x_j)\})$$因而可以得到$$\Delta N_k=\{(\varnothing,\{x_i\})\}\cup\{(\{x_i\},\{x_j\})\|i\lt j\}\cup\{(x_i,\varnothing)\}$$。为了方便，记$$\varnothing\rightarrow\{x_0\}$$，$$\varnothing\rightarrow\{x_{m+1}\}$$，于是，$$\Delta N_k=\{(\{x_i\},\{x_j\})\|0\leq i\lt j\leq m+1\}$$。当$$j-i\geq2$$时，考虑“数”$$x_{i+1},x_{i+2},...,x_{j-1}$$，根据假设$$\forall x_l,i\lt l\lt j:(\exists!o\lt k:x_l\in \Delta N_o)$$（$$\Delta N_0=N_1$$）。结合定理8的证明，有$$d(x_l)=o+1$$。取$$x_l\equiv argmin(d(x_{i+1}),d(x_{i+2}),...,d(x_{j-1}))$$，根据假设，如果$$d(x_i)\leq d(x_j)$$，那么$$x_i$$的左右集都不会递归地包含$$x_j$$，因此$$x_{i+1},x_{i+2},...,x_{l-1}\notin{x_l}_L$$。又因为$${x_l}_L\ngeq x_l$$，因此$${x_l}_L\ngtr x_i$$。同理$${x_l}_R\nless x_j$$。根据定理12，$$(\{x_i\},\{x_j\})=(\{x_i\}\cup {x_l}_L,\{x_j\}\cup {x_l}_R)=({x_l}_L,{x_l}_R)\equiv x_l$$。注意到当$$i=0$$或者$$j=m+1$$时，$$x_l\ngtr\varnothing$$以及$$x_l\nless\varnothing$$依然成立。上述证明还说明了符合条件的$$x_l$$是唯一的，否则就有$$(\{x_i\},\{x_j\})\lt(\{x_i\},\{x_j\})$$，而这是不成立的。因此$$\Delta N_k=\{(\{x_i\},\{x_{i+1}\})\|i\in[0..m]\}$$。由(1.)和(2.)归纳即可证明定理13。

**定义5** 加法定义。给定“数”$$x,y$$，$$x+y\equiv((x_L+y)\cup (y_L+x),(x_R+y)\cup (y_R+x))$$

**定理14** 给定“数”$$x$$，$$x+0=x$$

> 证明：(1.)$$0+0\equiv(\varnothing,\varnothing)\equiv 0$$，(2.)$$x+0\equiv(x_L+0,x_R+0)$$。归纳得$$x+0\equiv x$$

## Day 4

**定义5** 相反数定义。给定“数”$$x$$，$$-x\equiv(-x_L,-x_R)$$

**定义6** 减法定义。给定“数”$$x,y$$，$$x-y\equiv x+(-y)$$

**定理15** 给定“数”$$x,y,z$$，若$$x+y=z$$则$$z-y=x$$

> 证明：TODO

**定理12+** 给定“数”$$x\equiv(L,R)$$，取“数”$$x\equiv argmin(\forall x_i,y_L\ngeq x_i\ngeq y_R:d(x_i))$$，则$$x=y$$

> 证明：根据定理7+，$$x_L\lt x$$，且$$z\lt x_R\cup Y_R$$因而$$x_L\cup Y_L\lt x$$，且$$z\lt x_R$$，根据定义2和定理10，得到$$z\leq x$$。同理可得$$x\leq z$$，因此$$x=z$$
