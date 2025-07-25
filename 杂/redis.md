# 缓存三兄弟

## 什么是缓存击穿、缓存穿透、缓存雪崩?

### 缓存穿透

缓存穿透是指查询不存在的数据，由于缓存没有命中（因为数据根本就不存在），请求每次都会穿过缓存去查询数据库。如果这种查询非常频繁，就会给数据库造成很大的压力。

解决方法：

①、**缓存空值/默认值**
如果数据库查询结果为空，将该空结果（如 null 或 {}）缓存起来，并设置一个合理的过期时间。当后续请求再访问相同 ID 时，缓存直接返回空结果，避免每次都打到数据库。

②、**布隆过滤器**

通过布隆过滤器存储所有可能存在的合法数据的键，当请求到达时，先通过布隆过滤器判断该键是否存在：

- 如果布隆过滤器认为该键不存在，直接返回空，不会查询数据库。
- 如果布隆过滤器认为该键可能存在，则查询缓存和数据库。

### 缓存击穿

缓存击穿是指某一个高频数据在某个时间过期，大量请求就会直接到达数据库，导致数据库瞬间压力过大。

①、加互斥锁更新，⽐如请求查询 A，发现缓存中没有，对 A 这个 key 加锁，同时去数据库查询数据，写⼊缓存，再返回给⽤户，这样后⾯的请求就可以从缓存中拿到数据了。

②、设置热点数据永远不过期。

③、将过期时间组合写在 value 中，通过异步的⽅式不断的刷新过期时间，防⽌此类现象。

### 缓存雪崩

缓存雪崩是指在某一个时间点大量的缓存数据同时过期或缓存服务器突然宕机了，导致所有的请求都落到了数据库上，从而对数据库造成巨大压力，甚至导致数据库崩溃的现象。

- 给不同的Key的TTL添加随机值
- 利用Redis集群提高服务的可用性
- 给缓存业务添加降级限流策略
- 给业务添加多级缓存


# 双写一致
## mysql的数据如何与redis进行同步呢？

 延时双删

 分布式锁

 异步通知保证数据最终一致

 基于Canal的异步通知

![image-20250319164822646](https://s2.loli.net/2025/03/19/KIJaxndPU8L9Qcj.png)

 ## 排他锁是如何保证读写、读读互斥的呢？

候选人：其实排他锁底层使用的也是`SETNX`，它保证了同时只能有一个线程操作锁住的方法。

使用Redisson实现读写锁。在读的时候添加共享锁，可以保证读读不互斥、读写互斥。当更新数据的时候，添加排他锁。它是读写、读读都互斥，这样就能保证在写数据的同时，是不会让其他线程读数据的，避免了脏数据。

## 你听说过延时双删吗？为什么不用它呢？

延迟双删，如果是写操作，我们先把缓存中的数据删除，然后更新数据库，最后再延时删除缓存中的数据。其中，这个延时多久不太好确定。在延时的过程中，可能会出现脏数据，并不能保证强一致性，所以没有采用它。

# 缓存持久化

## redis做为缓存，数据的持久化是怎么做的？

Redis 的持久化机制保证了 Redis 服务器在重启后数据不丢失，通过 RDB 和 AOF 文件来恢复内存中原有的数据。这两种持久化方式可以单独使用，也可以同时使用。

## 什么是RDB
RDB 持久化通过创建数据集的快照来工作，在指定的时间间隔内将 Redis 在某一时刻的数据状态保存到磁盘的一个 RDB 文件中。

![image-20250319165342718](https://s2.loli.net/2025/03/19/YPVhltKWmJa9gGr.png)

## 什么是AOF
AOF 持久化通过记录每个写操作命令并将其追加到 AOF 文件中来工作，恢复时通过重新执行这些命令来重建数据集。

![](https://s2.loli.net/2025/03/19/FTynC631qUYP4JA.png)

## **这两种方式，哪种恢复的比较快呢？**

候选人：RDB因为是二进制文件，保存时体积也比较小，所以它恢复得比较快。但它有可能会丢数据。我们通常在项目中也会使用AOF来恢复数据。虽然AOF恢复的速度慢一些，但它丢数据的风险要小很多。在AOF文件中可以设置刷盘策略。我们当时设置的就是每秒批量写入一次命令。


## RDB和AOF的区别？

RDB：快照方式，记录数据，文件小、恢复快，但可能丢数据。

AOF：日志方式，记录命令，文件大、恢复慢，但数据更安全。

# 数据过期和淘汰策略
## Redis的数据过期策略有哪些？

Redis 的 key 过期回收策略主要有两种：惰性删除和定期删除。

![image-20250319170535458](https://s2.loli.net/2025/03/19/Bpt2yAgqaJnFDMr.png)


## Redis的数据淘汰策略有哪些？
数据淘汰策略在redis中提供了很多种，默认是noeviction，不删除任何数据，内部不足时直接报错。这个可以在redis的配置文件中进行设置。里面有两个非常重要的概念：一个是LRU，另外一个是LFU。
- LRU的意思就是最少最近使用。它会用当前时间减去最后一次访问时间。这个值越大，则淘汰优先级越高。
- LFU的意思是最少频率使用。它会统计每个key的访问频率。值越小，淘汰优先级越高。
我们在项目中设置的是allkeys-lru，它会挑选最近最少使用的数据进行淘汰，把一些经常访问的key留在redis中。

![image-20250321163602095](https://s2.loli.net/2025/03/21/T3XHfpqLjFMkYa5.png)
## 关于数据淘汰策略其他的面试问题
![image-20250321163728469](https://s2.loli.net/2025/03/21/D32ytvXHZuNckn7.png)


# 分布式锁
## Redis分布式锁如何实现？
   在redis中提供了一个命令SETNX(SET if not exists)。由于redis是单线程的，用了这个命令之后，只能有一个客户端对某一个key设置值。在没有过期或删除key的时候，其他客户端是不能设置这个key的。


## 如何控制Redis实现分布式锁的有效时长呢？
## Redisson实现的分布式锁是可重入的吗？
## Redisson实现的分布式锁能解决主从一致性的问题吗？

![image-20250321163900400](https://s2.loli.net/2025/03/21/2FChbWeTxQtD3pq.png)


## 如果业务非要保证数据的强一致性，这个该怎么解决呢？

Redis本身就是支持高可用的，要做到强一致性，就非常影响性能，所以，如果有强一致性要求高的业务，建议使用ZooKeeper实现的分布式锁，它是可以保证强一致性的。


# redis集群

## Redis集群有哪些方案, 知道嘛

在Redis中提供的集群方案总共有三种
- 主从复制
- 哨兵模式
- 分片集群

## 介绍一下主从同步

单节点Redis的并发能力是有上限的，要进一步提高Redis的并发能力，可以搭建主从集群，实现读写分离。一般都是一主多从，主节点负责写数据，从节点负责读数据，主节点写入数据之后，需要把数据同步到从节点中。

## redis主从数据同步的流程是什么？

主从同步分为了两个阶段，一个是全量同步，一个是增量同步。

![image-20250321171338797](https://s2.loli.net/2025/03/21/S23PpEe5qv9yTHs.png)

## 哨兵模式的作用

Redis提供了哨兵（Sentinel）机制来实现主从集群的自动故障恢复。哨兵的结构和作用如下：

•监控：Sentinel 会不断检查您的master和slave是否按预期工作
•自动故障恢复：如果master故障，Sentinel会将一个slave提升为master。当故障实例恢复后也以新的master为主
•通知：Sentinel充当Redis客户端的服务发现来源，当集群发生故障转移时，会将最新信息推送给Redis的客户端


## 哨兵选主规则

首先判断主与从节点断开时间长短，如超过指定值就排该从节点
然后判断从节点的slave-priority值，越小优先级越高
如果slave-prority一样，则判断slave节点的offset值，越大优先级越高
最后是判断slave节点的运行id大小，越小优先级越高。

## 怎么保证Redis的高并发高可用？

首先可以搭建主从集群，再加上使用Redis中的哨兵模式，哨兵模式可以实现主从集群的自动故障恢复，里面就包含了对主从服务的监控、自动故障恢复、通知；如果master故障，Sentinel（心跳机制）会将一个slave提升为master。当故障实例恢复后也以新的master为主；同时Sentinel也充当Redis客户端的服务发现来源，当集群发生故障转移时，会将最新信息推送给Redis的客户端，所以一般项目都会采用哨兵的模式来保证Redis的高并

## 什么是Redis集群脑裂，该怎么解决呢？

在一个高可用集群中，当多个服务器在指定的时间内，由于网络的原因无法互相检测到对方，而各自形成一个新的小规模集群，并且各小集群当中，会选举新的master节点，都对外提供独立的服务，由于网络断裂的原因，一个高可用集群中，实际上分裂为多个小的集群，这种情况就称为裂脑。
关于解决的话，我记得在Redis的：第一可以设置最少的slave节点个数，比如设置至少要有一个从节点才能同步数据，第二个可以设置主从数据复制和同步的延迟时间，达不到要求就拒绝请求，就可以避免大量的数据丢失。

## 你们使用redis是单点还是集群，哪种集群？

一般使用的是主从（1主1从）加哨兵。一般单节点不超过10G内存，如果Redis内存不足则可以给不同服务分配独立的Redis主从节点。尽量不做分片集群。因为集群维护起来比较麻烦，并且集群之间的心跳检测和数据通信会消耗大量的网络带宽，也没有办法使用Lua脚本和事务。


## redis的分片集群有什么作用

主从和哨兵可以解决高可用、高并发读的问题。但是依然有两个问题没有解决：

•海量数据存储问题
•高并发写的问题

![image-20250321173041447](https://s2.loli.net/2025/03/21/Q2Nx35LqMCc468W.png)


## Redis分片集群中数据是怎么存储和读取的？

![image-20250321173057188](https://s2.loli.net/2025/03/21/PnmrHwu8OzIaWvj.png)

# redis底层
## Redis是单线程的，但是为什么还那么快？

1. 完全基于内存的，C语言编写。
2. 采用单线程，避免不必要的上下文切换和竞争条件。
3. 使用多路I/O复用模型，非阻塞IO。
例如：`BGSAVE`和`BGREWRITEAOF`都是在后台执行操作，不影响主线程的正常使用，不会产生阻塞。


## 解释一下I/O多路复用模型？

I/O多路复用是指利用单个线程来同时监听多个Socket，并且在某个Socket可读、可写时得到通知，从而避免无效的等待，充分利用CPU资源。目前的I/O多路复用都是采用的epoll模式实现，它会在通知用户进程Socket就绪的同时，把已就绪的Socket写入用户空间，不需要挨个遍历Socket来判断是否就绪，提升了性能。

其中Redis的网络模型就是使用I/O多路复用结合事件的处理器来应对多个Socket请求，比如，提供了连接应答处理器、命令回复处理器，命令请求处理器；

在Redis6.0之后，为了提升更好的性能，在命令回复处理器使用了多线程来处理回复事件，在命令请求处理器中，将命令的转换使用了多线程，增加命令转换速度，在命令执行的时候，依然是单线程