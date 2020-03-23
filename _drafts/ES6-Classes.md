---
layout: page
title: ES6的类与原型
date: 2020-03-20 23:22:44 +0800
mdate: 2020-03-20 23:22:44 +0800
---

## 运行环境与this

ES中运行环境与函数相关（个人理解类比`var`定义的变量的作用域）。

`this`对象用于指代运行环境对象，主要区分全局和函数内。

全局的`this`为`window`（浏览器）或`module.exports`（node）。

函数内的`this`为调用该函数的对象；如果没有对象，严格模式下为`undefined`，一般模式下是`window`（浏览器）或`global`（node）。

具体看[这里](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/this)。

特别地，箭头函数不会生成新的运行环境，对这个函数使用`call`或`bind`均不会改变函数体内的`this`。

## 类与对象

ES里的类实际上就是函数，并通过关键字`new`来创建类的实例对象。`new`的可以暂时简单定义为以下操作：

```javascript
function operator_new(Class) {
    var obj = {};
    Class.call(obj); // 将obj作为this调用Class()
    return obj;
}
```

所以定义一个函数（类），可以这样创建对象：

```javascript
function Cls() {
    this.prop = 1;
}
var obj = new Cls(); // obj: Cls { prop: 1 }
```

显然如果给这个类定义一个成员函数，那么这个类的每一个实例都持有一份该成员函数的副本，无法复用。

## prototype VS [[prototype]]

为了解决问题，我们给函数（类）定义了一个`prototype`属性，`prototype`属性本身是一个对象，它用于存放需要在类内共享的属性，该类的所有实例都可以直接访问这些属性。`prototype`属性所指向的对象，其目的是在特定对象之间共享属性，这样的对象称作原型对象。

ES中所有的对象都是某个类的实例（`Object.prototype`应该不是），因而都会具有原型对象。为了让对象能访问到原型对象，ES引入`[[prototype]]`属性。对象的`[[prototype]]`属性本质是对某个类的`prototype`属性的引用，所以能够表示对象与类的关系。对象在读属性时，先查找自身是否存在对应的属性/getter，如果没有找到，在原型对象中继续查找，不断循环，直到某个原型对象不存在原型对象（`Object.prototype`或`Object.create(null)`）。对象在写属性时，仅查找自身是否存在属性/setter，如果没有就直接新增。在大部分解释器中`[[prototype]]`的实现为`__proto__`。

有了原型对象，就要修改`new`的实现来明确类与实例对象的关系：

```javascript
function operator_new(Class) {
    var obj = {};
    obj.__proto__ = Class.prototype;
    Class.call(obj); // 将obj作为this调用Class()
    return obj;
}
```

这样一来，重新定义函数，并在原型对象内定义共享属性

```javascript
function Cls() {
    this.prop = 1;
}
Cls.prototype.shared_prop = 2; // 只要是Cls的实例，都共享shared_prop属性
var obj_1 = new Cls(); // obj_1: Cls { prop: 1, __proto__.shared_prop: 2 }
var obj_2 = new Cls(); // obj_2: Cls { prop: 1, __proto__.shared_prop: 2 }
obj_2.prop = obj_2.__proto__.shared_prop = 3;
// obj_1: Cls { prop: 1, __proto__.shared_prop: 3 }
// obj_2: Cls { prop: 3, __proto__.shared_prop: 3 }
```

这么一看，读属性时会往`[[prototype]]`里找是为了共享，而写属性时不往`[[prototype]]`里找是因为乱改会产生其它影响。

## constructor

事实上，类本身应该也在所有对象之间共享。如果现在只能拿到某个类的实例对象，就没有办法继续创建这个类的更多实例对象。因此类自身（构造函数）也能被对象访问到是一个合理的设计。所以在通常定义一个函数时，它的`prototype`属性里会自带一个`constructor`的属性，这个属性指向函数自身，即`Class.prototype.constructor === Class`。当然这不绝对，用户可以对`prototype`属性重新赋值，也可以对`prototype.constructor`重新赋值，但这么做会改变“对象生成同类对象的行为”，除非特殊设计，`prototype.constructor`还是时刻注意与类自身保持一致。

```javascript
function Cls() { } // Cls.prototype: Object { constructor: Cls }
var obj_1 = new Cls(); // obj_1: Cls {}
var obj_2 = new obj_1.constructor(); // obj_2: Cls {}
```

## 原型链与Object

前面提到大部分对象都有原型对象，并且原型对象还有原型对象，因此根据`[[prototype]]`属性可以形成一个对象链，即原型链。因而在读一个对象的属性时，实际上是在对象的原型链上查找属性是否存在。

前面也提到`Object.prototype`没有原型对象（`Object.prototype.__proto__ === null`）。`Object`是一个类，大部分对象都是类`Object`的直接实例或间接实例，所以这些对象的原型链最终都会停在`Object.prototype`上。

```javascript
var obj = {}; // 定义空对象
obj.__proto__ === Object.prototype; // 空对象是类Object的实例

function Base() { } // 定义函数（类）
Base.__proto__ === Function.prototype; // 函数本身是类Function的实例
Function.prototype.__proto__ === Object.prototype; // 类Function的prototype属性是类Object的实例

var obj = new Base(); // 定义类的实例对象
obj.__proto__ === Base.prototype; // 对象是类Base的实例
Base.prototype.__proto__ === Object.prototype; // 类Base的prototype属性是类Object的实例
```

但是`Object.create(null)`会生成一个没有原型对象的对象，虽然也是个对象，但不是能正常用的对象（类`Object`的实例）。我暂时知道有啥用，这类对象和原型链终点是这类对象的对象，就不讨论了。

还有一个特殊的关键字就是`instanceof`，其实现可以简单表述为如下：

```javascript
function obj_instanceof_class(obj, cls) {
    let l = obj.__proto__;
    while (l !== null) {
        if (l === cls.prototype) {
            return true;
        }
        l = l.__proto__;
    }
    return false;
}
```

当然，此处没考虑变态的原型链成环的情况，但是简单来说，如果一个对象的原型链上有一个对象与这个类的`prototype`属性严格相等，那么就说这个对象是这个类的一个实例。

## 继承

利用原型链，可以实现继承。由于对象可以访问原型链上的所有属性，因此就相当于继承了原型链上的对象。首先定义一个基类：

```javascript
function Base() {
    this.base_prop = "base_prop";
}
Base.prototype.base_shared_prop = "base_shared_prop";
var base = new Base();
base.base_prop; // 类定义的实例属性
base.base_shared_prop; // 继承自Base.prototype，类的共享属性
```

然后根据子类定义的不同，分为几种不同的继承方式：

```javascript
// [1] 共享原型
function Derive() { }
Derive.prototype = Base.prototype;
Derive.prototype.derive_shared_prop = "derive_shared_prop"; // 会影响所有类Base的实例
// 结果：
var derive = new Derive();
// derive.base_prop; // 没有继承父类的实例属性
derive.derive_shared_prop; // 继承自Base.prototype，子类的共享属性
derive.base_shared_prop; // 继承自Base.prototype，父类的共享属性

// [2] 继承实例
function Derive() { }
Derive.prototype = new Base();
Derive.prototype.constructor = Derive;
Derive.prototype.derive_shared_prop = "derive_shared_prop";
// 结果：
var derive = new Derive();
derive.base_prop; // 继承自Derive.prototype，子类的共享属性、父类的实例属性
derive.derive_shared_prop; // 继承自Derive.prototype，子类的共享属性
derive.base_shared_prop; // 继承自Base.prototype，父类的共享属性

// [3] 继承原型
function Derive() { }
Derive.prototype = Object.create(Base.prototype);
Derive.prototype.constructor = Derive;
Derive.prototype.derive_shared_prop = "derive_shared_prop";
// 结果：
var derive = new Derive();
// derive.base_prop; // 没有继承父类的实例属性
derive.derive_shared_prop; // 继承自Derive.prototype，子类的共享属性
derive.base_shared_prop; // 继承自Base.prototype，父类的共享属性

// [4] 继承构造
function Derive() {
    Base.call(this);
}
Derive.prototype.derive_shared_prop = "derive_shared_prop";
// 结果：
var derive = new Derive();
derive.base_prop; // 继承自Base，子类的实例属性、父类的实例属性
derive.derive_shared_prop; // 继承自Derive.prototype，子类的共享属性
// derive.base_shared_prop; // 没有继承父类的共享属性


// [5] 混合继承[3][4]
function Derive() {
    Base.call(this);
}
Derive.prototype = Object.create(Base.prototype);
Derive.prototype.constructor = Derive;
Derive.prototype.derive_shared_prop = "derive_shared_prop";
// 结果：
var derive = new Derive();
derive.base_prop; // 继承自Base，子类的实例属性、父类的实例属性
derive.derive_shared_prop; // 继承自Derive.prototype，子类的共享属性
derive.base_shared_prop; // 继承自Base.prototype，父类的共享属性
```

- 1.第一种相当于重载了构造函数算不上继承
- 2.第二种继承了完整的父类实例，但是父类里的实例属性在子类里边共享了，这点和一般概念的继承不符
- 3.第三种继承了父类的共享属性，所以访问不到父类的实例属性
- 4.第四种只继承了父类的实例属性，所以访问不到父类的共享属性
- 5.第五种混合了3和4两种继承方法，符合一般概念种的继承

## ES6的class

ES6引入了class关键字，如果一个函数拿来当类用，那么就可以用该关键字来定义函数：

```javascript
class Base {
    // Base以及Base.protptype.constructor都指向这个函数
    constructor(){
        this.base_prop = "base_prop";
    }
    // 普通函数的定义都挂在prototype里，相当于Base.prototype.base_member
    base_member() { }
    // 静态函数的定义直接挂在函数上，相当于Base.static_base_member
    static static_base_member() { }
}
class Derive extends Base {
    constructor(){ }
    derive_member() { }
    static static_derive_member() { }
}
```

上述写法本身是对函数类的定义以及混合继承的语法糖，因此类`Base`，类`Derive`以及相关实例对象之间的关系与第五种继承方式中的描述一致，唯一的区别是，这个语法糖中还特别让`Derive.__proto__ === Base`，从而实现静态函数的继承，同时又有`Derive.__proto__.__proto__ === Function.prototype`并未破环原有原型链。
