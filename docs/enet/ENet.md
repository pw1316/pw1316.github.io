# 初始化

在使用Enet的功能之前要先初始化，在结束使用Enet后退出前要做清理

```
enet_initialize();
/* Add or Reference Network Code Here */
enet_deinitialize();
```

实际上以上两个函数在win32平台下才有意义，用于处理WSA和time

```
/* Needed when using winsock */
WSAStartUp(...)
WSACleanUp()

timeBeginPeriod(...)
timeEndPeriod(...)
```

# 使用

ENet的使用基于`ENetHost`，在通讯之前需要创建`ENetHost`实例

`enet_host_create()`新建一个`ENetHost`，可修改参数来定制

```
param const ENetAddress * address 绑定的地址
param size_t peerCount 管理的连接数
param size_t channelLimit 限制最大通道数，0代表不限制
param enet_uint32 incomingBandwidth 下行最大速率 Bytes/s
param enet_uint32 outgoingBandwidth 上行最大速率 Bytes/s

retval ENetHost* 新建的主机实例，失败的话返回NULL
```

`enet_host_destroy()`回收一个`ENetHost`实例，深回收

```
param ENetHost * host 需要回收的主机实例
```

## Callbacks

Callbacks封装了堆内存的分配操作

```
typedef struct _ENetCallbacks
{
    void * (ENET_CALLBACK * malloc) (size_t size);
    void (ENET_CALLBACK * free) (void * memory);
    void (ENET_CALLBACK * no_memory) (void);
} ENetCallbacks;
```

这个结构体中的函数指针指向自定义内存操作函数，默认值为`stdlib.h`下的`malloc`，`free`和`abort`

然后定义了两个接口`enet_malloc`和`enet_free`进一步封装结构体内函数的调用，这两个是实际使用的接口，而结构体被定义成静态的从而不允许外部直接访问

要构建自定义接口时使用接口`enet_initialize_with_callbacks`，传入自定义的结构体作为参数，Enet会在初始化之前更新静态结构体中的成员


## Lists

链表采用了侵入式链表，数据包等操作用链表实现，要加入链表的结构开头增加一个节点，减少增删节点时的消耗

## Packets

结构体`ENetPacket`记录的是除头部以外的数据，是上层数据收发的最小单位

```
typedef struct _ENetPacket
{
    size_t referenceCount;/* 引用计数，分片的时候一个Packet会被多个Command引用 */
    enet_uint32 flags;/* 控制信息 */
    enet_uint8 * data;/* 上层传下来的数据 */
    size_t dataLength;/* 数据长度 */
    ENetPacketFreeCallback freeCallback;/* 当该Packet被销毁之前会调用，用于添加调试信息，默认为NULL，需在创建之后手动赋值，或修改创建逻辑 */
    void * userData;/* 自定义数据，协议中不会用到，可本地记录用于调试 */
} ENetPacket;
```

关于控制信息，用枚举`ENetPacketFlag`表示，在创建时作为参数传入

```
typedef enum _ENetPacketFlag
{
    ENET_PACKET_FLAG_RELIABLE = (1 << 0),/* 发送后必须收到对方的ACK之后才算成功，否则超时后会重发 */
    ENET_PACKET_FLAG_UNSEQUENCED = (1 << 1),/* 这个Packet不会改变协议中的序号，在无序的状态收发，可靠包时该位无效 */
    ENET_PACKET_FLAG_NO_ALLOCATE = (1 << 2),/* 创建包的时候不会为数据新分配内存，直接使用原来的内存，释放包时不会释放data */
    ENET_PACKET_FLAG_UNRELIABLE_FRAGMENT = (1 << 3),/* 当这个包需要分片时采用非可靠的方式 */
    ENET_PACKET_FLAG_SENT = (1 << 8)/* 引用这个包的所有Command是否都已发送 */
} ENetPacketFlag;
```

ENet提供了符合`802.3`协议的CRC32算法`enet_crc32`，但是默认没有使用，要使用的话在创建`ENetHost`之后手动设置或者采用其它协议，用函数指针实现，只要符合

`typedef enet_uint32(ENET_CALLBACK * ENetChecksumCallback) (const ENetBuffer * buffers, size_t bufferCount);`即可

## Protocols

ENet通过`ENetProtocol`来标记协议类型，数据通信时是按照`ENetProtocol + Packet(Fragment)`的形式序列化的

具体协议类型分为以下几种：

`ENET_PROTOCOL_COMMAND_ACKNOWLEDGE`ACK  
`ENET_PROTOCOL_COMMAND_CONNECT`一次握手  
`ENET_PROTOCOL_COMMAND_VERIFY_CONNECT`二次握手  
`ENET_PROTOCOL_COMMAND_DISCONNECT`断开连接  
`ENET_PROTOCOL_COMMAND_PING`Ping  
`ENET_PROTOCOL_COMMAND_SEND_RELIABLE`发送可靠数据  
`ENET_PROTOCOL_COMMAND_SEND_UNRELIABLE`发送非可靠数据  
`ENET_PROTOCOL_COMMAND_SEND_FRAGMENT`发送分片数据  
`ENET_PROTOCOL_COMMAND_SEND_UNSEQUENCED`发送乱序数据  
`ENET_PROTOCOL_COMMAND_BANDWIDTH_LIMIT`调整带宽  
`ENET_PROTOCOL_COMMAND_THROTTLE_CONFIGURE`调整流量  
`ENET_PROTOCOL_COMMAND_SEND_UNRELIABLE_FRAGMENT`发送非可靠分片数据  

这些command具有统一的头部结构

    -------------------------------------------------
    |   0 -  7  |   8 - 15  |  16 - 23  |  24 - 31  |
    -------------------------------------------------
    |  command  | channelID |   reliableSeqNumber   |
    -------------------------------------------------

```
command /* 上述Enum中定义的值 */
channelID /* 发送的时候是对方的ID，接收的时候是自己的ID */
reliableSeqNumber /* 发送方的ReliableSeqNo */
```

后续部分根据协议具体需求添加了不同字段这里不细讲了

## Commands

虽然发送接收的时候是按`ENetProtocol + Packet(Fragment)`的形式，但是在本地缓存的时候是通过Command来存储的

Command分开保存了`ENetProtocol`和`ENetPacket`，同时还记录了一些额外信息

Command通过链表挂在`ENetPeer`下，Command分为in，out和ACK三类

```
typedef struct _ENetAcknowledgement
{
    ENetListNode acknowledgementList;/* 链表节点 */
    enet_uint32  sentTime;/* 对方的发送时间 */
    ENetProtocol command;/* 待回复的协议 */
    /* 没有Packet */
} ENetAcknowledgement;
```

```
typedef struct _ENetOutgoingCommand
{
    ENetListNode outgoingCommandList;/* 链表节点 */
    enet_uint16  reliableSequenceNumber;
    enet_uint16  unreliableSequenceNumber;/* 发送序号 */
    enet_uint32  sentTime;/* 发送时间，非可靠包无效 */
    enet_uint32  roundTripTimeout;/* 重发超时时间 */
    enet_uint32  roundTripTimeoutLimit;/* 断线超时时间 */
    enet_uint32  fragmentOffset;/* 片偏移量，Packet过大时用，否则为0 */
    enet_uint16  fragmentLength;/* 片长度，表示该Command下发送数据的实际长度 */
    enet_uint16  sendAttempts;/* 发送次数，每次重发该值+1 */
    ENetProtocol command;/* 待发送的协议 */
    ENetPacket * packet;/* 待发送的Packet，即使分片引用的也是整个包 */
} ENetOutgoingCommand;
```

```
typedef struct _ENetIncomingCommand
{
    ENetListNode     incomingCommandList;/* 链表节点 */
    enet_uint16      reliableSequenceNumber;
    enet_uint16      unreliableSequenceNumber;/* 接收序号 */
    ENetProtocol     command;/* 收到的协议 */
    enet_uint32      fragmentCount;/* 分片总数 */
    enet_uint32      fragmentsRemaining;/* 剩余片数 */
    enet_uint32 *    fragments;/* 数组用bit位记录哪些片已收到，当所有片的位都置1，表示这个包已收到 */
    ENetPacket *     packet;/* 收到的Packet，即使分片引用的也是整个包 */
} ENetIncomingCommand;
```

## Channels

序列化的数据都通过`ENetChannel`来转发，`ENetChannel`要记录各类有序包的序号，包括接收的和发送的

```
typedef struct _ENetChannel
{
    enet_uint16  outgoingReliableSequenceNumber;/* 发送可靠包(加入队列)前序号+1，send要指定channelID */
    enet_uint16  outgoingUnreliableSequenceNumber;/* 发送非可靠包(加入队列)前序号+1，如果发送了可靠包，该值重置，send要指定channelID */
    enet_uint16  usedReliableWindows;/* 一共16个可靠窗口，16位分别表示是否被使用 */
    enet_uint16  reliableWindows[ENET_PEER_RELIABLE_WINDOWS];/* 每个可靠窗口中ENetOutgoingCommand的数量，首次发包+1，收到ACK后-1 */
    enet_uint16  incomingReliableSequenceNumber;/* 收到可靠包被分到peer之前更新 */
    enet_uint16  incomingUnreliableSequenceNumber;/* 收到非可靠包被分到peer之前更新，如果分了可靠包到peer，该值重置 */
    ENetList     incomingReliableCommands;
    ENetList     incomingUnreliableCommands;/* 收到的包会首先挂在这个队列下面 */
} ENetChannel;
```

## Peers

所有和上层应用交互的数据都通过结构体`ENetPeer`，来收发，`ENetPeer`会向`ENetChannel`提交窗口信息，会从`ENetChannel`拿到待获得的数据

```
typedef struct _ENetPeer
{
    ENetListNode  dispatchList;/* 所有收到数据的ENetPeer会被挂在一个队列下统一分发 */
    struct _ENetHost * host;/* 所属的ENetHost */
    enet_uint16   outgoingPeerID;/* 建立连接后对方的PeerID */
    enet_uint16   incomingPeerID;/* 自己的PeerID，创建ENetHost时统一分配 */
    enet_uint32   connectID;/* 不同ENetHost的同序号ENetPeer用connectID区分，保证连接唯一；客户端允许同IP，但不允许同IP同端口同connectID */
    enet_uint8    outgoingSessionID;/* 握手的时候用，握手完之后和对方的incomingSessionID相等，发数据的时候带上 */
    enet_uint8    incomingSessionID;/* 握手的时候用，握手完之后和对方的outgoingSessionID相等，收数据的时候检查 */
    ENetAddress   address;/* 对方的地址和端口 */
    void *        data;/* 自由数据 */
    ENetPeerState state;/* ENetPeer状态 */
    ENetChannel * channels;/* 通道数组 */
    size_t        channelCount;/* 通道总数 */
    enet_uint32   incomingBandwidth;/* 对方的下行速率 bytes/second */
    enet_uint32   outgoingBandwidth;/* 对方的上行速率 bytes/second */
    enet_uint32   incomingBandwidthThrottleEpoch;
    enet_uint32   outgoingBandwidthThrottleEpoch;/* 上次发生限流计算的时间 */
    enet_uint32   incomingDataTotal;/* 收到的总字节数，收到的时机在sock_receive后dispatch前，限流计算后清零，peer重置时清零 */
    enet_uint32   outgoingDataTotal;/* 发送的总字节数，发送的时机在enet_send后queue前，限流计算后清零，peer重置时清零 */
    enet_uint32   lastSendTime;/* 最近一次发送时间，时机在sock_send前，peer重置时清零 */
    enet_uint32   lastReceiveTime;/* 最近一次收到ACK的时间，时机在sock_receive后，peer重置时清零 */
    enet_uint32   nextTimeout;/* 处在队列首部的Command的超时时间，peer重置时清零 */
    enet_uint32   earliestTimeout;/* 所有超时的Command中最早的发送时间，处理ACK时清零，peer重置时清零 */
    enet_uint32   packetLossEpoch;/* 最近一次计算丢包率的时间，时机在queue后sock_send前，peer重置时清零 */
    enet_uint32   packetsSent;/* 连Command带挂着的packet算一个，计算丢包率后清零，重发的再次计算 */
    enet_uint32   packetsLost;/* 连Command带挂着的packet算一个，计算丢包率后清零，重发的再次计算 */
    enet_uint32   packetLoss;/* 平均丢包率 */
    enet_uint32   packetLossVariance;/* 丢包率方差 */
    /* ENet主动丢非可靠包 */
    enet_uint32   packetThrottle;
    enet_uint32   packetThrottleLimit;
    enet_uint32   packetThrottleCounter;
    enet_uint32   packetThrottleEpoch;
    enet_uint32   packetThrottleAcceleration;
    enet_uint32   packetThrottleDeceleration;
    enet_uint32   packetThrottleInterval;
    /* ENet主动丢非可靠包 */
    /* ENet被动丢可靠包 */
    enet_uint32   pingInterval;
    enet_uint32   timeoutLimit;/* 32 */
    enet_uint32   timeoutMinimum;/* 5000 */
    enet_uint32   timeoutMaximum;/* 30000(5000 in PM02) */
    enet_uint32   lastRoundTripTime;
    enet_uint32   lowestRoundTripTime;
    enet_uint32   lastRoundTripTimeVariance;
    enet_uint32   highestRoundTripTimeVariance;
    enet_uint32   roundTripTime;/* 平均RTT */
    enet_uint32   roundTripTimeVariance;/* RTT方差 */
    /* ENet被动丢可靠包 */
    enet_uint32   mtu;
    enet_uint32   windowSize;
    enet_uint32   reliableDataInTransit;
    enet_uint16   outgoingReliableSequenceNumber;
    ENetList      acknowledgements;
    ENetList      sentReliableCommands;
    ENetList      sentUnreliableCommands;
    ENetList      outgoingReliableCommands;
    ENetList      outgoingUnreliableCommands;
    ENetList      dispatchedCommands;
    int           needsDispatch;
    enet_uint16   incomingUnsequencedGroup;
    enet_uint16   outgoingUnsequencedGroup;
    enet_uint32   unsequencedWindow[ENET_PEER_UNSEQUENCED_WINDOW_SIZE / 32];
    enet_uint32   eventData;
    size_t        totalWaitingData;/* dispatchedCommands下所有Packet的字节总数 */
} ENetPeer;
```

Peer的状态：

`ENET_PEER_STATE_DISCONNECTED`初始状态  
`ENET_PEER_STATE_CONNECTING`一次握手  
`ENET_PEER_STATE_ACKNOWLEDGING_CONNECT`二次握手  
`ENET_PEER_STATE_CONNECTION_PENDING`被连接方没有event接收CONNECT事件  
`ENET_PEER_STATE_CONNECTION_SUCCEEDED`连接方没有event接收CONNECT事件  
`ENET_PEER_STATE_CONNECTED`连接建立  
`ENET_PEER_STATE_DISCONNECT_LATER`收完ACK并发完非可靠包后开始挥手  
`ENET_PEER_STATE_DISCONNECTING`一次挥手  
`ENET_PEER_STATE_ACKNOWLEDGING_DISCONNECT`收到可靠挥手包  
`ENET_PEER_STATE_ZOMBIE`奇怪的状态  

## Hosts

`ENetHost`管理了一系列Peers，给Peers提供底层环境支持，负责将Peer上的数据传给应用

```
typedef struct _ENetHost
{
    ENetSocket           socket;
    ENetAddress          address;/* 本主机地址 */
    enet_uint32          incomingBandwidth;/* 下行速率 bytes/second */
    enet_uint32          outgoingBandwidth;/* 上行速率 bytes/second */
    enet_uint32          bandwidthThrottleEpoch;
    enet_uint32          mtu;/*最大传输单元，默认1400 */
    enet_uint32          randomSeed;/* 分配connectID用 */
    int                  recalculateBandwidthLimits;/* 在带宽限流时标记带宽是否要重新计算，有新连接或断开连接时 */
    ENetPeer *           peers;
    size_t               peerCount;
    size_t               channelLimit;/* 每个Peer允许的最大channel数 */
    enet_uint32          serviceTime;/* 当前时间，host以下的对象获取时间从这里读，host本身从系统读，单位毫秒 */
    ENetList             dispatchQueue;/* 有数据的Peer挂在这个队列下，数据由Host传给应用 */
    int                  continueSending;/* 一个窗口满了但是还有包没发出去时置1，表示还要继续发送 */
    size_t               packetSize;/* 某次发送中一共缓存的字节数，用于和mtu比较判断是否可以再加新包进来 */
    enet_uint16          headerFlags;/* 某次发送的头部标记，包括是否要带发送时间，是否压缩等，发送时存放在peerId的高16位中 */
    /* UDP发送Buffer */
    ENetProtocol         commands[ENET_PROTOCOL_MAXIMUM_PACKET_COMMANDS];
    size_t               commandCount;
    ENetBuffer           buffers[ENET_BUFFER_MAXIMUM];
    size_t               bufferCount;
    /* UDP发送Buffer */
    ENetChecksumCallback checksum;/* 校验和 */
    ENetCompressor       compressor;/* 压缩 */
    enet_uint8           packetData[2][ENET_PROTOCOL_MAXIMUM_MTU];/* 0用来缓存sock_recv的数据报，1用来缓存压缩解压缩的结果 */
    ENetAddress          receivedAddress;/* 传给指定Peer的对方地址，如果未建立连接则用于通知，如果已建立则用于校验 */
    enet_uint8 *         receivedData;/* 未压缩则软链到packetData[0]，压缩则软链到packetData[1] */
    size_t               receivedDataLength;/* 收到数据长度 */
    enet_uint32          totalSentData;/* 发送的字节数，不会定期清零，要手动处理 */
    enet_uint32          totalSentPackets;/* 发送的包数，Host级别的包指一次发送的Peer级别包的集合，不会定期清零，要手动处理 */
    enet_uint32          totalReceivedData;/* 收到的字节数，不会定期清零，要手动处理 */
    enet_uint32          totalReceivedPackets;/* 收到的包数，Host级别的包，不会定期清零，要手动处理 */
    ENetInterceptCallback intercept;/* 默认解包方法，如果忽略则按ENet自带的方法解包 */
    size_t               connectedPeers;/* 活跃连接数 */
    size_t               bandwidthLimitedPeers;/* 限制了带宽的连接数 */
    size_t               duplicatePeers;/* 允许同IP的peer数 */
    size_t               maximumPacketSize;/* 应用层单次发送数据限制32MB */
    size_t               maximumWaitingData;/* Host缓存的应用层数据最大限制32MB */
    char                 kcpBuffer[ENET_KCP_BUFF_SIZE];
    ENetList             kcpDispatchQueue;
} ENetHost;
```

### 地址信息

`ENetAddress`结构体记录了主机的地址信息，包括源IP(host)和源端口(port)：

    -----------------------------------------
    |  0 -  7 |  8 - 15 | 16 - 23 | 24 - 31 |
    -----------------------------------------
    |        host       |        port       |
    -----------------------------------------
    
该结构体表示对方若要对该`ENetHost`发起通信时所使用的地址，如果`ENetHost`内该结构体指针为`NULL`，则不允许被连接，而只能发起连接

`host`为`ENET_HOST_ANY(0)`时，内核会获取本机的一个IP，如果不为`0`，则使用指定地址

`port`为`0`时，内核会随机分配一个可用的端口给，如果不为`0`,则使用指定端口

允许被连接的`SOCKET`还需要`bind()`操作

### 网络数据处理

`enet_host_connect()`用于向指定地址发起连接

`enet_peer_disconnect()`用于发起断开请求，清空队列并发送挥手消息

`enet_peer_disconnect_later()`不清空队列，拒绝再发送数据，所有可靠包的ACK收到，所有非可靠包发送完后执行`enet_peer_disconnect()`

`enet_peer_disconnect_now()`清空队列并发一个无序的挥手消息，之后回收该Peer的资源

`enet_peer_send()`可将指定应用层数据加入队列

`enet_host_service()`处理所有网络层逻辑，`serviceTime`记录了上一次调用接口的时间，并在Host有数据时调用`enet_peer_receive()`返回给应用层

ENet是基于队列的数据包分发机制，队列操作由`enet_host_service(host, event, timeout)`驱动，以host为单位，返回事件，其余接口用于应用层和ENet交互

`timeout`可指定阻塞时间或用`0`表示非阻塞

### 整个处理逻辑：

1. Dispatch：`event != NULL`才执行，可返回`1`或`-1`
2. UpdateTime：更新Host时间
3. BandwidthThrottle：Host整体带宽限制，给Peer发`BANDWIDTH_LIMIT`的Protocol
4. SendOut：清空发送队列，可返回`1`或`-1`
5. RecvIn：读数据加到收取队列，可返回`1`或`-1`
6. SendOut：清空发送队列，可返回`1`或`-1`
7. Dispatch：`event != NULL`才执行，可返回`1`或`-1`
8. CheckTimeout：可返回`0`
9. UpdateTime：更新Host时间
10. Select：可返回`-1`
11. 如果Select被打断，回到9
12. 如果ReadSet不为空，回到3
13. 如果ReadSet为空，结束，返回`0`

#### 关于返回值：

1：有事件，传入event的话可以读

0：无事件

-1：出错

#### Dispatch

某个`ENetPeer`上有消息要通知应用层时，要将自己加入`ENetHost`的分发队列`dispatchQueue`，由`ENetHost`统一处理消息发给应用层

消息类型根据`ENetPeer`的状态而不同

`CONNECTION_PENDING CONNECTION_SUCCEEDED`：生成`CONNECT`事件

`ZOMBIE`：重置`ENetPeer`并生成`DISCONNECT`事件

`CONNECTED`：根据`ENetPeer`上是否有新的Packet，__Receive__并生成`RECEIVE`事件或忽略。如果`RECEIVE`事件后仍有新Packet，该`ENetPeer`会被再添加到`dispatchQueue`尾部等待再次Dispatch

`OTHERS`：忽略

##### Receive

`ENetPeer`的命令队列`dispatchedCommands`缓存了应用层数据包，头部出队列并返回其Packet部分，回收相应资源

#### BandwidthThrottle

限制带宽的接口，当循环调用`enet_host_service`时，每过一段时间会调用一次，用来限制已连接的`ENetPeer`的流量，时间间隔由`ENET_HOST_BANDWIDTH_THROTTLE_INTERVAL`指定

如果`ENetHost`限制了上行带宽，计算自上次调用以来：

1. 理论上能上行的最大数据
2. 实际每个`ENetPeer`的上行数据之和

然后开始循环调整(存在连接上的`ENetPeer`且需要调整的`flag == 1`)

1. 实际上行比理论上行大时，将门限`throttle`按比例缩小
2. 遍历所有`ENetPeer`，排除掉未连接的，不限下行的，已经被调整过的
3. 计算自上次调用以来该`ENetPeer`理论上能下行的最大数据
4. 若缩放过上行数据不超过下行限制，就跳过
5. TODO

#### SendOut

遍历当前`ENetHost`下的所有`ENetPeer`，并过滤掉`DISCONNECTED`和`ZOMBIE`状态的

构建发送Buffer，按照Header + Protocol1 + Packet1 + Protocol2 + Packet2 + Protocol3 + Packet3 +...

有的Protocol可能不包含Packet，单次发送Protocol的上限为32个

1. 缓存ACK
2. 检查是否发包超时(重传或直接断开连接)，可通过参数忽略此步
3. 缓存可靠包
4. 缓存Ping(没可靠包要缓存时)
5. 缓存非可靠包
6. 统计丢包率
7. 缓存头部，包括发送时间，CRC
8. 有压缩的话格式化
9. 给头部的PeerID附加信息
10. SocketSend

`peerID`记录了对方Peer的ID

最高位标记是否记录发送时间，次高位标记之后的数据是否压缩，再后2位标记自己的`outgoingSessionID`，低12位是实际ID

`4095`被用来标记未建立连接，因此单个Host理论上支持最多4094个Peer

##### ACK

`DISCONNECT`的ACK会Dispatch一个`ZOMBIE`状态

##### CheckTimeout

插入位置为发送队列头部

超时的可靠包加回发送队列，超时时间变为2倍，超过限制的直接返回离线事件

##### Reliable

窗口号为`序列号 / 可靠窗口大小(4096)`

1. 首次发送 && 不是该窗口的第一个序号 && (前一个可靠窗口塞了超过4096个可靠包 || 当前窗口起后8个窗口有被使用的) 就不允许发有通道的可靠包(连接请求channelID为255不受影响)(可靠窗口的大小是指使用该窗口的可靠包数，被使用的周期从首次发送开始，到收到ACK为止)
2. Peer的窗口大小用限流系数修正，如果算上当前Packet，字节数超过修正的窗口大小和mtu的最大值，不允许发带数据的可靠包(peer->windowSize指的是所有Data的大小，host->mtu指的是所有Data+Command的大小)
3. 有可靠包要发了就不需要Ping
4. 如果使用的Buffer数量超限制，或Command+Packet的字节数超过剩余可用字节数，当前次SendOut结束，并标记还要继续SendOut
5. 超时时间为RTT + 4 * RTTVar，断开时间为超时时间的32倍(32可配)

##### Unreliable

1. 如果使用的Buffer数量超限制，或Command+Packet的字节数超过剩余可用字节数，当前次SendOut结束，并标记还要继续SendOut
2. 带Packet的包可能被丢掉，以限流系数与32的商为保留概率
3. 如果丢掉的话会把之后序号相等的一串包都丢掉(可靠序号和不可靠序号都相等)
4. `DISCONNECT_LATER`的检查能不能断开

#### RecvIn

循环收256遍

读到的数据缓存在`packetData[0]`中，如果定义了`intercept`回调，则调用该回调，否则正常处理收包

1. 从数据头中解包解出相关信息
2. 如果压缩了，解压缩到原始数据；如果包含了CRC信息，进行CRC校验
3. 从剩下的数据中逐条解成一个个数据包
4. 根据`Command`的内容对这个包执行对应的处理
5. 最后如果这个包需要回复，把相应的ACK包加入发送队列

最后一个包如果不完整会抛错

##### ACKNOWLEDGE

更新限流系数，更新RTT，根据发送序号和通道号找到对应的Command，移出队列，释放对应可靠窗口

##### CONNECT

更新流量管控参数，QUEUE一个`VERIFY_CONNECT`包

##### VERIFY_CONNECT

移除序号1，通道255的Command(CONNECT)，更新流量管控参数，返回CONNECT事件

##### DISCONNECT

检查是否要发ACK，一般Dispatch一个ZOMBIE

##### SEND

检查通道号，分片的检查是否第一片，无序TODO，加入Channel的Incoming队列

检查能否使用Protocol里的序列号，如果收到包或收到所有分片就移到DispatchedQueue

##### BANDWIDTH_LIMIT

修改带宽，调整Data窗口大小

##### THROTTLE_CONFIGURE

修改周期，加减速度

### enet_host_connect

#### Client DISCONNECTED -> CONNECTING

握手需要发送`CONNECT`包，其结构如下：

    ---------------------------------------------------------------------------------
    |       0 -  7      |       8 - 15      |      16 - 23      |      24 - 31      |
    ---------------------------------------------------------------------------------
    |      command      |     channelID     |         reliableSequenceNumber        |
    ---------------------------------------------------------------------------------
    |            outgoingPeerID             | incomingSessionID | outgoingSessionID |
    ---------------------------------------------------------------------------------
    |                                      mtu                                      |
    ---------------------------------------------------------------------------------
    |                                  windowSize                                   |
    ---------------------------------------------------------------------------------
    |                                 channelCount                                  |
    ---------------------------------------------------------------------------------
    |                               incomingBandwidth                               |
    ---------------------------------------------------------------------------------
    |                               outgoingBandwidth                               |
    ---------------------------------------------------------------------------------
    |                            packetThrottleInterval                             |
    ---------------------------------------------------------------------------------
    |                           packetThrottleAcceleration                          |
    ---------------------------------------------------------------------------------
    |                           packetThrottleDeceleration                          |
    ---------------------------------------------------------------------------------
    |                                   connectID                                   |
    ---------------------------------------------------------------------------------
    |                                     data                                      |
    ---------------------------------------------------------------------------------

`command`数据包类型，低4位表示对应类型的枚举值，这里是`ENET_PROTOCOL_COMMAND_CONNECT`；高2位是控制信息，最高位表示是否需要ACK，次高位表示是否乱序，这里是`bits 10`

`channelID`该包使用的通道，在没有建立连接时该值为`0xFF`，因此通道数最大为`255`，最大可用ID为`254`

`reliableSequenceNumber`序列号，用于可靠传输，初始值0，发送时设为1

`outgoingPeerID`自己的peerID，初始化时会根据自身在表中的位置获得一个ID，存在`ENetPeer.incomingPeerID`中

`incomingSessionID`，`outgoingSessionID`建立连接前为255，建立连接后双方的In-Out，Out-In要对应

`mtu`这里记录的是所属host的mtu

`windowSize`发送Data窗口大小，根据host的上行速率来决定，这里的标准是64KB/s的上行分配4KB的窗口大小，按比例缩放

`channelCount`用于通知对方要分配的通道数，和自己本地的通道数相同

`incomingBandwidth`，`outgoingBandwidth`，本host的上下速率

`packetThrottleInterval`，`packetThrottleAcceleration`，`packetThrottleDeceleration`通知peer上限流的时间间隔，加速度和减速度

`connectID`连接号，由host里的一个随机数生成

`data`自定义数据

整个`CONNECT`包会被挂在`ENetOutgoingCommand`结构体下，同时的附加信息包括`序列号，发送时间，超时信息，分片信息，发送次数，数据包下的Data`。peer下的链表以`ENetOutgoingCommand`为单元存取

#### Server DISCONNECTED -> ACKNOWLEDGING_CONNECT

host允许不同端口同一IP的连接，如果是同IP同端口，或该IP已存在的连接数超过限制，就不响应，客户端之后会自行超时并断线

收到握手包时，读包内头部信息，遍历peers表找一个`DISCONNECTED`状态的peer，更新其信息

1. 通道数与包内的相等
2. `connectID`两边相等，之后的包如果不相等直接忽略
3. 对方的`peerID`存在`outgoingPeerID`中
4. `peer->incomingBandwidth`是下行速率，`peer->outgoingBandwidth`是上行速率，(peer里存的是反的)
5. 限流信息和对方相同
6. `sectionID`根据收到包而循环递增，取值`[0, 3]`，连接时默认`0xFF`无效信息，从0开始
7. 初始化`channel`
8. mtu双方共享
9. `peer->windowSize`代表本peer的发送窗口大小，数据包里有对方的下行速率可计算对方接受窗口大小，取两者较小值
10. 根据本地host的下行速率，计算接受窗口大小，根据数据包里的`windowSize`，计算实际接收窗口大小，这个值需要回传
11. 二次握手

二次握手需要发送`VERIFY_CONNECT`包，其结构如下：

    ---------------------------------------------------------------------------------
    |       0 -  7      |       8 - 15      |      16 - 23      |      24 - 31      |
    ---------------------------------------------------------------------------------
    |      command      |     channelID     |         reliableSequenceNumber        |
    ---------------------------------------------------------------------------------
    |            outgoingPeerID             | incomingSessionID | outgoingSessionID |
    ---------------------------------------------------------------------------------
    |                                      mtu                                      |
    ---------------------------------------------------------------------------------
    |                                  windowSize                                   |
    ---------------------------------------------------------------------------------
    |                                 channelCount                                  |
    ---------------------------------------------------------------------------------
    |                               incomingBandwidth                               |
    ---------------------------------------------------------------------------------
    |                               outgoingBandwidth                               |
    ---------------------------------------------------------------------------------
    |                            packetThrottleInterval                             |
    ---------------------------------------------------------------------------------
    |                           packetThrottleAcceleration                          |
    ---------------------------------------------------------------------------------
    |                           packetThrottleDeceleration                          |
    ---------------------------------------------------------------------------------
    |                                   connectID                                   |
    ---------------------------------------------------------------------------------

`command`取`ENET_PROTOCOL_COMMAND_VERIFY_CONNECT | ENET_PROTOCOL_COMMAND_FLAG_ACKNOWLEDGE`

`channelID`这里也是没建立连接用`0xFF`表示

`reliableSequenceNumber`是Server的序号，初始也从1开始

其它项目根据之前收到的数据包更新的peer信息，填写相应的host或peer中对应的值

`sectionID`这里填的是Client的值，因此发送的时候和Server的值是反的(`CONNECT`发送的也是Client的值，发送的时候和Client相同)

`windowSize`这里填的是本peer接收窗口的大小(`CONNECT`包里该字段填的是发送窗口大小)

`data`项被去掉

由于之前的`CONNECT`包带有ACK的flag，按理是应该再生成一个ACK包的，这里直接忽略掉了

#### Client CONNECTING -> CONNECTED

这个时候可以给Client的地址信息赋值了，收到了Server消息后能拿到Server的IP和Port，记录下来

如果双方的通道数，限流信息等不一致，就会进入`ZOMBIE`状态

由于Server并没有发送ACK过来，Client这里要手动ACK，把之前的`CONNECT`从等待回复队列中删除

用数据包里的`windowSize`更新自己的，这样双方的发送窗口都能保证速率不会超过两端的上下行速率限制

然后Client会生成一个`CONNECTED`的事件，如果传入`event == NULL`，会进入`SUCCEEDED`状态等待dispatch

由于的`VERIFY_CONNECT`包带有ACK的flag，所以要生成一个ACK包。本来这个ACK能在当前`enet_host_service`的调用周期内发掉的，但是由于事件的产生，提前结束了调用周期，所以ACK要在下个周期内才能被发送

ACK要发送`ACKNOWLEDGE`包，其结构如下：

    ---------------------------------------------------------------------------------
    |       0 -  7      |       8 - 15      |      16 - 23      |      24 - 31      |
    ---------------------------------------------------------------------------------
    |      command      |     channelID     |         reliableSequenceNumber        |
    ---------------------------------------------------------------------------------
    |     receivedReliableSequenceNumber    |            receivedSentTime           |
    ---------------------------------------------------------------------------------

`command`为`ENET_PROTOCOL_COMMAND_ACKNOWLEDGE`且这个包不需要被ACK

`channel`为`VERIFY_CONNECT`里的值

`reliableSequenceNumber`是对方的发送序号

`receivedReliableSequenceNumber`是自己收到的序号，这里和对方发送的相同

`receivedSentTime`对方数据包的发送时间

ACK`DISCONNECT`会发peer异常

#### Server ACKCONNECTING -> CONNECTED

之前Server已经记录过了Client的信息，这里只是个确认，做的事有，计算RTT，调整Throttle，更新统计信息。
