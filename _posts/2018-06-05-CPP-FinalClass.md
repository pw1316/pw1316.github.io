---
layout: page
title: c++定义不可被继承的类
date: 2018-06-05 21:01:09 +0800
mdate: 2018-10-23 20:50:57 +0800
---

不使用`final`关键字让类不可被继承

## 实现

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

类`Base`的构造函数和析构函数设置为`private`使得子类和用户代码不能创建和销毁该类对象，但允许友元类`T`创建和销毁

类`FinalClass`通过`public`继承于类`Base`并且是类`Base`的友元，因此类`FinalClass`可以创建和销毁类`Base`的对象，因而子类和用户代码可以创建和销毁类`FinalClass`，即正常使用。类`Base`是模板类的原因仅仅是让不同的*final*类存在不同的基类

为了使`FinalClass`不能被继承，需让其子类`Derived`无法构造。显然类`Derived`无法构造`Base`对象，所以只要把`FinalClass`和`Base`之间的继承改成虚继承（普通继承子类仅负责构造直接父类）即可使`Derived`在构造时必须直接构造`Base`部分，然而`Derived`访问不到`Base`的构造函数，所以`Derived`的对象就无法被构造，因而类`FinalClass`是不可被继承的。
