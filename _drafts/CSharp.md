- 委托返回值，允许函数返回子类
- 委托参数，允许函数传入基类

CS调用Lua，预创建委托，生成Wrap

1. CS

定义委托类型：

deletage R Signature(A a, B b, C c);

定义委托生成器：

Delegate SignatureGen(DelegateBridge){
    return new Signature(signature_gen); // 有隐式类型转换
}

定义委托播放函数：

R signature_gen(A a, B b, C c){
    // Lua Call
}

定义委托：

Signature signature;

缓存：

Dictionary<Type, Func<DelegateBridge, Delegate>> 委托的Type到委托生成器的映射

发起调用：

1. LuaEnv.Global.Get<Signature>(funcName): Signature;
   1. LuaEnv.Global.Get<string, Signature>(funcName, out Signature value): void;
      1. lua stack ops
      2. luaEnv.translator.Get<Signature>(L, -1, out Signature value): void;
         1. 基本类型 tryGetGetFuncByType(Type type, out T func): boolean;
            1. T 的函数签名为 Func<IntPtr, int, xxx>，第一个参数是Lua虚拟机，第二个参数是栈位置，返回类型xxx是 type
            2. Dictionary<Type, Delegate> get_func_with_type; 这里记录了基本类型的读取器
            3. 初始化的时候 Func<IntPtr, int, xxx> 会被隐式转成基类 Delegate
            4. 给func赋值的时候会有隐式转换，转回 Func<IntPtr, int, xxx>
         2. 其它一律走 GetObject(Intptr L, int index, Type type): object; type == typeof(Signature) 需要显式类型转成 type
            1. 缓存 TODO
            2. 如果是Wrap给Lua的userdata
            3. objectCasters.GetCaster(Type type): ObjectCast; type == typeof(Signature)
               1. type是委托类型，走 ObjectCast.Invoke(L, index, null)
                  1. translator.CreateDelegateBridge(L, type, index): object; type == typeof(Signature)
                     1. 把栈里的LuaFunction做个ref，后续就直接根据ref找委托了，如果ref找不到，再重新获取
                     2. bridge.GetDelegateByType(type): Delegate 返回的时候隐式转了 object
                        1. 去缓存里查表，返回的是生成器
                        2. 调用生成器返回委托，其已经有一个绑定是播放函数

这里用静态导出的形式，避免函数参数是基本类型的时候会被装箱成object有GC
