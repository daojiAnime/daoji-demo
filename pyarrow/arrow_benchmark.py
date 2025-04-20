import gc
import os

import numpy as np
import pandas as pd
import psutil

import pyarrow as pa


def memory_usage():
    """获取当前进程内存使用"""
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / 1024 / 1024  # MB


# 创建大型DataFrame
size = 10000000
df = pd.DataFrame(
    {"id": np.arange(size), "value": np.random.randn(size), "category": np.random.choice(["A", "B", "C"], size)}
)

print(f"Pandas DataFrame 内存: {memory_usage():.2f} MB")

# 转换为PyArrow表格
table = pa.Table.from_pandas(df)
df = None  # 释放pandas对象

gc.collect()  # 强制垃圾回收

print(f"PyArrow Table 内存: {memory_usage():.2f} MB")
