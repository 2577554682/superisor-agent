from env_utils import SMTP_USER,SMTP_PASS,MODELSCOPE_TOKEN
# ================== 1. 配置管理 ==================
class Config:
    """集中管理所有配置，从环境变量读取"""
    SMTP_USER: str = SMTP_USER
    SMTP_PASS: str = SMTP_PASS
    MODELSCOPE_TOKEN: str = MODELSCOPE_TOKEN

    @classmethod
    def get_mcp_config(cls) -> dict:
        if not cls.MODELSCOPE_TOKEN:
            raise ValueError("MODELSCOPE_TOKEN 未设置，请检查 .env 文件")
        return {
            "bing-cn-mcp-server": {
                "transport": "streamable_http",
                "url": "https://mcp.api-inference.modelscope.net/4b1da48cd8f64c/mcp",
                "headers": {"Authorization": f"Bearer {cls.MODELSCOPE_TOKEN}"},
            },
            "12306-mcp": {
                "transport": "streamable_http",
                "url": "https://mcp.api-inference.modelscope.net/232dca244f8f48/mcp",
                "headers": {"Authorization": f"Bearer {cls.MODELSCOPE_TOKEN}"},
            },
        }