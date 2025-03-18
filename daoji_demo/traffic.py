import calendar
import json
import os
import sys
from datetime import date, datetime, time

import typer
from boto3.session import Session
from dotenv import load_dotenv
from mypy_boto3_lightsail.client import LightsailClient
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

app = typer.Typer(help="AWS Lightsail 实例流量统计工具")
console = Console()

load_dotenv()
session = Session(
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION"),
)
client: LightsailClient = session.client("lightsail")


def get_current_month_first_day_zero_time():
    today = date.today()
    first_day = today.replace(day=1)
    first_day_zero_time = datetime.combine(first_day, time.min)
    return first_day_zero_time


def get_current_month_last_day_last_time():
    today = date.today()
    last_day = today.replace(day=calendar.monthrange(today.year, today.month)[1])
    last_day_last_time = datetime.combine(last_day, time(23, 59, 59))
    return last_day_last_time


def stop_instance(instance_name: str):
    client.stop_instance(instanceName=instance_name, force=True)
    console.print(f"[bold red]实例 {instance_name} 已停止！[/bold red]")


def list_instances(instances_list: list[str]):
    paginator = client.get_paginator("get_instances")
    # Create a PageIterator from the Paginator
    page_iterator = paginator.paginate()
    for page in page_iterator:
        for instance in page["instances"]:
            console.print(f"找到实例: [cyan]{instance['name']}[/cyan]")
            instances_list.append(instance["name"])


def get_month_dto_quota(instance_name: str) -> int:
    response = client.get_instance(instanceName=instance_name)
    dto_quota = response["instance"]["networking"]["monthlyTransfer"]["gbPerMonthAllocated"]
    current_datetime = datetime.now()
    instance_created_datetime = response["instance"]["createdAt"]
    if (instance_created_datetime.year == current_datetime.year) and (
        instance_created_datetime.month == current_datetime.month
    ):
        month_ts = (
            get_current_month_last_day_last_time().timestamp() - get_current_month_first_day_zero_time().timestamp()
        )
        instance_valide_ts = get_current_month_last_day_last_time().timestamp() - instance_created_datetime.timestamp()
        dto_quota = (instance_valide_ts / month_ts) * dto_quota
        console.print(f"本月创建实例，配额: [blue]{dto_quota:.2f}GB[/blue]")
    else:
        dto_quota = response["instance"]["networking"]["monthlyTransfer"]["gbPerMonthAllocated"]
        console.print(f"往月创建实例，完整配额: [blue]{dto_quota:.2f}GB[/blue]")

    return dto_quota


def get_instance_data_usage(instance_name: str, data_type: str) -> int:
    start_time = get_current_month_first_day_zero_time()
    end_time = get_current_month_last_day_last_time()
    start_time_str = start_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    end_time_str = end_time.strftime("%Y-%m-%dT%H:%M:%SZ")

    response = client.get_instance_metric_data(
        instanceName=instance_name,
        metricName=data_type,
        period=6 * 600 * 24,
        unit="Bytes",
        statistics=["Sum"],
        startTime=start_time_str,
        endTime=end_time_str,
    )

    data_points = response["metricData"]
    total_data_usage = sum([data_point["sum"] for data_point in data_points])
    usage_gb = total_data_usage / (1000 * 1000 * 1000)
    console.print(f"{data_type} 使用量: [green]{usage_gb:.2f}GB[/green]")
    return total_data_usage


def get_percent_color(percent: float) -> str:
    """根据百分比返回对应的颜色"""
    if percent >= 95:
        return "red"
    elif percent >= 80:
        return "orange3"
    elif percent >= 60:
        return "yellow"
    else:
        return "green"


@app.command()
def run(
    auto_stop: bool = typer.Option(
        True, "--no-auto-stop", help="超过流量阈值时不自动停止实例", is_flag=True, flag_value=False
    ),
):
    """统计AWS Lightsail实例的流量使用情况"""
    console.print(Panel.fit(Text("AWS Lightsail 实例流量统计", style="bold cyan"), border_style="blue"))

    instance_name: list[str] = []
    list_instances(instance_name)

    if not instance_name:
        console.print("[bold red]未找到任何实例！[/bold red]")
        return {"statusCode": 404, "body": json.dumps("No instances found!")}

    # 创建表格
    table = Table(title=f"当前月份: {datetime.now().strftime('%Y年%m月')}")
    table.add_column("实例名称", style="cyan")
    table.add_column("出站流量 (GB)", justify="right", style="green")
    table.add_column("入站流量 (GB)", justify="right", style="green")
    table.add_column("总流量 (GB)", justify="right", style="yellow")
    table.add_column("配额 (GB)", justify="right", style="blue")
    table.add_column("使用百分比", justify="right")
    table.add_column("使用进度", justify="left", width=30)
    table.add_column("状态", style="magenta")

    # 用于计算总和的变量
    total_network_out = 0
    total_network_in = 0
    total_quota = 0

    for i in instance_name:
        console.print(f"\n[bold]处理实例: [cyan]{i}[/cyan][/bold]")
        quota = get_month_dto_quota(i) * 1000 * 1000 * 1000
        network_out = get_instance_data_usage(i, "NetworkOut")
        network_in = get_instance_data_usage(i, "NetworkIn")
        total = network_out + network_in

        # 转换为GB
        network_out_gb = network_out / (1000 * 1000 * 1000)
        network_in_gb = network_in / (1000 * 1000 * 1000)
        total_gb = total / (1000 * 1000 * 1000)
        quota_gb = quota / (1000 * 1000 * 1000)

        # 累加总和
        total_network_out += network_out_gb
        total_network_in += network_in_gb
        total_quota += quota_gb

        # 计算百分比并保留两位小数
        percent = (total / quota) * 100
        percent_formatted = f"{percent:.2f}%"

        # 根据百分比获取颜色
        percent_color = get_percent_color(percent)

        # 创建进度条
        progress = f"[{percent_color}]{'■' * int(percent / 3.33):<30}[/{percent_color}]"

        # 判断状态
        status = "[green]正常[/green]"
        if (int(quota) * 0.95) < int(total):
            if auto_stop:
                status = "[red]已停止 (超过配额95%)[/red]"
                console.print(f"[bold red]警告: 实例 {i} 流量已超过配额的95%，自动停止！[/bold red]")
                stop_instance(i)
            else:
                status = "[red]超过配额95% (未停止)[/red]"
                console.print(f"[bold orange3]警告: 实例 {i} 流量已超过配额的95%，但未执行自动停止。[/bold orange3]")
        elif percent >= 80:
            status = f"[orange3]警告 ({percent:.2f}%)[/orange3]"

        # 添加到表格
        table.add_row(
            i,
            f"{network_out_gb:.2f}",
            f"{network_in_gb:.2f}",
            f"{total_gb:.2f}",
            f"{quota_gb:.2f}",
            f"[{percent_color}]{percent_formatted}[/{percent_color}]",
            progress,
            status,
        )

    # 计算总体使用百分比
    total_usage = total_network_out + total_network_in
    total_percent = (total_usage / total_quota) * 100 if total_quota > 0 else 0
    total_percent_formatted = f"{total_percent:.2f}%"
    total_percent_color = get_percent_color(total_percent)
    total_progress = f"[{total_percent_color}]{'■' * int(total_percent / 3.33):<30}[/{total_percent_color}]"

    # 添加总计行
    table.add_row(
        "[bold]总计[/bold]",
        f"[bold]{total_network_out:.2f}[/bold]",
        f"[bold]{total_network_in:.2f}[/bold]",
        f"[bold]{total_usage:.2f}[/bold]",
        f"[bold]{total_quota:.2f}[/bold]",
        f"[bold][{total_percent_color}]{total_percent_formatted}[/{total_percent_color}][/bold]",
        total_progress,
        "",
    )

    # 显示表格
    console.print(table)

    # 显示总结
    summary = Text()
    summary.append("总出站流量: ", style="bold")
    summary.append(f"{total_network_out:.2f}GB", style="green")
    summary.append(", 总入站流量: ", style="bold")
    summary.append(f"{total_network_in:.2f}GB", style="green")
    summary.append(", 总流量: ", style="bold")
    summary.append(f"{total_usage:.2f}GB", style="yellow")
    summary.append(", 总配额: ", style="bold")
    summary.append(f"{total_quota:.2f}GB", style="blue")
    console.print(Panel(summary, title="流量总结", border_style="green"))

    return {"statusCode": 200, "body": json.dumps("total_data_usage from Lambda!")}


def main() -> None:
    """入口函数"""
    try:
        app()
    except Exception as e:
        console.print(f"[bold red]错误: {str(e)}[/bold red]")
        sys.exit(1)


if __name__ == "__main__":
    main()
