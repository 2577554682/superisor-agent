# ================== 4. 流式输出处理器 ==================
from langchain_core.messages import AIMessageChunk


async def stream_agent_output(agent, user_input: str):
    """封装流式输出逻辑，隔离chunk格式兼容处理"""
    async for chunk in agent.astream({"messages": [{"role": "user", "content": user_input}]}):
        content = None
        if isinstance(chunk, AIMessageChunk):
            content = chunk.content
        elif isinstance(chunk, dict):
            # 兼容 dict 包装格式
            messages = chunk.get("model", {}).get("messages", [])
            if messages and hasattr(messages[-1], "content"):
                content = messages[-1].content

        if content:
            print(content, end="", flush=True)
        elif isinstance(chunk, dict):
            # 仅在无文本内容时提示工具调用
            msgs = chunk.get("model", {}).get("messages", [])
            if msgs and getattr(msgs[-1], "tool_call_chunks", None):
                print("\n正在调用工具...", flush=True)
    print()  # 结束后换行