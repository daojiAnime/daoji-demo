import json

import pandas as pd
import rich


def main() -> None:
    # jsonl 文件
    # 使用 chunksize 读取, 每次读取 chunksize 条记录
    chunks = 1000
    df = pd.read_json("./pyarrow/nested_test.jsonl", lines=True, chunksize=chunks)
    for chunk in df:
        rich.print(chunk)

    # json 文件
    json_data = json.load(open("./pyarrow/nested_test.json"))
    df = pd.json_normalize(
        json_data,
        sep="_",
    )
    rich.print(df)


if __name__ == "__main__":
    main()
