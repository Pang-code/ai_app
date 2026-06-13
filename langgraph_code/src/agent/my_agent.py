from langchain.agents import create_agent
from agent.init_llm import deepseek_llm
def send_email(to: str, subject: str, body: str):
    """发送邮件"""
    email = {
        "to": to,
        "subject": subject,
        "body": body
    }
    # ... 邮件发送逻辑（可自行补充SMTP或第三方API实现）
    return f"邮件已发送至 {to}"




# 创建智能体实例
agent = create_agent(
    # "qwen3.7-max",
    deepseek_llm,
    tools=[send_email],
    system_prompt="你是一个邮件助手。请始终使用 send_email 工具。"
)