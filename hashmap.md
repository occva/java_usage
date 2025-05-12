### [简述 Java 的 HashMap](https://javabetter.cn/interview/java-basic-baguwen.html#%E7%AE%80%E8%BF%B0-java-%E7%9A%84-hashmap)

JDK8 之前底层实现是数组 + 链表，JDK8 改为数组 + 链表/红黑树。
主要成员变量包括存储数据的 table 数组、元素数量 size、加载因子 loadFactor。
HashMap 中数据以键值对的形式存在，键对应的 hash 值用来计算数组下标，如果两个元素 key 的 hash 值一样，就会发生哈希冲突，被放到同一个链表上。

table 数组记录 HashMap 的数据，每个下标对应一条链表，所有哈希冲突的数据都会被存放到同一条链表，Node/Entry 节点包含四个成员变量：key、value、next 指针和 hash 值。在 JDK8 后链表超过 8且数值大于64 会转化为红黑树。查询效率从O(n)提升至O(log n)。

当元素数量超过capacity * loadFactor（默认0.75）时触发扩容。例如，默认容量16时，阈值为12。默认初始化容量为 16，扩容容量必须是 2 的幂次方、最大容量为 1<< 30 、默认加载因子为 0.75。

