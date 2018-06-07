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

## 解释

原始的基类*Base*的构造函数和析构函数设置为*private*使得该对象不能从子类，用户代码被创建，而只能通过成员进行创建与销毁。但是该基类设置了友元，使得友元也可以创建和销毁
基类对象。

子类*FinalClass*继承基类*Base*并且是基类*Base*的友元，因此可以访问到基类*Base*的*private*成员，因此子类*FinalClass*的对象可以被其子类，成员，以及用户代码创建以及销毁，即该子类*FinalClass*可以正常使用。

为了使*FinalClass*不能被继承，需考虑它的子类*Derived*会访问其没有访问权限的内容。注意到其间接基类*Base*的构造函数和析构函数是*private*权限且其不是该基类的友元，因此其不能构造和销毁这部分基类的内容。但是一般的继承中子类只负责构造和销毁其直接父类的内容，因此为了使子类*Derived*直接访问到*Base*的构造函数，需要将*Base*设置为虚基类。在*C++*的继承体系中，最终的子类会优先构造所有的虚基类，之后才会根据顺序逐一构造非虚的直接父类。因此只要将*FinalClass*对*Base*的继承改为虚继承即可阻止*Derived*对象的创建与销毁。因为*Derived*的对象在构造时会先构造虚基类*Base*而它的构造函数无法访问，因此这个对象就无法创建。
