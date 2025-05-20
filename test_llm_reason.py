from openai import OpenAI
import asyncio
import os
from openai import AsyncOpenAI
from typing import List
from opik.integrations.openai import track_openai
from tenacity import retry, stop_after_attempt, wait_random_exponential
from loguru import logger
from configs.configs import *
from logics.copilot.llm_openrouter import LLMOpenRouter
from rich import print
from rich.live import Live
from rich.panel import Panel
from rich.layout import Layout
from rich.console import Console
from rich.text import Text
from rich.markdown import Markdown
from rich.console import Group
from rich.padding import Padding
from pydantic import BaseModel
import sys

choose_member_prompt = """\
# Role

You are a Leader of a financial team, and you will lead the team to solve financial problems raised by users.

# Requirements
1. You will determine whether the user's question needs to be assigned to team members based on the question. You currently have 2 team members: Analyst and Researcher.
2. If assignment is needed, please choose the most suitable team member and provide the reason for the assignment.
3. You can only assign one question to one team member at a time. The team member will return the results to you, and you will then determine whether to continue assigning the question or solve it.
4. If assignment is not needed, please answer the user's question directly.
5. Return your judgment and choice in JSON format.

# Team Members

- Analyst: Skilled in using Python code to solve financial problems, proficient in using various finance-related third-party libraries, and experienced in various data analysis and calculations. Analyst can use our existing tools to retrieve company stock prices, financial statements, and other data. Company news can also be directly obtained by the Analyst through our provided tools.
- Researcher: Skilled in searching for data relevant to questions from reliable documents (such as SEC filings, earnings call transcripts, etc.). Researcher has access to original PDF files, and while these PDFs contain financial statements and other data, we have already extracted this data and made it available to the Analyst. Additionally, the Researcher cannot answer questions about stock prices or recent events; you need to use the Analyst to answer these types of questions.

# Example of JSON return format

member: Analyst / Researcher / solved

# Format
Only return the member text, no other text.
PS: 
Question: How much is the stock price of AAPL?
Answer: solved

Question: What's the stock price of AAPL?
Answer: Analyst
""".strip()

question_list = """\
Please analyze the changes in Apple Inc.'s (AAPL) capital structure over the past three years and calculate the changing trend of its weighted average cost of capital (WACC).
We extract R&D spending data from Tesla's (TSLA) 10-K reports and analyze its correlation with revenue growth.
Analyze the impact of Microsoft's (MSFT) merger and acquisition activities in the past five years on its financial statements, especially the changes in goodwill and intangible assets.
Please extract net profit, total assets and shareholders' equity data from Netflix's financial report, calculate its ROA and ROE, and analyze the impact of its video content capitalization policy on these indicators.
Please construct a rolling 12-month EBITDA chart based on the quarterly financial data in Meta's latest annual report and mark the YoY growth rate inflection point.
Identify all acquisitions listed in Microsoft's 2023 10-K report, list the transaction name, amount and potential impact of the transaction on operating cash flow.
Based on Tesla's 2023 10-K report, we extracted revenue data related to regulatory credits and analyzed how much they contribute to the overall gross profit margin.
Please analyze the revenue growth drivers from Apple's most recent 10-K report and calculate the compound annual growth rate (CAGR) over the past three years.
""".strip()

class ChooseMemberResult(BaseModel):
    member: str
    reason: str

async def main():
    client = LLMOpenRouter().client
    prompt = """\
What's the stock price of AAPL?
"""
    console = Console()
    console.print(Panel("正在调用API...", title="状态", border_style="yellow"))
    
    # 创建Markdown对象用于思维链和内容展示
    thinking_md = ""
    content_md = ""
    reason_text = Text("等待中...", style="bold yellow")
    
    # 创建布局
    layout = Layout()
    layout.split_column(
        Layout(name="upper", ratio=3),
        Layout(name="lower", ratio=1),
    )
    
    # 进一步拆分上部区域用于思维链
    layout["upper"].split_row(
        Layout(name="thinking", ratio=5),
        Layout(name="thinking_status", ratio=2),
    )
    
    # 下部区域用于内容
    layout["lower"].name = "content"
    
    # 初始化布局面板
    layout["thinking"].update(Panel("等待思维链...", title="思维链", border_style="cyan"))
    layout["thinking_status"].update(Panel("等待思维链结束...", title="思维链状态", border_style="yellow"))
    layout["content"].update(Panel("等待内容...", title="内容", border_style="green"))
    
    # 创建Live显示但不立即进入上下文
    live = Live(
        layout, 
        refresh_per_second=10,
        transient=False,
        auto_refresh=False
    )
    
    try:
        # 启动显示
        live.start()
        live.refresh()
        
        print("开始API调用和流式接收数据...", file=sys.stderr)
        
        # 调用API
        response = await client.chat.completions.create(
            model="anthropic/claude-3.7-sonnet:thinking",
            messages=[
                {
                    "role": "system",
                    "content": choose_member_prompt
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            reasoning_effort="medium",
            stream=True,
        )
        
        # 更新状态
        layout["thinking_status"].update(Panel("API连接已建立，等待数据...", title="思维链状态", border_style="yellow"))
        live.refresh()
        
        # 逐块处理响应
        chunk_counter = 0
        reasoning_counter = 0
        content_counter = 0
        
        has_shown_sample = False
        
        async for chunk in response:
            chunk_counter += 1
            
            # 打印第一个chunk的详细信息用于调试
            if not has_shown_sample and chunk_counter <= 3:
                has_shown_sample = True
                print("\n==== 样本数据块详情 ====", file=sys.stderr)
                print(f"类型: {type(chunk)}", file=sys.stderr)
                print(f"属性: {dir(chunk)}", file=sys.stderr)
                print(f"原始内容: {chunk}", file=sys.stderr)
                
                if hasattr(chunk, "choices") and len(chunk.choices) > 0:
                    delta = chunk.choices[0].delta
                    print(f"Delta类型: {type(delta)}", file=sys.stderr)
                    print(f"Delta属性: {dir(delta)}", file=sys.stderr)
                    print(f"Delta内容: {delta}", file=sys.stderr)
                    
                    # 尝试查找reasoning属性或相关属性
                    print("查找思维链数据:", file=sys.stderr)
                    if hasattr(delta, "reasoning"):
                        print(f"- delta.reasoning存在: {delta.reasoning}", file=sys.stderr)
                    else:
                        print("- delta.reasoning不存在", file=sys.stderr)
                        
                    # 检查_extra_fields
                    if hasattr(delta, "_extra_fields"):
                        print(f"- delta._extra_fields存在: {delta._extra_fields}", file=sys.stderr)
                        if "reasoning" in delta._extra_fields:
                            print(f"  - reasoning在_extra_fields中: {delta._extra_fields['reasoning']}", file=sys.stderr)
                    else:
                        print("- delta._extra_fields不存在", file=sys.stderr)
                        
                    # 检查raw属性
                    if hasattr(chunk, "_raw_response"):
                        print(f"- 原始响应: {chunk._raw_response}", file=sys.stderr)
            
            delta = chunk.choices[0].delta if hasattr(chunk, 'choices') and len(chunk.choices) > 0 else None
            
            # 尝试从不同可能的位置获取reasoning数据
            reasoning_data = None
            
            # 方法1: 标准位置
            if delta and hasattr(delta, "reasoning") and delta.reasoning:
                reasoning_data = delta.reasoning
                
            # 方法2: 检查_extra_fields
            elif delta and hasattr(delta, "_extra_fields") and delta._extra_fields and "reasoning" in delta._extra_fields:
                reasoning_data = delta._extra_fields["reasoning"]
                
            # 方法3: 检查原始响应
            elif hasattr(chunk, "_raw_response") and "reasoning" in str(chunk._raw_response):
                # 尝试从原始响应中提取reasoning
                import json
                try:
                    if isinstance(chunk._raw_response, dict) and "reasoning" in chunk._raw_response:
                        reasoning_data = chunk._raw_response["reasoning"]
                    elif isinstance(chunk._raw_response, str):
                        data = json.loads(chunk._raw_response)
                        if "reasoning" in data:
                            reasoning_data = data["reasoning"]
                except Exception as e:
                    print(f"解析原始响应失败: {e}", file=sys.stderr)
            
            # 处理找到的思维链数据
            if reasoning_data:
                reasoning_counter += 1
                
                # 尝试将文本格式化为Markdown
                # 如果是普通文本，添加一些基本的Markdown格式
                reasoning_data = reasoning_data.strip()
                
                # 将思维链数据添加到累积的markdown文本中
                thinking_md += reasoning_data
                
                # 渲染为Markdown
                md = Markdown(thinking_md)
                layout["thinking"].update(
                    Panel(
                        Group(
                            md,
                            Padding("", 1)  # 添加一些底部填充
                        ),
                        title=f"思维链 (已接收{reasoning_counter}个片段)",
                        border_style="cyan",
                        height=console.height // 2  # 使用一半屏幕高度
                    )
                )
                layout["thinking_status"].update(Panel("正在接收思维链...", title="思维链状态", border_style="cyan"))
                live.refresh()  # 立即刷新
            
            # 处理结束原因
            if hasattr(chunk.choices[0], "finish_reason") and chunk.choices[0].finish_reason:
                reason = chunk.choices[0].finish_reason
                reason_text = Text(f"思维链结束，原因：{reason}", style="bold green")
                layout["thinking_status"].update(Panel(reason_text, title="思维链状态", border_style="green"))
                live.refresh()  # 立即刷新
            
            # 处理内容
            if delta and hasattr(delta, "content") and delta.content is not None:
                content_counter += 1
                content_md += delta.content

                # 渲染为Markdown
                content_markdown = Markdown(content_md)
                layout["content"].update(
                    Panel(
                        content_markdown,
                        title=f"内容 (已接收{content_counter}个片段)",
                        border_style="green"
                    )
                )
                live.refresh()  # 立即刷新
            
            # 给控制台一些时间渲染
            await asyncio.sleep(0.01)
            
        # 完成后更新状态
        if reasoning_counter == 0:
            layout["thinking"].update(Panel("未接收到思维链数据", title="思维链", border_style="red"))
        else:
            # 最终显示完整的思维链
            final_thinking_md = Markdown(thinking_md)
            layout["thinking"].update(
                Panel(
                    final_thinking_md,
                    title=f"思维链 (总计{reasoning_counter}个片段)",
                    border_style="cyan"
                )
            )
            
        if content_counter == 0:
            layout["content"].update(Panel("未接收到内容数据", title="内容", border_style="red"))
        else:
            # 最终显示完整的内容
            final_content_md = Markdown(content_md)
            layout["content"].update(
                Panel(
                    final_content_md,
                    title=f"内容 (总计{content_counter}个片段)",
                    border_style="green"
                )
            )
            
        layout["thinking_status"].update(Panel(f"完成！共接收{chunk_counter}个数据块", title="状态", border_style="green"))
        live.refresh()
        
        # 打印统计信息
        print(f"\n处理完成: 共{chunk_counter}个数据块, {reasoning_counter}个思维链片段, {content_counter}个内容片段", file=sys.stderr)
        
        # 再给用户一些时间查看最终结果
        await asyncio.sleep(1)
        
    except Exception as e:
        # 处理异常
        error_text = Text(f"发生错误: {str(e)}", style="bold red")
        layout["thinking_status"].update(Panel(error_text, title="错误", border_style="red"))
        live.refresh()
        print(f"错误详情: {str(e)}", file=sys.stderr)
        import traceback
        traceback.print_exc()
    finally:
        # 确保Live显示被正确停止
        live.stop()
        
    # 在Live显示之外打印最终结果
    console = Console(width=120)  # 指定更宽的控制台宽度
    console.print("\n\n最终结果:")
    
    # 使用Markdown显示完整思维链
    thinking_panel = Panel(
        Markdown(thinking_md) if thinking_md else Text("无思维链数据", style="dim red"),
        title="完整思维链",
        border_style="cyan",
        width=console.width
    )
    console.print(thinking_panel)
    
    # 显示思维链结束原因
    console.print(Panel(reason_text, title="思维链结束原因", border_style="cyan", width=console.width))
    
    # 使用Markdown显示完整内容
    content_panel = Panel(
        Markdown(content_md) if content_md else Text("无内容数据", style="dim red"),
        title="完整内容",
        border_style="green",
        width=console.width
    )
    console.print(content_panel)


# 添加专门的调试函数来分析API响应格式
async def debug_api_response():
    """调试函数，专门用于分析API返回的数据结构"""
    client = LLMOpenRouter().client
    prompt = "今天天气如何？"
    console = Console()
    console.print(Panel("开始调试API响应", title="调试", border_style="yellow"))
    
    response = await client.chat.completions.create(
        model="anthropic/claude-3.7-sonnet:thinking",
        messages=[
            {
                "role": "user", 
                "content": prompt
            }
        ],
        reasoning_effort="medium",
        stream=True,
    )
    
    console.print("开始接收数据流...")
    chunk_count = 0
    
    async for chunk in response:
        chunk_count += 1
        console.print(f"\n[bold yellow]===== 数据块 #{chunk_count} =====")
        
        # 打印基本信息
        console.print(f"[bold cyan]类型:[/] {type(chunk)}")
        console.print(f"[bold cyan]字符串表示:[/] {str(chunk)}")
        
        # 查看主要属性
        main_attrs = ["id", "object", "created", "model", "choices"]
        for attr in main_attrs:
            if hasattr(chunk, attr):
                console.print(f"[bold cyan]{attr}:[/] {getattr(chunk, attr)}")
                
        # 深入检查choices
        if hasattr(chunk, "choices") and chunk.choices:
            choice = chunk.choices[0]
            console.print("\n[bold magenta]choices[0] 详情:")
            
            choice_attrs = ["index", "finish_reason", "delta"]
            for attr in choice_attrs:
                if hasattr(choice, attr):
                    console.print(f"[bold cyan]{attr}:[/] {getattr(choice, attr)}")
            
            # 检查delta
            if hasattr(choice, "delta"):
                delta = choice.delta
                console.print("\n[bold blue]delta 详情:")
                
                delta_attrs = ["content", "role", "reasoning"]
                for attr in delta_attrs:
                    if hasattr(delta, attr):
                        console.print(f"[bold cyan]{attr}:[/] {getattr(delta, attr)}")
                
                # 检查额外字段
                if hasattr(delta, "_extra_fields"):
                    console.print(f"[bold cyan]_extra_fields:[/] {delta._extra_fields}")
                    
                # 尝试检查全部属性
                console.print(f"[bold cyan]所有属性:[/] {dir(delta)}")
                
        # 只打印前3个chunk详细信息，之后只计数
        if chunk_count >= 3:
            console.print("[dim]后续数据块省略详细信息...[/]")
            break
            
    # 继续计数但不打印详情
    async for _ in response:
        chunk_count += 1
        
    console.print(f"\n[bold green]API调试完成，共接收 {chunk_count} 个数据块")

async def test_llm_reason():
    client = LLMOpenRouter().client
    prompt = """\
今天天气如何？
"""
    response = await client.chat.completions.create(
        model="anthropic/claude-3.7-sonnet:thinking",
        messages=[
        {
            "role": "user", 
            "content": prompt
        }
    ],
        reasoning_effort="medium",
        stream=True,
    )
    thinking = ""
    content = ""
    chunk_list = []
    async for chunk in response:
        # 思维链打印
        chunk_list.append(chunk)
        if hasattr(chunk.choices[0].delta, "reasoning") and chunk.choices[0].delta.reasoning:
            thinking += chunk.choices[0].delta.reasoning
            if chunk.choices[0].finish_reason:
                print(f"思考链：{chunk.choices[0].finish_reason}")

        if hasattr(chunk.choices[0].delta, "content") and chunk.choices[0].delta.content:
            content += chunk.choices[0].delta.content

    print(f"思考链：{thinking}")
    print(f"内容：{content}")


async def test_llm_format():
    client = LLMOpenRouter().client
    prompt = """\
今天天气如何？
"""
    response = await client.chat.completions.create(
        model="anthropic/claude-3.7-sonnet:thinking",
        messages=[
        {
            "role": "user", 
            "content": prompt
        }
    ],
        stream=True,
        response_format={"type": "json_object"},
    )
    async for chunk in response:
        print(chunk)


async def test_llm_question_list():
    client = LLMOpenRouter().client
    for question in question_list.split("\n"):
        response = await client.chat.completions.create(
            model="anthropic/claude-3.7-sonnet:thinking",
            messages=[
                {
                    "role": "system",
                    "content": choose_member_prompt
                },
                {
                    "role": "user", 
                    "content": question
                }
            ],
            reasoning_effort="medium",
            stream=True,
        )
        thinking = ""
        content = ""
        async for chunk in response:
            if hasattr(chunk.choices[0].delta, "reasoning") and chunk.choices[0].delta.reasoning:
                thinking += chunk.choices[0].delta.reasoning

            if hasattr(chunk.choices[0].delta, "content") and chunk.choices[0].delta.content:
                content += chunk.choices[0].delta.content
        
        print(f"内容：{content}")
        assert content.lower() in ["analyst", "researcher", "solved"]

async def test_chart_generation():
    schema = {'$schema': 'http://json-schema.org/schema#', 'type': 'array', 'items': {'type': 'object', 'properties': {'date': {'type': 'string'}, 'sector': {'type': 'string'}, 'exchange': {'type': 'string'}, 'averageChange': {'type': 'number'}}, 'required': ['averageChange', 'date', 'exchange', 'sector']}}

    chart_generation_prompt = """\
You are a financial analyst. 你很擅长使用 echartjs 生成图表，现在需要你根据用户的需求生成一个合理的图表针对金融数据进行表达, 并且需要你返回一个完整的 html 字符串。

# 要求
1. 图表需要使用 echartjs 生成
2. 图表需要根据用户的需求生成，并且需要符合 echartjs 的规范
3. 图表需要尽可能的详细，并且需要尽可能的符合用户的需求
4. 图表需要尽可能的符合金融数据的特点，并且需要尽可能的符合金融数据的可视化规范
5. 图表需要尽可能的符合金融数据的可视化规范，并且需要尽可能的符合金融数据的可视化规范
6. 除 HTML 字符串外，不要返回任何其他内容

# 数据结构, 这是通过 genson 解析后的数据结构
{'$schema': 'http://json-schema.org/schema#', 'type': 'array', 'items': {'type': 'object', 'properties': {'date': {'type': 'string'}, 'sector': {'type': 'string'}, 'exchange': {'type': 'string'}, 'averageChange': {'type': 'number'}}, 'required': ['averageChange', 'date', 'exchange', 'sector']}}

# 代码规范

1. 函数入参字段名有且只有一个 data
2. 函数内部根据数据结构解析 data 数据，并根据数据结构生成 echartjs 图表
3. 函数返回值为 echartjs 图表的 html 字符串
4. 通过 https://financialmodelingprep.com/stable/sector-performance-snapshot?date=2024-02-01&apikey=WEyyZhXSOzgHLXLdBT3Ml3v3147FErC1 获取数据
5. 调用函数时，需要传入 date 参数，date 参数从第3 条规范的 URL 中获取
"""
    client = LLMOpenRouter().client
    response = await client.chat.completions.create(
        model="deepseek/deepseek-chat-v3-0324",
        messages=[
            {"role": "system", "content": chart_generation_prompt},
            {"role": "user", "content": "查询各个行业在市场的平均变化"}
        ],
        response_format=schema,
    )
    content = response.choices[0].message.content
    with open("ubde.html", "w") as f:
        f.write(content)

if __name__ == "__main__":
    asyncio.run(test_chart_generation())