---
layout: page
title: Leet Code笔记
date: 2018-10-11 20:36:30 +0800
mdate: 2018-11-26 20:32:31 +0800
showbar: false
---

- [Pre](#pre)
    - [邪道](#%E9%82%AA%E9%81%93)
    - [浮点转整数](#%E6%B5%AE%E7%82%B9%E8%BD%AC%E6%95%B4%E6%95%B0)
- [P1 TwoSum](#p1-twosum)
- [P3 Longest Substring Without Repeating Characters](#p3-longest-substring-without-repeating-characters)
- [P4 Median of Two Sorted Arrays](#p4-median-of-two-sorted-arrays)
- [P5 最长回文子串](#p5-%E6%9C%80%E9%95%BF%E5%9B%9E%E6%96%87%E5%AD%90%E4%B8%B2)
- [P11 Container With Most Water](#p11-container-with-most-water)
- [P28 字符串匹配](#p28-%E5%AD%97%E7%AC%A6%E4%B8%B2%E5%8C%B9%E9%85%8D)
- [P41 First Missing Positive](#p41-first-missing-positive)
- [P84 Largest Rectangle in Histogram](#p84-largest-rectangle-in-histogram)
- [P85 Maximal Rectangle](#p85-maximal-rectangle)
- [P494 求目标和](#p494-%E6%B1%82%E7%9B%AE%E6%A0%87%E5%92%8C)
- [P673 最长上升子序列个数](#p673-%E6%9C%80%E9%95%BF%E4%B8%8A%E5%8D%87%E5%AD%90%E5%BA%8F%E5%88%97%E4%B8%AA%E6%95%B0)

## Pre

### 邪道

在题解类前面插入代码加速读取：

```c++
auto x = []()
{
    std::ios::sync_with_stdio(false);
    cin.tie(NULL);
    return 0;
}();
```

### 浮点转整数

1. `floor`:不大于的最大整数
2. `ceil`:不小于的最小整数
3. ...

## P1 TwoSum

给定一个数组，从里面挑两个使得和为某一给定值。（数不重复且每个只能挑一遍）

任意数$$A$$，目标$$T$$，只要$$B=T-A$$在数组内即可

为了快速验证$$B$$，建立一个hash table记录索引。

```
for all A in Array:
    if B in hash table:
        return result
    Add A to hash table
```

## P3 Longest Substring Without Repeating Characters

数组$$A$$记录每个字符上一次出现的位置

记录当前不重复子串的起始位置$$l$$

```
l = 0
for all character C in s:
    if A[C] >= l:
        l = A[C] + 1
    Calculate length start from index l and ends at character C
    Update max length
```

时间复杂度$$O(n)$$

## P4 Median of Two Sorted Arrays

中位数：所有小于等于中位数的个数和大于等于中位数的个数相等

数组$$A_N$$和$$B_M$$，在$$A$$中找到分割点$$i$$，在$$B$$中找到分割点$$j$$，将整个数组分为两个部分$$L$$和$$H$$：

```
AL = A[:i]
AH = A[i:]
BL = B[:j]
BH = B[j:]
L = AL + BL
H = AH + BH
```

如果能找到这样的$$i$$，$$j$$使得$$L$$正好是小于中位数的那一半，而$$H$$正好是大于中位数的那一半，那么就可以找到中位数。

分成两半$$i+j=N-i+M-j$$，得到$$j=0.5*(N+M)-i$$。由于两个数组本生是排好序的，所以满足中位数的条件有两个：$$A_{i-1}\le B_j$$以及$$A_i\ge B_{j-1}$$。

如果条件一不满足，说明$$i_{real}\lt i$$；如果条件二不满足，说明$$i_{real}\gt i$$；两个条件不可能同时不满足。

二分即可

## P5 最长回文子串

首先在字符之间和首尾加上特殊符号，可以是'#'，这样就不用考虑回文串的长度的奇偶

再在新串的首位加上不同的特殊符号，可以是'^'和'$'，这样就不用单独考虑边界情况

```
  b a b c b a b c b a c c b a
^#b#a#b#c#b#a#b#c#b#a#c#c#b#a#$
```

记$$P_i$$为以$$i$$为中心，最大的回文长度（距中心的长度）

```
0123456789ABCDEF...
^#b#a#b#c#b#a#b#c#b#a#c#c#b#a#$
P010301070109010...
```

定义已知回文串中心$$C$$，以及其右端点$$R$$

对于字符串上的每一个位置$$i$$，如果$$i\lt R$$说明该中心位于已知回文串的内部，那么根据对称性，$$P_i=P_{2*C-i}$$，例如当$$C=11$$，$$i=13$$时，$$P_{11}=P_9=1$$；但当$$i=15$$时，如果用相同的方法，$$P_{15}=P_7=7$$，就会发现$$i$$为中心的子串的右端点$$15+7=22$$超过了$$C$$为中心的子串的右端点$$R=20$$，而$$R$$右侧的情况是未知的，所以最右只能取到$$R$$，之后要逐项判断：

```
P[i]=max{min{P[2*C-i], R-i}, 0}
P[i]=Expand(P[i])
```

显然如果$$i$$本身就在$$R$$右侧那么就没有对称性可以参考，也必须逐项判断

如果扩展结束后的回文串的右端点超过$$R$$，即$$P_i+i\gt R$$，那么就把$$i$$作为新的中心，$$P_i+i$$作为新的右端点

最后把$$P$$数组遍历一遍，找到值最大的，取值和其索引，索引恢复到原始串的索引，值恢复到原始串内的长度（一半）

## P11 Container With Most Water

用$$f_{i,j}$$表示左端$$i$$，右端$$j$$可以存多少，$$f_{i,j}=min(h_i,h_j)*(j-i+1)$$。

理论上所有$$(i,j)$$组合都要算一遍但是由于高度是短板决定的，所以

如果短板是$$i$$：

$$
\begin{align}
f_{i,j}&\gt min(h_i, h_j)*(k-i+1)\\
&\ge min(h_i, h_k)*(k-i+1)\\
&=f_{i,k}
\end{align}
$$

即所有以$$i$$为左端点，$$j$$左侧的点为右端点的就不用算了；短板是$$j$$时同理，$$i$$右侧的也不用算了

```
l = 0, r = n - 1
while l < r:
    Update max area
    if i is shorter:
        ++i
    else:
        --j
```

## P28 字符串匹配

求字串在原字符串中的位置，KMP

```
int n = //原串长度;
int m = //子串长度;
vector<int> next_table(m, -1);// 转移表，初始-1

for(int i = 1; i < m; ++i)
{
    int tmp = i - 1;// 前一个位置
    while(tmp > -1)
    {
        tmp = next_table[tmp];// 前缀的末位索引，-1表示不存在，保持语义一致
        if(needle[tmp + 1] == needle[i])
        {
            /* 找到i对应的前缀末位索引 */
            next_table[i] = tmp + 1;
            break;
        }
    }
}

int k = 0;
for(int i = 0; i < n;)
{
    /* 一直匹配上 */
    while(needle[k] == haystack[i + k] && k < m)
    {
        ++k;
    }
    /* 直到末尾 */
    if(k == m)
    {
        return i;
    }
    /* 如果不是末尾，找跳转表 */
    if(k > 0)
    {
        i += k;
        k = next_table[k - 1] + 1;
        i -= k;
    }
    else
    {
        i += 1;
    }
}
return -1;
```

## P41 First Missing Positive

给定数组，找到最小缺失的整数

不缺的情况下$$A_i=i+1$$，所以只要把每个数放到其应该出现的位置。注意点：

1. 跳过不该出现的数（非正整数，超过数组大小）
2. 跳过已经在正确位置上的数
3. 交换过来的数可能依然不在其正确位置上，所以要持续交换直到其应该被跳过
4. 数组里的数可能重复，所以如果交换的两个数相等也要跳过，防止死循环

```
for k, v in A:
    while (v in range) and (v not in the right place) and (A[v - 1] != v):
        swap(A[v - 1], A[k])
for k, v in A:
    if v != k + 1:
        return k + 1
```

## P84 Largest Rectangle in Histogram

用$$f_i$$表示以$$i$$为最短两边扩展的最大面积，所以要在$$i$$左右各找到第一个比$$i$$短的。维护一个栈，顺序遍历每个长条：如果当前$$r$$比栈顶$$i$$长就直接压栈；如果当前比栈顶短：

1. 弹栈得到$$i$$
    - 新栈顶$$l$$必然是$$i$$左侧第一个比$$i$$短的，因为比$$i$$长的已经弹栈了
    - 而当前$$r$$必然是$$i$$右侧第一个比$$i$$短的，遍历顺序就是从左往右的
2. 用$$l$$和$$r$$可以计算$$f_i$$
3. 挑选所有$$f_i$$里最大的为最终结果

## P85 Maximal Rectangle

逐行做，$$f_i$$代表前$$i$$行的最大面积，每行都能化简成一个P84的子问题：

```
height = []
Set hea all to zero
for each row from top to bottom:
    for each col in this row:
        if value at (row, col) is 1:
            ++height[col]
        else:
            height[col] = 0
    Solve P84 on height
    Update max area
``` 

## P494 求目标和

给定一串数，每个数可以任意添加正负号，最后将这些数加起来，使得和等于给定值`S`，求添加正负号的种类数

1. DP：`dp[i][j]`，前`i+1`个数字，和为`j`的种数。由于已知和不超过`1000`，`j`的维数为`2001`。所以有`dp[i][j]=dp[i-1][j-nums[i]]+dp[i-1][j+nums[i]]`，最终结果为`dp[n-1][S]`
2. 改进DP：
   1. 假设所有数之和为`sum`，那么可能产生的和最小为`-sum`，最大为`sum`。左右同时加`sum`使可能最小值变为`0`，这样左边的条件变为，不选或者选择该数的两倍，右边的条件变为`S+sum`
   2. 上述变化之后，每一项无论怎么选都是偶数，所以`S+sum`也应该是偶数，所以可以将和为奇数的直接筛掉，并将和为偶数的部分两边除以`2`，这样左边的条件变为每个数选或不选，右边的条件变为`(S+sum)/2`
   3. `dp[i][j]=dp[i-1][j]+dp[i-1][j-nums[i]]`，`dp[0][0]=1`
   4. 上式的特点是每一行的第`j`列，和上一行第`j`列以后的所有列都无关，因此只要`j`倒序循环，就可以在空间上消掉`i`的那维：`dp[j]=dp[j]+dp[j-num[i]]`，最终结果为`dp[(S+sum)/2]`

第一个是我写的，20ms；第二个是最速，0ms

## P673 最长上升子序列个数

`L[i]`为以`s[i]`作为初始字符的最长上升子序列长度

`N[i]`为`s[i]`作为初始字符的长度为`L[i]`的上升子序列长度

`L[i]=max{L[j]+1},j>i`

`N[i]=sum{N[j]},j>i,L[j]+1=L[i]`

但是最终结果不限定初始字符的位置，所以每一个`L[i]`都可能是结果长度

`MaxL=max{L[i]}`

`MaxN=sum{N[i]},L[i]=MaxL`
