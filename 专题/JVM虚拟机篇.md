![image-20250508180408448](https://s2.loli.net/2025/05/08/nN9m8OWsGhqzbQE.png)

## 1. JVM 的组成

- ClassLoader（类加载器）
  
- Runtime Data Area（运行时数据区，内存分区）
  
- Execution Engine（执行引擎）
  
- Native Method Library（本地库接口）



## 2. 类加载器
### 2.1 什么是类加载器，类加载器有哪些?

将**字节码文件加载到JVM中**


**类加载器种类**

类加载器根据各自加载范围的不同，划分为四种类加载器：

- **启动类加载器(BootStrap ClassLoader)：**
  
- 该类并不继承ClassLoader类，其是由C++编写实现。用于加载**JAVA_HOME/jre/lib**目录下的类库。
  
- **扩展类加载器(ExtClassLoader)：**
  
- 该类是ClassLoader的子类，主要加载**JAVA_HOME/jre/lib/ext**目录中的类库。
  
- **应用类加载器(AppClassLoader)：**
  
- 该类是ClassLoader的子类，主要用于加载**classPath**下的类，也就是加载开发者自己编写的Java类。
  
- **自定义类加载器：**
  
- 开发者自定义类继承ClassLoader，实现自定义类加载规则。
  



## 3. 垃圾收回

### 3.1 GC是什么？为什么要GC

### 3.2 垃圾收回算法

#### 1.引用计数法


#### 2.可达性分析算法



### 3.3 JVM 垃圾回收算法有哪些？

#### 1.标记清除算法

#### 2.复制算法

#### 3.标记整理算法

#### 4.分代收集算法



### 3.4 JVM 有哪些垃圾回收器？

#### 1.串行垃圾收集器

#### 2.并行垃圾收集器

#### 3.CMS（并发）垃圾收集器

#### 4.G1垃圾收集器



### 3.5 G1垃圾回收器




### 3.6 强引用、软引用、弱引用、虚引用的区别？




## 4. JVM实践（调优）