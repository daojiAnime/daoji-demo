"""
nb_log 高级示例 1: 增强的 print 函数

这个示例展示了 nb_log 的增强 print 功能：
- 自动添加时间戳
- 显示文件名和行号
- 彩色输出
- 自动记录到文件
"""

# 导入 nb_log 后，print 函数会自动增强
from nb_log import get_logger

# 创建日志器（这会触发 print 增强）
logger = get_logger("print_demo")

print("=== 增强的 print 功能演示 ===\n")

# 普通的 print，现在会自动添加时间戳和位置信息
print("这是一个普通的 print 语句")
print("它会自动显示时间戳和文件位置")

# print 支持所有标准参数
print("支持", "多个", "参数", sep=" | ")
print("可以自定义", end=" >>> ")
print("结束符")


# 在函数中使用 print
def my_function():
    print("函数中的 print 会显示函数名")

    for i in range(3):
        print(f"循环 {i+1}: 每次 print 都会显示准确的行号")


my_function()


# 在类中使用 print
class MyClass:
    def method(self):
        print("类方法中的 print 也能正确显示位置")


obj = MyClass()
obj.method()

# print 会自动记录到文件（如果配置了 PRINT_WRTIE_FILE_NAME）
print("\n💡 提示:")
print("  - print 语句会自动记录到 .print 文件")
print("  - 文件位置默认在 ~/pythonlogs/YYYY-MM-DD.project.print")
print("  - 可以通过环境变量 PRINT_WRTIE_FILE_NAME 自定义文件名")

# 对比原始 print 和增强 print
print("\n=== 功能对比 ===")
print("✅ 增强 print: 有时间戳、文件位置、彩色输出")
print("✅ 在 IDE 中可以点击跳转到源代码位置")
print("✅ 自动记录到文件供后续分析")

# 如何禁用 print 增强（如果需要）
print("\n如需禁用增强 print，在配置文件中设置:")
print("AUTO_PATCH_PRINT = False")

print("\n✅ 增强 print 示例完成！")
