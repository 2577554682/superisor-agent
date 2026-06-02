from langchain.tools import tool
from langchain.agents import create_agent
from superisor_agent_demo.tools import send_email

# ================== 3. Agent 工厂层 ==================
class AgentFactory:
    """统一创建和管理各类Agent，解耦构建逻辑与运行逻辑"""

    def __init__(self, llm):
        self.llm = llm

    def create_email_agent(self):
        """创建邮件子Agent"""
        agent = create_agent(self.llm, tools=[send_email])

        @tool
        async def email_tool(input: str) -> str:
            """根据用户意图调用邮件子Agent发送邮件"""
            result = await agent.ainvoke({"messages": [{"role": "user", "content": input}]})
            return str(result["messages"][-1].content)

        return email_tool

    def create_search_agent(self, mcp_tools: list):
        """创建搜索子Agent"""
        agent = create_agent(self.llm, tools=mcp_tools)

        @tool
        async def search_tool(input: str) -> str:
            """搜索天气、车票等信息"""
            result = await agent.ainvoke({"messages": [{"role": "user", "content": input}]})
            return str(result["messages"][-1].content)

        return search_tool

    def create_supervisor(self, sub_tools: list):
        """创建主管Agent"""
        return create_agent(
            model=self.llm,
            tools=sub_tools,
            system_prompt=(
                "你是一个智能任务调度主管。\n"
                "1. 用户询问天气和行程时，先调用工具查询日期，再查询天气。\n"
                "2. 根据天气情况决定是否查询车票。\n"
                "3. 最后根据计划决定发送哪种邮件。\n"
                "注意：请基于当前真实日期进行查询，不要猜测年份。"
            ),
        )