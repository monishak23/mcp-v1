# mcp-v1
Model Context Protocol working

## Need for MCP

To connect all the external databses, files and api through a common protocol that is accepted by all the llms.

## Without MCP

1. We have to provide the llm with all the list of apis and use this in the respective case
2. Whenerver a new tool (function) is introduced we have to add that also llm in call each time.
3. Custom glue code is needed to connect llm and tools.
4. To solve these Anthropic introduced this concept called MCP

## MCP

 MCP Server
  - it has all the tools 
  - whenever a new tool is added only it can be updated here
  - runs as a separate process 

MCP Client
 - this is where llm call is made
 - list tools is added from server
 - calls tools on server when LLM requests it
 - sends tool result back to LLM      
