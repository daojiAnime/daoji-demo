import asyncio

import rich
from fastmcp.client import Client
from fastmcp.client.transports import StdioTransport


async def main():
    npx_stdio = StdioTransport(command="bunx", args=["-y", "@browsermcp/mcp@latest"])
    client = Client(transport=npx_stdio)

    async with client:
        rich.print(await client.list_tools())


if __name__ == "__main__":
    asyncio.run(main())
