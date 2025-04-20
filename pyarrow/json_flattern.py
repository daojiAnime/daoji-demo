import json

import pandas as pd
import rich


def flatten_json(nested_json: dict) -> pd.DataFrame:
    """Flatten a nested JSON object"""
    df = pd.json_normalize(nested_json)
    return df


if __name__ == "__main__":
    nested_json = json.load(open("./pyarrow/nested_test.json"))
    df = flatten_json(nested_json)
    print(df)
    rich.print(f"type: {[type(df.iloc[0][col]) for col in df.columns]}")
