---
layout: page
title: Leet Code笔记
showbar: false
---

## 1 邪道

在题解类前面插入代码加速读取：

```c++
auto x = []()
{
    std::ios::sync_with_stdio(false);
    cin.tie(NULL);
    return 0;
}();
```

## 2 浮点转整数

1. `floor`:不大于的最大整数
2. `ceil`:不小于的最小整数
3. ...

## 3 P3最长不重复子串

用一个Map记录访问过的字符的最新位置（反正字符就这么点，直接开数组比各种Hash快）

记录当前不重复子串的起始位置`start`

顺序访问字符串的每个字符，先访问Map查找上次出现的位置，如果没有出现过或者出现在当前子串之前，说明从`start`开始到当前字符都是不重复的；否则该字符重复，其上次出现的位置的下一个字符作为新的`start`。

时间复杂度`O(n)`

## 4 P5最长回文子串

首先在字符之间和首尾加上特殊符号，可以是'#'，这样就不用考虑回文串的长度的奇偶

再在新串的首位加上不同的特殊符号，可以是'^'和'$'，这样就不用单独考虑边界情况

```
  b a b c b a b c b a c c b a
^#b#a#b#c#b#a#b#c#b#a#c#c#b#a#$
```

记`P[i]`为以`i`为中心，最大的回文长度（距中心的长度）

```
0123456789ABCDEF...
^#b#a#b#c#b#a#b#c#b#a#c#c#b#a#$
P010301070109010...
```

定义已知回文串中心`C`，以及其右端点`R`

对于字符串上的每一个位置`i`，如果`i<R`说明该中心位于已知回文串的内部，那么根据对称性，`P[i]=P[2*C-i]`，例如当`C=11`，`i=13`时，`P[11]=P[9]=1`；但当`i=15`时，如果用相同的方法，`P[15]=P[7]=7`，就会发现`i`为中心的子串的右端点`15+7=22`超过了`C`为中心的子串的右端点`R=20`，而`R`右侧的情况是未知的，所以最右只能取到`R`，之后要逐项判断：

```
P[i]=max{min{P[2*C-i], R-i}, 0}
P[i]=Expand(P[i])
```

显然如果`i`本身就在`R`右侧那么就没有对称性可以参考，也必须逐项判断

如果扩展结束后的回文串的右端点超过`R`，即`P[i]+i>R`，那么就把`i`作为新的中心，`P[i]+i`作为新的右端点

最后把`P`数组遍历一遍，找到值最大的，取值和其索引，索引恢复到原始串的索引，值恢复到原始串内的长度（一半）

## 5 P494求目标和

给定一串数，每个数可以任意添加正负号，最后将这些数加起来，使得和等于给定值`S`，求添加正负号的种类数

1. DP：`dp[i][j]`，前`i+1`个数字，和为`j`的种数。由于已知和不超过`1000`，`j`的维数为`2001`。所以有`dp[i][j]=dp[i-1][j-nums[i]]+dp[i-1][j+nums[i]]`，最终结果为`dp[n-1][S]`
2. 改进DP：
   1. 假设所有数之和为`sum`，那么可能产生的和最小为`-sum`，最大为`sum`。左右同时加`sum`使可能最小值变为`0`，这样左边的条件变为，不选或者选择该数的两倍，右边的条件变为`S+sum`
   2. 上述变化之后，每一项无论怎么选都是偶数，所以`S+sum`也应该是偶数，所以可以将和为奇数的直接筛掉，并将和为偶数的部分两边除以`2`，这样左边的条件变为每个数选或不选，右边的条件变为`(S+sum)/2`
   3. `dp[i][j]=dp[i-1][j]+dp[i-1][j-nums[i]]`，`dp[0][0]=1`
   4. 上式的特点是每一行的第`j`列，和上一行第`j`列以后的所有列都无关，因此只要`j`倒序循环，就可以在空间上消掉`i`的那维：`dp[j]=dp[j]+dp[j-num[i]]`，最终结果为`dp[(S+sum)/2]`

第一个是我写的，20ms；第二个是最速，0ms

## 6 P673最长上升子序列个数

`L[i]`为以`s[i]`作为初始字符的最长上升子序列长度

`N[i]`为`s[i]`作为初始字符的长度为`L[i]`的上升子序列长度

`L[i]=max{L[j]+1},j>i`

`N[i]=sum{N[j]},j>i,L[j]+1=L[i]`

但是最终结果不限定初始字符的位置，所以每一个`L[i]`都可能是结果长度

`MaxL=max{L[i]}`

`MaxN=sum{N[i]},L[i]=MaxL`