---
layout: page
title: Vulkan Notes
date: 2020-01-08 16:15:10 +0800
mdate: 2020-01-08 16:15:10 +0800
---

- [1. 实例](#1-%e5%ae%9e%e4%be%8b)
  - [1.1. 实例层 &amp; 实例扩展](#11-%e5%ae%9e%e4%be%8b%e5%b1%82-amp-%e5%ae%9e%e4%be%8b%e6%89%a9%e5%b1%95)
  - [1.2. VkInstance](#12-vkinstance)
  - [1.3. VkDebugUtilsMessengerEXT](#13-vkdebugutilsmessengerext)
- [2. 窗口](#2-%e7%aa%97%e5%8f%a3)
- [3. 设备](#3-%e8%ae%be%e5%a4%87)
  - [3.2. 物理设备](#32-%e7%89%a9%e7%90%86%e8%ae%be%e5%a4%87)
    - [3.2.1. VkPhysicalDevice](#321-vkphysicaldevice)
    - [3.2.2. 设备属性 &amp; 设备特性](#322-%e8%ae%be%e5%a4%87%e5%b1%9e%e6%80%a7-amp-%e8%ae%be%e5%a4%87%e7%89%b9%e6%80%a7)
    - [3.2.3. 设备层 &amp; 设备扩展](#323-%e8%ae%be%e5%a4%87%e5%b1%82-amp-%e8%ae%be%e5%a4%87%e6%89%a9%e5%b1%95)
    - [3.2.4. 与窗口的兼容性](#324-%e4%b8%8e%e7%aa%97%e5%8f%a3%e7%9a%84%e5%85%bc%e5%ae%b9%e6%80%a7)
    - [3.2.5. 队列族](#325-%e9%98%9f%e5%88%97%e6%97%8f)
  - [3.3. 逻辑设备](#33-%e9%80%bb%e8%be%91%e8%ae%be%e5%a4%87)
    - [3.3.1. VkDevice](#331-vkdevice)
  - [3.4. 指令池](#34-%e6%8c%87%e4%bb%a4%e6%b1%a0)

## 1. 实例

### 1.1. 实例层 & 实例扩展

{:.tbl style="background-color:#EEC"}
|接口|功能|
|-|-|
| vkEnumerateInstanceLayerProperties() | 枚举所有VulkanRT支持的层 |
| vkEnumerateInstanceExtensionProperties() | 枚举所有VulkanRT支持的扩展 |

### 1.2. VkInstance

句柄`VkInstance`，对应结构体`VkInstanceCreateInfo`。

结构体内要提供**开启的实例层**{:.text-error}、**开启的实例扩展**{:.text-error}以及**结构体VkApplicationInfo**{:.text-error}。实例层以及实例扩展需要VulkanRT支持，结构体不包含重要信息。

> Vulkan的合法性检查需要开启`"VK_LAYER_LUNARG_standard_validation"`层\\
> GLFW窗口需要开启`glfwGetRequiredInstanceExtensions()`获得的扩展\\
> 启用调试需要开启`"VK_EXT_debug_utils"`扩展

### 1.3. VkDebugUtilsMessengerEXT

句柄`VkDebugUtilsMessengerEXT`，对应结构体`VkDebugUtilsMessengerCreateInfoEXT`。

> 该句柄的创建和销毁接口需要运行期通过接口`vkGetInstanceProcAddr()`获得

结构体内要提供**回调函数**{:.text-error}。启用`"VK_EXT_debug_utils"`扩展后Debug消息会调用回调函数，启用`"VK_LAYER_LUNARG_standard_validation"`层后Vulkan合法性检查相关内容也会以Debug消息的形式进行反馈。

## 2. 窗口

句柄`GLFWwindow*`，为GLFW库内容，需要开启相应的实例层。

句柄`VkSurfaceKHR`，无对应结构体，由GLFW库实现创建（依赖`GLFWwindow*`以及`VkInstance`）。

## 3. 设备

### 3.2. 物理设备

#### 3.2.1. VkPhysicalDevice

句柄`VkPhysicalDevice`，无对应结构体，由`VkInstance`枚举而得。

#### 3.2.2. 设备属性 & 设备特性

{:.tbl style="background-color:#EEC"}
|接口|功能|
|-|-|
| vkGetPhysicalDeviceProperties() | 获得所有物理设备的属性 |
| vkGetPhysicalDeviceFeatures() | 获得所有物理设备的特性 |

#### 3.2.3. 设备层 & 设备扩展

{:.tbl style="background-color:#EEC"}
|接口|功能|
|-|-|
| vkEnumerateDeviceLayerProperties() | 枚举所有物理设备支持的层 |
| vkEnumerateDeviceExtensionProperties() | 枚举所有物理设备支持的扩展 |

#### 3.2.4. 与窗口的兼容性

{:.tbl style="background-color:#EEC"}
|接口|功能|
|-|-|
| vkGetPhysicalDeviceSurfaceFormatsKHR() | 获得所有Surface支持的数据格式 |
| vkGetPhysicalDeviceSurfacePresentModesKHR() | 获得所有Surface支持的显示模式 |

#### 3.2.5. 队列族

队列族代表一系列Vulkan指令的集合。

{:.tbl style="background-color:#EEC"}
|接口|功能|
|-|-|
| vkGetPhysicalDeviceQueueFamilyProperties() | 获得物理设备的所有队列族 |

运行时任意设备获得的队列族信息是固定的，因此在需要使用队列族的地方往往用**索引**{:.text-error}来访问。

### 3.3. 逻辑设备

#### 3.3.1. VkDevice

句柄`VkDevice`，对应结构体`VkDeviceCreateInfo`。

结构体内要提供**开启的设备层**{:.text-error}、**开启的设备扩展**{:.text-error}、**开启的设备特性**{:.text-error}以及**结构体VkDeviceQueueCreateInfo列表**{:.text-error}。设备层、设备扩展以及设备特性需要物理设备支持，结构体列表用于从队列族创建队列。

每个结构体`VkDeviceQueueCreateInfo`内要提供**队列族的索引**{:.text-error}以及**该队列族创建的队列数量**{:.text-error}。

### 3.4. 指令池

TODO
