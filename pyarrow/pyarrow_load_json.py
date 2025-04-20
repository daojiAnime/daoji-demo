import orjson
import pandas as pd

import pyarrow as pa
import pyarrow.json as pj


def arrow_load_json() -> None:
    #! 不支持 list[Any] 类型
    # 用自定义 Schema 读取 JSON
    table = pj.read_json("./pyarrow/test.json")

    # 打印读取的表格
    print(table)

    # 将表格转换为 Pandas DataFrame
    df = table.to_pandas()
    print(df)


def pandas_load_json() -> None:
    # 读取 JSON 文件
    df = pd.read_json("./pyarrow/test.json")
    print(df)

    # 将 DataFrame 转换为 Arrow Table
    table = pa.Table.from_pandas(df)
    print(table)


if __name__ == "__main__":
    # pandas_load_json()
    with open("./pyarrow/test.json", "rb") as f:
        data = orjson.loads(f.read())
    print(data)
