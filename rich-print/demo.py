from rich.console import Console
from rich.panel import Panel

console = Console()


def panel_fit():
    """主函数"""
    console.print(
        Panel.fit(
            "[bold cyan]金融RAG系统功能测试生成工具[/bold cyan]",
            subtitle="[cyan]一个完整的工作流工具[/cyan]",
            border_style="cyan",
        )
    )

    # 步骤选择
    console.print("\n[bold]请选择要执行的步骤:[/bold]")
    console.print("1. 执行所有步骤（推荐）")
    console.print("2. 只生成金融问题")
    console.print("3. 只转换JSON到Excel")


def main() -> None:
    panel_fit()


if __name__ == "__main__":
    main()
