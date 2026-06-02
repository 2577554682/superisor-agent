import asyncio

from superisor_agent_demo.agent_factory import AgentFactory
from langchain_mcp_adapters.client import MultiServerMCPClient

from superisor_agent_demo.config import Config
from superisor_agent_demo.stream_output import stream_agent_output


# ================== 5. 主入口 ==================
async def main():
    from my_llm import deepseek  # 延迟导入，便于配置先行校验

    print("开始执行任务...\n")

    factory = AgentFactory(deepseek)
    mcp_client = MultiServerMCPClient(Config.get_mcp_config())

    try:
        mcp_tools = await mcp_client.get_tools()
        print(f"成功加载 {len(mcp_tools)} 个 MCP 工具\n")

        # 组装子工具
        search_tool = factory.create_search_agent(mcp_tools)
        email_tool = factory.create_email_agent()

        # 创建主管并执行
        supervisor = factory.create_supervisor([search_tool, email_tool])
        await stream_agent_output(
            supervisor,
            "南充明天天气怎么样，要是还不错的话，帮我看看明天兰州到南充的车票。"
            "如果天气好的话，发送邮件给xxxxxxx@qq.com告诉他我明天去南充。"
            "如果天气不好的话就告诉他我明天不去南充了。",
        )
    finally:
        if hasattr(mcp_client, "close"):
            await mcp_client.close()
            print("\n MCP 连接已安全关闭")


if __name__ == "__main__":
    asyncio.run(main())