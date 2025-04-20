import json
import random
import time

from json2schema import json_to_schema


def generate_large_json(num_records: int) -> str:
    """生成大型JSON数据用于性能测试"""
    records = []

    # 可能的值池
    names = ["张三", "李四", "王五", "赵六", "钱七", "孙八", "周九", "吴十"]
    cities = ["北京", "上海", "广州", "深圳", "杭州", "成都", "重庆", "西安"]
    streets = ["中关村大街", "南京路", "天河路", "福田路", "西湖大道", "锦江大道", "解放碑", "钟楼大街"]
    zip_codes = ["100010", "200020", "510030", "518000", "310012", "610041", "400010", "710003"]

    for i in range(num_records):
        record = {
            "id": i,
            "name": random.choice(names),
            "age": random.randint(18, 60),
            "is_active": random.choice([True, False]),
            "scores": [random.randint(60, 100) for _ in range(3)],
            "address": {
                "street": random.choice(streets),
                "city": random.choice(cities),
                "zip": random.choice(zip_codes),
            },
        }
        records.append(record)

    return json.dumps(records)


def benchmark(json_data: str, use_pyarrow: bool, repeat: int = 5) -> dict[str, float]:
    """测量解析性能"""
    total_time = 0
    min_time = float("inf")
    max_time = 0

    for _ in range(repeat):
        start_time = time.time()

        # 执行解析
        schema = json_to_schema(json_data, use_pyarrow=use_pyarrow)

        end_time = time.time()
        elapsed = end_time - start_time

        total_time += elapsed
        min_time = min(min_time, elapsed)
        max_time = max(max_time, elapsed)

    return {"avg_time": total_time / repeat, "min_time": min_time, "max_time": max_time}


def main():
    # 测试不同大小的数据集
    sizes = [100, 1000, 10000]

    print(f"{'数据量':>10} | {'方法':>10} | {'平均时间(秒)':>15} | {'最小时间(秒)':>15} | {'最大时间(秒)':>15}")
    print("-" * 75)

    for size in sizes:
        print(f"生成 {size} 条记录的测试数据...")
        json_data = generate_large_json(size)

        # Python解析
        print(f"测试Python实现 ({size} 条记录)...")
        py_results = benchmark(json_data, use_pyarrow=False)

        # PyArrow解析
        print(f"测试PyArrow实现 ({size} 条记录)...")
        pa_results = benchmark(json_data, use_pyarrow=True)

        # 输出结果
        print(
            f"{size:>10} | {'Python':>10} | {py_results['avg_time']:>15.6f} | {py_results['min_time']:>15.6f} | {py_results['max_time']:>15.6f}"
        )
        print(
            f"{size:>10} | {'PyArrow':>10} | {pa_results['avg_time']:>15.6f} | {pa_results['min_time']:>15.6f} | {pa_results['max_time']:>15.6f}"
        )
        print("-" * 75)

        # 对比
        speedup = py_results["avg_time"] / pa_results["avg_time"] if pa_results["avg_time"] > 0 else 0
        print(f"PyArrow 与 Python 实现速度比: {speedup:.2f}x")
        print("=" * 75)


if __name__ == "__main__":
    main()
