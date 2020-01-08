---
layout: page
title: Vulkan Notes
date: 2020-01-08 16:15:10 +0800
mdate: 2020-01-08 16:15:10 +0800
---

- [1. 实例](#1-%e5%ae%9e%e4%be%8b)
  - [1.1. 实例层](#11-%e5%ae%9e%e4%be%8b%e5%b1%82)
  - [1.2. 实例扩展](#12-%e5%ae%9e%e4%be%8b%e6%89%a9%e5%b1%95)
  - [1.3. VkInstance](#13-vkinstance)
  - [1.3.1. 结构体](#131-%e7%bb%93%e6%9e%84%e4%bd%93)
  - [1.4. VkDebugUtilsMessengerEXT](#14-vkdebugutilsmessengerext)
    - [1.4.1 回调函数](#141-%e5%9b%9e%e8%b0%83%e5%87%bd%e6%95%b0)
- [2. 窗口](#2-%e7%aa%97%e5%8f%a3)
- [3. Device](#3-device)
  - [3.2. Physical Device](#32-physical-device)

## 1. 实例

### 1.1. 实例层

接口`vkEnumerateInstanceLayerProperties()`可枚举所有VulkanRT支持的层。

### 1.2. 实例扩展

接口`vkEnumerateInstanceExtensionProperties()`可枚举所有VulkanRT支持的扩展。

### 1.3. VkInstance

句柄`VkInstance`，对应结构体`VkInstanceCreateInfo`。

### 1.3.1. 结构体

结构体内要提供以下内容：

{:.tbl style="background-color:#EEC"}
| 提供内容 | 备注 |
|-|-|
| 开启的Instance Layer | 需要VulkanRT支持 |
| 开启的Instance Extension | 需要VulkanRT支持 |
| Application Info | 元信息、不影响结果 |

> Vulkan的合法性检查需要开启`"VK_LAYER_LUNARG_standard_validation"`层\\
> GLFW窗口需要开启`glfwGetRequiredInstanceExtensions()`获得的扩展\\
> 启用调试需要开启`"VK_EXT_debug_utils"`扩展

### 1.4. VkDebugUtilsMessengerEXT

句柄`VkDebugUtilsMessengerEXT`，对应结构体`VkDebugUtilsMessengerCreateInfoEXT`。

> 该句柄的创建和销毁接口需要运行期通过接口`vkGetInstanceProcAddr()`获得

#### 1.4.1 回调函数

启用`"VK_EXT_debug_utils"`扩展后Debug消息会调用回调函数，启用`"VK_LAYER_LUNARG_standard_validation"`层后Vulkan合法性检查相关内容也会以Debug消息的形式进行反馈。

## 2. 窗口

句柄`GLFWwindow*`，为GLFW库内容，需要开启相应的Instance Extension。

句柄`VkSurfaceKHR`，无对应结构体，创建依赖GLFW库的实现。

## 3. Device

### 3.2. Physical Device

句柄`VkPhysicalDevice`，无对应结构体。可从`VkInstance`中枚举，表示对应实例中所有支持的物理设备（显卡）。