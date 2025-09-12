import asyncio
import math
import threading
from collections.abc import Awaitable
from typing import Annotated, Any

from fastmcp import Client, FastMCP
from nest_asyncio import apply
from pydantic import Field
from rich import pretty

apply()
pretty.install()

mcp = FastMCP(name="CalculatorServer")
client = Client(mcp)


class TrigonometryCalculator:
    @staticmethod
    def add(a: float, b: float):
        """
        Adds two numbers.
        """
        return a + b

    @staticmethod
    def sine(x: float):
        """
        Calculates the sine of an angle in radians.

        :param x: The angle in radians.
        :return: The sine of x.
        """
        return math.sin(x)

    @staticmethod
    def cosine(x: float):
        """
        Calculates the cosine of an angle in radians.

        :param x: The angle in radians.
        :return: The cosine of x.
        """
        return math.cos(x)

    @staticmethod
    def tangent(x: float):
        """
        Calculates the tangent of an angle in radians.

        :param x: The angle in radians.
        :return: The tangent of x.
        """
        return math.tan(x)

    @staticmethod
    def _square(x: float):
        """
        Calculates the square of a number.
        """
        return x * x

    @staticmethod
    def demo(query: str | None = None):
        """
        A demo function.
        """
        return query

    @staticmethod
    def pydantic_field_func(query: Annotated[str, Field(default="test query", description="A demo field")]) -> str:
        """
        A demo function.
        """
        return query


def load_tools_from_module(module_class: object):
    """
    从模块中加载工具
    # 1. 遍历工具类的函数
    # 2. 排除下划线开头的函数
    """
    for name, func in module_class.__dict__.items():
        if name.startswith("_"):
            continue
        if isinstance(func, staticmethod) or isinstance(func, classmethod):
            func = func.__func__
        mcp.tool(func)


load_tools_from_module(TrigonometryCalculator)


async def list_tools(mcp_client: Client):
    async with mcp_client:
        result = await mcp_client.list_tools()
    return result


def run_async_blocking_in_async(coro: Awaitable[Any]) -> Any:
    """
    在异步环境中，使用线程安全方式运行一个协程并阻塞等待结果。
    - 适用于 async 函数中调用同步函数时，这个同步函数要运行协程并返回结果。
    """
    result_container = {}
    exc_container = {}

    def runner():
        try:
            result_container["result"] = asyncio.run(coro)
        except Exception as e:
            exc_container["error"] = e

    thread = threading.Thread(target=runner)
    thread.start()
    thread.join()

    if "error" in exc_container:
        raise exc_container["error"]
    return result_container["result"]


async def main() -> None:
    result = run_async_blocking_in_async(list_tools(client))
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
