import json

import pyarrow as pa


def infer_schema_from_json(json_data):
    """从JSON数据推断PyArrow Schema"""
    if isinstance(json_data, dict):
        # 处理对象
        fields = []
        for key, value in json_data.items():
            field_type = infer_field_type(value)
            fields.append(pa.field(key, field_type))
        return pa.schema(fields)
    else:
        raise ValueError("Root JSON must be an object")


def infer_field_type(value):
    """推断字段类型"""
    if value is None:
        return pa.null()
    elif isinstance(value, bool):
        return pa.bool_()
    elif isinstance(value, int):
        return pa.int64()
    elif isinstance(value, float):
        return pa.float64()
    elif isinstance(value, str):
        return pa.string()
    elif isinstance(value, dict):
        # 处理嵌套对象
        fields = []
        for k, v in value.items():
            fields.append(pa.field(k, infer_field_type(v)))
        return pa.struct(fields)
    elif isinstance(value, list):
        # 处理数组 - 关键点：处理混合类型数组
        if not value:
            # 空数组默认为字符串数组
            return pa.list_(pa.string())

        # 检查是否存在混合类型
        types = set(type(item) for item in value)
        if len(types) > 1:
            # 如有混合类型，将所有元素转为字符串
            return pa.list_(pa.string())
        else:
            # 单一类型数组
            return pa.list_(infer_field_type(value[0]))
    else:
        # 默认转为字符串
        return pa.string()


def json_to_arrow(json_str):
    """将JSON字符串转换为Arrow表"""
    # 解析JSON
    data = json.loads(json_str)

    # 推断schema
    schema = infer_schema_from_json(data)

    # 转换数据为符合schema的格式
    converted_data = convert_data_for_arrow(data, schema)

    # 创建Arrow表
    return pa.Table.from_pydict(converted_data, schema)


def convert_data_for_arrow(data, schema):
    """转换数据以匹配Arrow schema"""
    result = {}

    for field in schema:
        name = field.name
        field_type = field.type

        if name in data:
            value = data[name]

            # 处理列表类型，特别是混合类型列表
            if pa.types.is_list(field_type) and isinstance(value, list):
                # 如果schema指定为字符串列表，将所有元素转为字符串
                if pa.types.is_string(field_type.value_type):
                    result[name] = [str(item) if item is not None else None for item in value]
                else:
                    result[name] = value
            else:
                result[name] = value
        else:
            result[name] = None

    return result


# 使用示例
json_data = """
{
    "name": "John",
    "age": 30,
    "city": ["New York", true, 1]
}
"""

# 转换为Arrow表
arrow_table = json_to_arrow(json_data)

# 将Arrow表保存为文件
import pyarrow.feather as feather

feather.write_feather(arrow_table, "mixed_data.arrow")
