---
layout: page
title: 研究之美
date: 2019-01-23 15:27:39 +0800
mdate: 2019-01-24 20:50:25 +0800
showbar: false
---

## Before All

**定义1** “数”的定义。“数”构成了集合$$x\in N$$，“数”由两个集合组成$$x\equiv(L,R)$$，这两个集合中的元素也是“数”$$L,R\subset N$$，不存在这样的数$$i,j$$同时满足：$$i\in L$$，$$j\in R$$，$$i\geq j(j\leq i)$$。符合上述定义的元素称为“数”。上述定义简写为$$L\ngeq R$$。

**定义2** “小于等于”的定义。给定两个“数”$$i,j$$，如果既不存在“数”$$k$$同时满足：$$k\in i_L$$，$$k\geq j$$，也不存在“数”$$l$$同时满足$$l\in j_R$$，$$l\leq i$$，则称$$i\leq j(j\geq i)$$。上述定义简写为$$i_L\ngeq j\land j_R\nleq i$$。

## Day 1

**定义3** $$0\equiv(\varnothing,\varnothing)$$。

**定理1** $$0$$是“数”。

> 证明：$$0_L\equiv\varnothing\ngeq\varnothing\equiv0_R$$，因而$$0_L\ngeq 0_R$$，符合定义1。

**定理2** $$0\leq 0$$。

> 证明：$$0_L\equiv\varnothing\ngeq 0$$，$$0_R\equiv\varnothing\nleq 0$$，符合定义2。

## Day 2

**定义4** $$1\equiv(\{0\},\varnothing)$$，$$-1\equiv(\varnothing,\{0\})$$。

**定理3** $$1$$和$$-1$$都是“数”。

> 证明：对于$$1$$，$$\{0\}\ngeq\varnothing$$；对于$$-1$$，$$\varnothing\ngeq\{0\}$$。两者都符合定义1。

**定理4** $$x\equiv(L,\varnothing)$$和$$y\equiv(\varnothing,R)$$都是“数”，且$$y\leq x$$，其中$$L$$，$$R$$为任意“数”集。

> 证明：同定理3。

**定理5** $$-1\lt 0$$，$$0\lt 1$$，$$-1\lt 1$$。

> 证明：根据定理4可得$$-1\leq0$$，$$-1\leq1$$，$$0\leq1$$。已知$$-1_R\equiv\{0\}$$，而根据定理2，$$0\geq 0$$，因此$$0\nleq -1$$，即$$-1\lt 0$$。同理可得$$0\lt 1$$。又已知$$1_L\equiv\{0\}$$，而$$0\geq -1$$，因此$$1\nleq-1$$即$$-1\lt 1$$。

## Day 3

**定理6** 如果$$x$$是“数”，则$$x\leq x$$。

> 证明：(1.)根据定理2得到$$0\leq 0$$。(2.)已知$$x_L$$非空且$$\forall x_l\in x_L:x_l\leq x_l$$，$$x_R$$非空且$$\forall x_r\in x_R:x_r\leq x_r$$，则$$x_L\ngeq x_l$$不成立，$$x_R\nleq x_r$$不成立；根据定义2得到$$\forall x_l\in x_L:x\nleq x_l$$，$$\forall x_r\in x_R:x_r\nleq x$$，即$$x_L\ngeq x$$，$$x_R\nleq x$$；再根据定义2得到$$x\leq x$$。如果$$x_L$$为空则$$\varnothing\ngeq x$$天然成立，$$x_R$$为空则$$\varnothing\nleq x$$也天然成立。结合(1.)和(2.)归纳可得$$x\leq x$$。

**定理7** 给定一个“数”$$x$$，如果$$x_L$$非空，则$$\forall x_l\in x_L:x_l\leq x$$；如果$$x_R$$非空，则$$\forall x_r\in x_R:x_r\geq x$$。

> 证明：(1.)首先证明$$\forall R:0\leq(\{0\}, R)$$。由于不等号右侧需要符合定义1，因此$$R\nleq 0$$；又因为$$0_L\equiv\varnothing\ngeq(\{0\}, R)$$，根据定义2得到$$0\leq(\{0\}, R)$$。(2.)已知$$x_L$$非空，且$$\forall x_l\in x_L,x_{lL}\neq\varnothing,x_{ll}\in x_{lL}:x_{ll}\leq x_l$$，那么首先$$x$$是个“数”，根据定义1得到$$\forall x_l\in x_L:x_R\nleq x_l$$。其次，如果$$x_{lL}$$为空，则$$\varnothing\ngeq x$$，因而根据定义2有$$\forall x_l\in x_L:x_l\leq x$$；如果$$x_{lL}$$非空，假设$$\exists x_l\in x_L:x_l\nleq x$$，那么定义2的两个条件$$x_{lL}\ngeq x$$，$$x_R\nleq x_l$$至少有一个不满足，但是由于第二个条件必然成立，所以可以得到$$\exists x_l\in x_L,x_{ll}\in x_{lL}:x_{ll}\geq x$$，再根据定义2，$$\exists x_l\in x_L,x_{ll}\in x_{lL}:x_L\ngeq x_{ll}$$，这与前提条件$$x_{ll}\leq x_l$$矛盾，假设不成立，因此$$\forall x_l\in x_L:x_l\leq x$$。由(1.)和(2.)归纳可得$$\forall x_l\in x_L:x_l\leq x$$；同理，$$\forall x_r\in x_R:x_r\geq x$$。

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

**定理12** 给定$$x\equiv(L,R)$$是一个数，任意取两个“数”集$$Y_L,Y_R$$满足$$Y_L\lt x\lt Y_R$$，则$$z\equiv(x_L\cup Y_L,x_R\cup Y_R)=x$$。其中$$a=b$$表示$$a\leq b\land b\leq a$$

> 证明：根据定理7+，$$x_L\lt x$$，且$$z\lt x_R\cup Y_R$$因而$$x_L\cup Y_L\lt x$$，且$$z\lt x_R$$，根据定义2和定理10，得到$$z\leq x$$。同理可得$$x\leq z$$，因此$$x=z$$
