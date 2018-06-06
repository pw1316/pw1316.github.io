---
layout: page
title: 使用C++03定义不可被继承的类
showbar: false
---

## 题外话

虽然C++11早就引入了*final*关键字，但是还是记一笔，毕竟曾经也是个骚操作。

## 结果

```c++
template<class T>
class Base
{
    friend T;
private:
    Base() = default;
    ~Base() = default;
};

class FinalClass : public virtual Base<FinalClass>
{
public:
    FinalClass() = default;
    ~FinalClass() = default;
};

/* Will not compile */
// class Derived : public FinalClass
// {
// public:
//     Derived() = default;
//     ~Derived() = default;
// };
```

## 解释（又摸了）
