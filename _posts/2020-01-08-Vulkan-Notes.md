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
  - [3.1. 物理设备](#31-%e7%89%a9%e7%90%86%e8%ae%be%e5%a4%87)
    - [3.1.1. VkPhysicalDevice](#311-vkphysicaldevice)
    - [3.1.2. 设备属性 &amp; 设备特性](#312-%e8%ae%be%e5%a4%87%e5%b1%9e%e6%80%a7-amp-%e8%ae%be%e5%a4%87%e7%89%b9%e6%80%a7)
    - [3.1.3. 设备层 &amp; 设备扩展](#313-%e8%ae%be%e5%a4%87%e5%b1%82-amp-%e8%ae%be%e5%a4%87%e6%89%a9%e5%b1%95)
    - [3.1.4. 与窗口的兼容性](#314-%e4%b8%8e%e7%aa%97%e5%8f%a3%e7%9a%84%e5%85%bc%e5%ae%b9%e6%80%a7)
    - [3.1.5. 队列族](#315-%e9%98%9f%e5%88%97%e6%97%8f)
  - [3.2. 逻辑设备](#32-%e9%80%bb%e8%be%91%e8%ae%be%e5%a4%87)
    - [3.2.1. VkDevice](#321-vkdevice)
  - [3.3. 指令池](#33-%e6%8c%87%e4%bb%a4%e6%b1%a0)
- [4. 交换链](#4-%e4%ba%a4%e6%8d%a2%e9%93%be)
  - [4.1. VkSwapchainKHR](#41-vkswapchainkhr)
  - [4.2. VkImage](#42-vkimage)
  - [4.2. VkImageView](#42-vkimageview)
- [5. 流水线](#5-%e6%b5%81%e6%b0%b4%e7%ba%bf)
  - [5.1. 着色器](#51-%e7%9d%80%e8%89%b2%e5%99%a8)
    - [5.1.1. VkShaderModule](#511-vkshadermodule)
    - [5.1.2. VkPipelineShaderStageCreateInfo](#512-vkpipelineshaderstagecreateinfo)
  - [5.2. 固定状态](#52-%e5%9b%ba%e5%ae%9a%e7%8a%b6%e6%80%81)
    - [5.2.1. VkPipelineVertexInputStateCreateInfo](#521-vkpipelinevertexinputstatecreateinfo)
    - [5.2.2. VkPipelineInputAssemblyStateCreateInfo](#522-vkpipelineinputassemblystatecreateinfo)
    - [5.2.3. VkPipelineTessellationStateCreateInfo](#523-vkpipelinetessellationstatecreateinfo)
    - [5.2.3. VkPipelineViewportStateCreateInfo](#523-vkpipelineviewportstatecreateinfo)
    - [5.2.4. VkPipelineRasterizationStateCreateInfo](#524-vkpipelinerasterizationstatecreateinfo)
    - [5.2.5. VkPipelineMultisampleStateCreateInfo](#525-vkpipelinemultisamplestatecreateinfo)
    - [5.2.6. VkPipelineDepthStencilStateCreateInfo](#526-vkpipelinedepthstencilstatecreateinfo)
    - [5.2.7. VkPipelineColorBlendStateCreateInfo](#527-vkpipelinecolorblendstatecreateinfo)
    - [5.2.8. VkPipelineDynamicStateCreateInfo](#528-vkpipelinedynamicstatecreateinfo)
  - [5.3. 流水线布局](#53-%e6%b5%81%e6%b0%b4%e7%ba%bf%e5%b8%83%e5%b1%80)
  - [5.4. 渲染流程](#54-%e6%b8%b2%e6%9f%93%e6%b5%81%e7%a8%8b)

## 1. 实例

### 1.1. 实例层 & 实例扩展

{:.tbl style="background-color:#EEC"}
|接口|功能|
|-|-|
| vkEnumerateInstanceLayerProperties() | 枚举所有VulkanRT支持的层 |
| vkEnumerateInstanceExtensionProperties() | 枚举所有VulkanRT支持的扩展 |

### 1.2. VkInstance

句柄`VkInstance`，对应结构体`VkInstanceCreateInfo`。VulkanRT库初始化。

结构体内要提供**开启的实例层**{:.text-error}、**开启的实例扩展**{:.text-error}以及**结构体VkApplicationInfo**{:.text-error}。实例层以及实例扩展需要VulkanRT支持，结构体不包含重要信息。

> Vulkan的合法性检查需要开启`"VK_LAYER_LUNARG_standard_validation"`层\\
> GLFW窗口需要开启`glfwGetRequiredInstanceExtensions()`获得的扩展\\
> 启用调试需要开启`"VK_EXT_debug_utils"`扩展

### 1.3. VkDebugUtilsMessengerEXT

句柄`VkDebugUtilsMessengerEXT`，对应结构体`VkDebugUtilsMessengerCreateInfoEXT`。开启调试回调。

> 该句柄的创建和销毁接口需要运行期通过接口`vkGetInstanceProcAddr()`获得

结构体内要提供**回调函数**{:.text-error}。启用`"VK_EXT_debug_utils"`扩展后Debug消息会调用回调函数，启用`"VK_LAYER_LUNARG_standard_validation"`层后Vulkan合法性检查相关内容也会以Debug消息的形式进行反馈。

## 2. 窗口

句柄`GLFWwindow*`，为GLFW库内容，需要开启相应的实例层。

句柄`VkSurfaceKHR`，无对应结构体，由GLFW库实现创建（依赖`GLFWwindow*`以及`VkInstance`）。

## 3. 设备

### 3.1. 物理设备

#### 3.1.1. VkPhysicalDevice

句柄`VkPhysicalDevice`，无对应结构体，由`VkInstance`枚举而得。表示可用的GPU。

#### 3.1.2. 设备属性 & 设备特性

{:.tbl style="background-color:#EEC"}
|接口|功能|
|-|-|
| vkGetPhysicalDeviceProperties() | 获得所有物理设备的属性 |
| vkGetPhysicalDeviceFeatures() | 获得所有物理设备的特性 |

#### 3.1.3. 设备层 & 设备扩展

{:.tbl style="background-color:#EEC"}
|接口|功能|
|-|-|
| vkEnumerateDeviceLayerProperties() | 枚举所有物理设备支持的层 |
| vkEnumerateDeviceExtensionProperties() | 枚举所有物理设备支持的扩展 |

#### 3.1.4. 与窗口的兼容性

{:.tbl style="background-color:#EEC"}
|接口|功能|
|-|-|
| vkGetPhysicalDeviceSurfaceFormatsKHR() | 获得所有Surface支持的数据格式 |
| vkGetPhysicalDeviceSurfacePresentModesKHR() | 获得所有Surface支持的显示模式 |

#### 3.1.5. 队列族

队列族代表一系列Vulkan指令的集合。

{:.tbl style="background-color:#EEC"}
|接口|功能|
|-|-|
| vkGetPhysicalDeviceQueueFamilyProperties() | 获得物理设备的所有队列族 |

运行时任意设备获得的队列族信息是固定的，因此在需要使用队列族的地方往往用**索引**{:.text-error}来访问。

### 3.2. 逻辑设备

#### 3.2.1. VkDevice

句柄`VkDevice`，对应结构体`VkDeviceCreateInfo`。与Vulkan API交互的虚拟设备。

结构体内要提供**开启的设备层**{:.text-error}、**开启的设备扩展**{:.text-error}、**开启的设备特性**{:.text-error}以及**结构体VkDeviceQueueCreateInfo列表**{:.text-error}。设备层、设备扩展以及设备特性需要物理设备支持，结构体列表用于从队列族创建队列。

每个结构体`VkDeviceQueueCreateInfo`内要提供**队列族的索引**{:.text-error}以及**该队列族创建的队列数量**{:.text-error}。

> 如果创建成功`vkGetDeviceQueue()`接口可以获得队列的句柄

### 3.3. 指令池

句柄`VkCommandPool`，对应结构体`VkCommandPoolCreateInfo`。每个队列族需要一个指令池用以分配指令缓存。

结构体内要提供**队列族**{:.text-error}。

## 4. 交换链

### 4.1. VkSwapchainKHR

句柄`VkSwapchainKHR`，对应结构体`VkSwapchainCreateInfoKHR`。用于Vulkan图像和Surface交互。其管理了一个图像队列，并按一定规则将图像送至Surface用于显示。

结构体内要提供**Surface**{:.text-error}、**图像属性**{:.text-error}、**显示模式**{:.text-error}等内容。

图像属性包括：

{:.tbl style="background-color:#EEC"}
|属性|意义|
|-|-|
| minImageCount | 图像队列大小（需要在物理设备和Surface允许的范围内） |
| imageFormat | 图像每个像素的格式（需要物理设备和Surface支持） |
| imageColorSpace | 图像的颜色空间（需要物理设备和Surface支持） |
| imageExtent | 图像大小（与Surface管理的窗口大小相同） |
| imageArrayLayers | 图像层数，表示3D图像，取1则表示2D图像 |
| imageUsage | 图像用途（颜色缓存，深度缓存。。。） |
| imageSharingMode | 描述不同队列族的指令如何访问同一图像 |

显示模式（需要物理设备和Surface支持）包括：

{:.tbl style="background-color:#EEC"}
|属性|意义|
|-|-|
| VK_PRESENT_MODE_IMMEDIATE_KHR | 图像与Surface同步 |
| VK_PRESENT_MODE_MAILBOX_KHR | 图像与Surface通过图像队列异步；如果队列已满，之的提交会被覆盖 |
| VK_PRESENT_MODE_FIFO_KHR | 图像与Surface通过图像队列异步；如果队列已满，图像会等待Surface |
| VK_PRESENT_MODE_FIFO_RELAXED_KHR | 同上，但是如果队列为空，下一次提交会直接与Surface同步 |

### 4.2. VkImage

句柄`VkImage`，对应结构体`VkImageCreateInfo`（若由`VkSwapchainKHR`管理，则不通过该结构体创建）。用于描述Vulkan中的所有图像。

接口`vkGetSwapchainImagesKHR()`可直接获得图像队列中每张图像的句柄。

### 4.2. VkImageView

句柄`VkImageView`，对应结构体`VkImageViewCreateInfo`。`VkImage`中的内容不能直接访问，需要通过相应的`VkImageView`才能进行读写。

`VkImageView`有自己的像素格式，需要与对应`VkImage`的格式兼容。类似DX11中`ID3D11ShaderResourceView`的格式需要与对应的`ID3D11Texture2D`格式兼容。

`VkImageView`可进行通道映射，其每个通道都可以指定`VkImage`的任意一个通道。

`VkImageView`可只访问`VkImage`的一部分。包括部分连续的MipMap，部分连续层。

## 5. 流水线

句柄`VkPipeline`，对应结构体`VkGraphicsPipelineCreateInfo`或`VkComputePipelineCreateInfo`。描述流水线构成，可以是图形管线，也可以是计算管线。

描述图形管线的`VkPipeline`包括以下部分：

{:.tbl style="background-color:#EEC"}
|流水线组成|意义|
|-|-|
| 着色器（Shader Stage） | 可编程着色器 |
| 固定状态（Fixed State） | 不可编程但可配置的内容 |
| 流水线布局（Pipeline Layout） | 用于着色器访问外部数据 |
| 渲染流程（Render Pass） | 控制流水线的运行时行为 |

### 5.1. 着色器

Vulkan使用`SPIR-V`字节码作为SL。可以由HLSL、GLSL等直接编译而来。

#### 5.1.1. VkShaderModule

句柄`VkShaderModule`，对应结构体`VkShaderModuleCreateInfo`。作为`SPIR-V`字节码的容器。

#### 5.1.2. VkPipelineShaderStageCreateInfo

结构体`VkPipelineShaderStageCreateInfo`列表，描述`VkPipeline`中每个着色器阶段的`VkShaderModule`绑定信息，。

### 5.2. 固定状态

#### 5.2.1. VkPipelineVertexInputStateCreateInfo

结构体`VkPipelineShaderStageCreateInfo`，描述：

{:.tbl style="background-color:#EEC"}
| 顶点结构体描述列表 | std::vector&lt;VkVertexInputBindingDescription&gt; |
| 顶点属性描述列表 | std::vector&lt;VkVertexInputAttributeDescription&gt; |

流水线通过绑定槽（Bind）读取顶点数据，每个Bind用一个`VkVertexInputBindingDescription`描述，包括槽位号、每个顶点所占的空间以及该槽是逐顶点数据还是逐实例数据。

着色器通过`layout(location=xxx)`访问顶点数据，每个layout用一个`VkVertexInputAttributeDescription`描述，包括着色器内的位置、顶点所处的Bind、访问格式以及数据所在顶点结构体的偏移值。

#### 5.2.2. VkPipelineInputAssemblyStateCreateInfo

结构体`VkPipelineInputAssemblyStateCreateInfo`，描述光栅化时如何利用顶点组成图元。

#### 5.2.3. VkPipelineTessellationStateCreateInfo

TODO

#### 5.2.3. VkPipelineViewportStateCreateInfo

结构体`VkPipelineViewportStateCreateInfo`，描述视口以及剪刀。

{:.tbl style="background-color:#EEC"}
| 视口列表 | std::vector&lt;VkViewport&gt; |
| 剪刀列表 | std::vector&lt;VkRect2D&gt; |

视口描述如何从NDC映射到Frame Buffer，而剪刀描述了Frame Buffer的可见区域。

#### 5.2.4. VkPipelineRasterizationStateCreateInfo

结构体`VkPipelineRasterizationStateCreateInfo`，描述光栅化的配置：

{:.tbl style="background-color:#EEC"}
| depthClampEnable | 开启后，深度在远近平面以外会被截断 |
| rasterizerDiscardEnable | 开启后，流水线到此为止 |
| polygonMode | 多边形填充方案 |
| cullMode | 剔除方案 |
| frontFace | 正面规则 |

#### 5.2.5. VkPipelineMultisampleStateCreateInfo

TODO

#### 5.2.6. VkPipelineDepthStencilStateCreateInfo

TODO

#### 5.2.7. VkPipelineColorBlendStateCreateInfo

TODO

#### 5.2.8. VkPipelineDynamicStateCreateInfo

TODO

### 5.3. 流水线布局

### 5.4. 渲染流程
