# **🚀 PyOxidizer 详细介绍**



**PyOxidizer** 是一个用于 **将 Python 应用程序打包成独立的可执行文件**的工具，目标是创建一个**无需依赖 Python 运行环境**的可执行文件（EXE、Mac/Linux 可执行文件），类似于 **PyInstaller**，但性能更强大，基于 **Rust** 语言构建。



------



**🎯 PyOxidizer 的核心作用**

| **作用**               | **解释**                                                   |
| ---------------------- | ---------------------------------------------------------- |
| **打包 Python 应用**   | 生成一个 **完全独立** 的二进制可执行文件（无 Python 依赖） |
| **高性能**             | 直接在 Rust 内部加载 Python 代码，比 PyInstaller 更快      |
| **跨平台支持**         | 支持 Windows、Linux、macOS                                 |
| **支持 Rust + Python** | 可以在 Rust 项目中嵌入 Python                              |
| **减少体积**           | 生成更小的可执行文件                                       |
| **安全性更高**         | 避免暴露 Python 源代码                                     |





------



**🔧 PyOxidizer 的安装**



PyOxidizer 依赖 **Rust**，因此需要先安装 Rust：



**1️⃣ 安装 Rust**

```
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

**2️⃣ 安装 PyOxidizer**



可以使用 **Cargo**（Rust 的包管理器）安装：

```
cargo install pyoxidizer
```

安装完成后，使用 pyoxidizer --help 进行测试：

```
pyoxidizer --help
```





------



**📁 PyOxidizer 项目结构**



在项目目录中使用：

```
pyoxidizer init my_project
```

会生成如下目录结构：

```
my_project/
├── pyoxidizer.bzl  # PyOxidizer 配置文件（核心）
├── build/          # 编译输出目录
└── src/            # Python 源码目录
```

​	•	**pyoxidizer.bzl**：PyOxidizer 的 **构建配置文件**，控制 Python 代码的打包方式。

​	•	**src/**：存放你的 Python 源代码（如 main.py）。

​	•	**build/**：生成的可执行文件目录。



------



**🚀 PyOxidizer 快速示例**



假设我们有一个简单的 main.py：

```
# src/main.py
print("Hello, PyOxidizer!")
```

**1️⃣ 配置 pyoxidizer.bzl**



编辑 pyoxidizer.bzl，定义如何构建应用：

```
def make_python_distribution():
    return default_python_distribution()

def make_embedded_python_config():
    return default_embedded_python_config()

def make_application():
    python_config = make_embedded_python_config()
    policy = python_config.to_execution_policy()
    
    # 创建可执行文件
    return policy.to_python_packaging_policy()
```

**2️⃣ 运行构建**

```
pyoxidizer build
```

如果成功，会在 build/ 目录下生成一个 **独立可执行文件**，无需安装 Python 也能运行！



**3️⃣ 运行可执行文件**

```
./build/my_project  # Linux/macOS
build\my_project.exe  # Windows
```

输出：

```
Hello, PyOxidizer!
```





------



**🔥 PyOxidizer vs PyInstaller 对比**

| **特性**               | **PyOxidizer** **🦀**       | **PyInstaller** **🐍**        |
| ---------------------- | -------------------------- | ---------------------------- |
| **打包方式**           | 直接编译为 Rust 可执行文件 | 生成 Python 解释器 + Py 文件 |
| **依赖 Python 运行时** | ❌ 无需依赖                 | ✅ 需要 Python 运行环境       |
| **执行速度**           | 🚀 更快                     | 🐢 略慢                       |
| **可执行文件大小**     | 🔥 较小（几 MB）            | 📦 较大（几十 MB）            |
| **跨平台支持**         | ✅ Windows/Linux/macOS      | ✅ Windows/Linux/macOS        |
| **安全性**             | ✅ 代码更难反编译           | ❌ Python 代码可被反编译      |

✅ **结论**：

​	•	**PyOxidizer 更适合** **性能要求高、无 Python 依赖、希望更小体积**的应用。

​	•	**PyInstaller 更适合** **兼容性好、支持动态库**的应用。



------



**📌 PyOxidizer 的高级用法**



**1️⃣ 在 Rust 项目中嵌入 Python**



如果你有 Rust 项目，并希望在 Rust 中运行 Python 代码，可以这样做：

```
use pyembed::MainPythonInterpreter;

fn main() {
    let result = MainPythonInterpreter::new().unwrap().run_code("print('Hello from Rust!')");
    println!("{:?}", result);
}
```

这样，你可以用 **Rust** 来加载 **Python** 代码，非常适合高性能应用。



------



**2️⃣ 打包整个 Python 应用**



如果你的 Python 项目有多个依赖，可以修改 pyoxidizer.bzl：

```
python_config = default_embedded_python_config()
python_config.pip_install(["numpy", "requests"])
```

然后 **重新构建**：

```
pyoxidizer build
```

最终的可执行文件会包含 **numpy** 和 **requests**，即使目标环境没有 Python 也能运行！



------



**🎯 PyOxidizer 的适用场景**



✅ **适合的项目**：

​	•	**打包 Python 应用**：创建无依赖的 EXE/Linux/Mac 可执行文件。

​	•	**加速 Python 执行**：使用 Rust 加速 Python 代码加载。

​	•	**提高安全性**：避免 Python 源码被反编译。

​	•	**嵌入 Python 到 Rust**：Rust 项目需要调用 Python 代码。



❌ **不适合的情况**：

​	•	**需要动态加载 .py 文件的应用**（PyOxidizer 默认打包时不支持动态加载）。

​	•	**GUI 应用**（PyOxidizer 目前对 Tkinter、PyQt 支持较弱）。



------



**🎯 总结**

​	•	**PyOxidizer 作用**：打包 Python 代码为独立可执行文件，无需 Python 运行环境。

​	•	**优势**：

​	•	**性能更快**（基于 Rust）

​	•	**文件更小**（比 PyInstaller 生成的 EXE 更小）

​	•	**安全性更高**（难以反编译）

​	•	**适用场景**：

​	•	打包 CLI 工具

​	•	生成跨平台 Python EXE

​	•	在 Rust 项目中嵌入 Python



如果你希望构建 **更快、更小、更安全**的 Python 可执行文件，PyOxidizer 是一个非常棒的选择！🚀



------



🎉 **现在可以试试看！**

```
pyoxidizer init my_project
cd my_project
pyoxidizer build
```

如果有任何问题或需要更深入的示例，欢迎继续讨论！😊🚀