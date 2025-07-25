### `final` 和 `static` 的区别

| 特性       | `final`         | `static`     |
| -------- | --------------- | ------------ |
| **修饰对象** | 类、方法、变量         | 变量、方法        |
| **含义**   | 最终的、不可变的        | 静态的、属于类本身    |
| **类**    | 不能被继承           | -            |
| **方法**   | 不能被覆盖           | 可以被调用，但不能被覆盖 |
| **变量**   | 值不能被改变          | 属于类，所有实例共享   |
| **调用方式** | 通过实例调用          | 通过类名调用       |
| **初始化**  | 必须在声明时或构造方法中初始化 | 在类加载时初始化     |

### 常见面试问题

**final 和 static 可以同时修饰一个变量吗？**
- 可以。`final static` 修饰的变量是一个常量，属于类本身，所有实例共享。
- 示例：
```java
  class Constants {
      final static int MAX_VALUE = 100;
  }
```


**`final` 和 `static` 可以同时修饰一个方法吗？**

- **可以。** `final static` 修饰的方法是静态的，且不能被覆盖。
    
- **示例：**

```java
class MathUtils {
    final static int add(int a, int b) {
        return a + b;
    }
}```
**`final` 和 `static` 的区别是什么？**

- **`final`：** 表示不可变，用于修饰类、方法和变量，确保它们的定义或值不会被改变。
    
- **`static`：** 表示静态，用于修饰变量和方法，表示它们属于类本身，而不是类的某个实例。
    

**为什么 `final` 方法不能被覆盖？**

- `final` 方法不能被覆盖是为了确保子类不会改变父类方法的实现逻辑，保证父类方法的行为一致性。
    

**为什么 `static` 方法不能被覆盖？**

- `static` 方法属于类，而不是类的实例。覆盖（重写）是基于实例的多态特性，而 `static` 方法不依赖于实例，因此不能被覆盖。不过，`static` 方法可以被隐藏（通过子类定义同名方法）。
    

**`final` 和 `static` 的最佳实践是什么？**

- **`final`：** 用于定义不可变的类、方法和常量，提高代码的安全性和可读性。
    
- **`static`：** 用于定义类级别的变量和方法，减少实例之间的重复，提高效率。




 语法区别 
 1. **构造器**：抽象类能有构造器，接口不能有。 
 2. **成员变量** - 抽象类：有普通成员变量。 - 接口：无普通成员变量，定义的变量是 `public static final` 类型。 
 3. **方法** - 抽象类：可包含非抽象的普通方法，抽象方法访问类型可以是 `public`、`protected` 和默认访问权限。 - 接口：Java 8 前所有方法必须是抽象的，且只能是 `public`；Java 8 起可拥有默认方法（`default` 修饰）和类方法（`static` 修饰），Java 9 允许有 `private` 方法，后三者需有方法体。 
 4. **继承与实现**：一个类能实现多个接口，但只能继承一个抽象类。 
 5. 应用区别 
 - **接口**：主要在系统架构设计中起作用，体现一种规范。
 - **抽象类**：在代码实现方面发挥作用，可实现代码重用，如模板模式。






# &、&&、|、|| 运算符对比




## 优先级对比

### 按位运算符 vs 逻辑运算符

按位运算符（&、|）的优先级高于逻辑运算符（&&、||）。这意味着在表达式中，按位运算会先于逻辑运算进行计算。

### 逻辑运算符优先级顺序

逻辑运算符的优先级顺序为：! > && > ||。也就是说，逻辑非（!）的优先级最高，其次是逻辑与（&&），最后是逻辑或（||）。
## 短路行为差异

### && 和 ||

具有短路行为。当左侧操作数为假时，&&会跳过右侧操作数的评估；当左侧操作数为真时，||会跳过右侧操作数的评估。

### & 和 |

不具有短路行为。无论左侧操作数的值如何，右侧操作数总是会被评估。