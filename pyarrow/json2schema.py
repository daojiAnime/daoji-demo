import json
from typing import Any

import pyarrow as pa


def infer_type(value: Any) -> str:
    """推断值的类型"""
    if value is None:
        return "null"
    elif isinstance(value, bool):
        return "boolean"
    elif isinstance(value, int):
        return "int64"
    elif isinstance(value, float):
        return "double"
    elif isinstance(value, str):
        return "string"
    elif isinstance(value, list):
        if value:
            # 列表元素类型（简化处理，取第一个元素的类型）
            element_type = infer_type(value[0])
            return f"list<{element_type}>"
        else:
            return "list<null>"
    elif isinstance(value, dict):
        return "struct"
    else:
        return "unknown"


def analyze_json(json_data: dict | list) -> dict[str, Any]:
    """直接分析 JSON 数据结构，创建 schema 信息"""
    if isinstance(json_data, list) and json_data:
        # 如果是数组，只分析第一个元素（假设所有元素结构相似）
        sample = json_data[0]
        if isinstance(sample, dict):
            return analyze_object(sample)
        else:
            return {"type": infer_type(sample)}
    elif isinstance(json_data, dict):
        return analyze_object(json_data)
    else:
        return {"type": infer_type(json_data)}


def analyze_object(obj: dict) -> dict[str, Any]:
    """分析 JSON 对象结构"""
    fields = []

    for key, value in obj.items():
        field_info = {"name": key, "nullable": value is None}

        if isinstance(value, dict):
            # 递归处理嵌套对象
            nested_result = analyze_object(value)
            field_info["type"] = "struct"
            field_info["fields"] = nested_result["fields"]
        elif isinstance(value, list) and value and isinstance(value[0], dict):
            # 处理对象数组
            field_info["type"] = "list<struct>"
            nested_result = analyze_object(value[0])
            field_info["fields"] = nested_result["fields"]
        else:
            # 基本类型
            field_info["type"] = infer_type(value)

        fields.append(field_info)

    return {"fields": fields}


def python_type_to_arrow_type(py_type: str) -> pa.DataType:
    """将Python类型字符串转换为PyArrow数据类型"""
    type_map = {
        "null": pa.null(),
        "boolean": pa.bool_(),
        "int64": pa.int64(),
        "double": pa.float64(),
        "string": pa.string(),
    }

    if py_type in type_map:
        return type_map[py_type]
    elif py_type.startswith("list<"):
        inner_type = py_type[5:-1]  # 提取list<TYPE>中的TYPE
        return pa.list_(python_type_to_arrow_type(inner_type))
    else:
        # 默认处理为字符串
        return pa.string()


def schema_dict_to_arrow_schema(schema_dict: dict[str, Any]) -> pa.Schema:
    """将schema字典转换为PyArrow Schema对象"""
    fields = []

    for field_info in schema_dict.get("fields", []):
        name = field_info["name"]
        field_type = field_info["type"]
        nullable = field_info.get("nullable", True)

        if field_type == "struct" and "fields" in field_info:
            # 处理嵌套结构
            nested_schema_dict = {"fields": field_info["fields"]}
            nested_schema = schema_dict_to_arrow_schema(nested_schema_dict)
            fields.append(pa.field(name, pa.struct(nested_schema.types), nullable=nullable))
        else:
            # 处理基本类型
            arrow_type = python_type_to_arrow_type(field_type)
            fields.append(pa.field(name, arrow_type, nullable=nullable))

    return pa.schema(fields)


def json_to_schema(json_str: str, output_format: str = "dict", use_pyarrow: bool = False) -> dict[str, Any] | pa.Schema:
    """将 JSON 字符串转换为 schema

    Args:
        json_str: JSON 字符串
        output_format: 输出格式，支持 "dict"（字典）或 "arrow"（PyArrow Schema）
        use_pyarrow: 此参数保留用于向后兼容，但在此实现中不起作用

    Returns:
        如果 output_format 为 "dict"，返回 schema 字典
        如果 output_format 为 "arrow"，返回 PyArrow Schema 对象
    """
    try:
        # 解析JSON
        json_data = json.loads(json_str)

        # 使用Python解析器分析JSON结构
        schema_dict = analyze_json(json_data)
        schema_dict["metadata"] = {}

        # 根据输出格式返回结果
        if output_format.lower() == "arrow":
            return schema_dict_to_arrow_schema(schema_dict)
        else:
            return schema_dict
    except Exception as e:
        if output_format.lower() == "arrow":
            # 如果请求Arrow格式但失败，返回空schema
            return pa.schema([])
        else:
            return {"error": f"Failed to parse JSON: {str(e)}"}


# 使用示例
if __name__ == "__main__":
    # 未知结构的 JSON 示例
    unknown_json = """
    [
        {
            "name": "John Doe",
            "age": 30,
            "is_active": true,
            "scores": [85, 90, 78],
            "address": {
                "street": "123 Main St",
                "city": "Anytown",
                "zip": "12345"
            }
        },
        {
            "name": "Jane Smith",
            "age": 28,
            "is_active": false,
            "scores": [95, 88, 92],
            "address": {
                "street": "456 Oak Ave",
                "city": "Somewhere",
                "zip": "67890"
            }
        }
    ]
    """

    # 获取字典格式的schema
    schema_dict = json_to_schema(unknown_json, output_format="dict")
    print("\n=== Schema 字典 ===")
    print(json.dumps(schema_dict, indent=2))

    # 获取PyArrow格式的schema
    schema_arrow = json_to_schema(unknown_json, output_format="arrow")
    print("\n=== PyArrow Schema ===")
    print(schema_arrow)
