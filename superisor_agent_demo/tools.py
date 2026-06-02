import asyncio
import smtplib
from typing import List
from langchain.tools import tool
from email.mime.text import MIMEText

from superisor_agent_demo.config import Config


# ================== 2. 独立工具层 ==================
@tool
async def send_email(to: List[str], subject: str, body: str) -> str:
    """发送邮件工具。参数: to(收件人列表), subject(主题), body(正文)"""
    msg = MIMEText(body, "plain", "utf-8")
    msg["From"] = Config.SMTP_USER
    msg["To"] = ", ".join(to)
    msg["Subject"] = subject

    def _sync_send():
        """同步发送逻辑，放到线程池中执行避免阻塞事件循环"""
        server = smtplib.SMTP_SSL("smtp.qq.com", 465, timeout=10)
        try:
            server.login(Config.SMTP_USER, Config.SMTP_PASS)
            server.sendmail(Config.SMTP_USER, to, msg.as_string())
            return "邮件发送成功！"
        except Exception as e:
            return f"邮件发送失败: {str(e)}"
        finally:
            server.quit()

    # 同步IO操作放入线程池，不阻塞异步Agent
    return await asyncio.to_thread(_sync_send)