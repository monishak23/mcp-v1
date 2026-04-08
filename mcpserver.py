from mcp.server.fastmcp import FastMCP

mcp = FastMCP("My first MCP")

@mcp.tool()
def add_numbers(num1: int, num2: int) -> int:
    return num1 + num2

mcp.run()


