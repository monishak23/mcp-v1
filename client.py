import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from google import genai
from google.genai import types

client = genai.Client(api_key="")

async def run():
    server_parameters = StdioServerParameters(
        command = "python",
        args = ["mcpserver.py"],
    )

    async with stdio_client(server_parameters) as (read, write):
        async with ClientSession(read, write) as session:
             await session.initialize()
             tools_result = await session.list_tools()

             gemini_tools = []
             for tool in tools_result.tools:
                 gemini_tools.append(
                     types.Tool(function_declarations=[
                         types.FunctionDeclaration(
                             name=tool.name,
                             description=tool.description,
                             parameters=tool.inputSchema
                         )
                     ])
                 )

                 # ask Gemini something that needs the tool
             response = client.models.generate_content(
                 model="gemini-2.5-flash-lite",
                 contents="What is 25 plus 37?",
                 config=types.GenerateContentConfig(
                     tools=gemini_tools
                 )
             )

             part = response.candidates[0].content.parts[0]
             if hasattr(part, "function_call"):
                 fn = part.function_call
                 print(f"Gemini wants to call: {fn.name}({dict(fn.args)})")

                 # call the tool on your MCP server
                 result = await session.call_tool(fn.name, dict(fn.args))
                 print(f"Tool result: {result.content[0].text}")

                 # send result back to Gemini for final answer to maintain history and tool will retrun only answer gemini will add context
                 final = client.models.generate_content(
                     model="gemini-2.5-flash-lite",
                     contents=[
                         {"role": "user", "parts": [{"text": "What is 25 plus 37?"}]},
                         {"role": "model", "parts": [{"text": str(part.text)}]},
                     ]
                 )
                 print(f"Gemini: {final.text}")

asyncio.run(run())