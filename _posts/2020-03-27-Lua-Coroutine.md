---
layout: page
title: Lua-Coroutine
date: 2020-03-27 20:25:45 +0800
mdate: 2020-03-27 20:25:45 +0800
---

## 0. thread 类型

存在四种状态：

S(uspended)，R(unning)，D(ead)，N(ormal)

## 1. coroutine.create(f)

创建一个coroutine

### 参数

`f`为一个函数，其代码为coroutine执行内容

### 返回值

返回一个`thread`类型的值

## 2. coroutine.status(co)

获取coroutine的状态

### 参数

`co`为一个thread类型的值

### 返回值

返回一个字符串表示该coroutine当前的状态

## 3. coroutine.resume(co, ...)

唤醒一个coroutine，目标进入R状态，自己进入N状态

### 参数

`co`为待唤醒的coroutine

`...`如果目标是第一次被唤醒，其将作为目标coroutine的参数；如果不是第一次，这些数据作为`yield`的返回值被获取

### 返回值

第一个值为`boolean`类型表示是否成功

后面的所有值为目标coroutine挂起时传入`yield`的参数，或者为目标coroutine结束时的返回值

## 4. coroutine.yield(...)

使当前coroutine挂起，自己进入S状态

### 参数

`...`为向唤醒它的coroutine传输的数据，唤醒它的coroutine在`resume`的返回值中获得

### 返回值

所有值为将其唤醒的coroutine调用`resume`时传入的额外参数
