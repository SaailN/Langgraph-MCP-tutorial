import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq

async def main():
    client = MultiServerMCPClient(
        {
            "math": {
                "command": "python",
                "args": ["./math_server.py"],  # Replace this
                "transport": "stdio",
            },

            "weather": {
                "url": "http://127.0.0.1:8000/mcp",
                "transport": "streamable_http",
            }
        }
    )

    tools = await client.get_tools()
    print("Registered Tools:", [tool.name for tool in tools])

  # You can replace this with any LLM API (ChatGPT, Gemini)
    llm = ChatGroq(
    model_name="llama3-70b-8192",
    temperature=0,
    api_key=" ")  # replace by your API key


    agent = create_react_agent(llm, tools)
    math_response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "what's (3 + 5) x 12?"}]}
    )
    print("🧮 Math Response:", math_response)

    for msg in math_response["messages"]:
        if hasattr(msg, "content") and msg.content.strip().isdigit():
            print("Final Math Result:", msg.content)



    weather_response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "what is the weather in nyc?"}]}
    )
    print("⛅ Weather Response:", weather_response)
    for msg in weather_response["messages"]:
        if hasattr(msg, "content") and msg.content.strip():
            print("Final weather Result:", msg.content)




# Run the async function
if __name__ == "__main__":
    asyncio.run(main())

