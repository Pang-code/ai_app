import os

from dotenv import load_dotenv

# override=True 确保.env文件优先
load_dotenv(override=True)


# DeepSeek
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL")

# OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")

# Anthropic (Claude)
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
ANTHROPIC_BASE_URL = os.getenv("ANTHROPIC_BASE_URL")

# Google Gemini
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_BASE_URL = os.getenv("GOOGLE_BASE_URL")

# 阿里通义千问 (Qwen)
DASHSCOPE_API_KEY = os.getenv("QWEN_API_KEY")
DASHSCOPE_BASE_URL = os.getenv("QWEN_BASE_URL")

# 字节豆包 (Doubao)
DOUBAO_API_KEY = os.getenv("DOUBAO_API_KEY")
DOUBAO_BASE_URL = os.getenv("DOUBAO_BASE_URL")

# 智普 (zhipu)
ZHIPUAI_API_KEY = os.getenv("ZHIPUAI_API_KEY")
ZHIPUAI_BASE_URL = os.getenv("ZHIPUAI_BASE_URL")

# KIMI
KIMI_API_KEY = os.getenv("KIMI_API_KEY")
KIMI_BASE_URL = os.getenv("KIMI_BASE_URL")

# HUNYUAN
HUNYUAN_APP_ID = os.getenv("HUNYUAN_APP_ID")
HUNYUAN_SECRET_ID = os.getenv("HUNYUAN_SECRET_ID")
HUNYUAN_SECRET_KEY = os.getenv("HUNYUAN_SECRET_KEY")

# MINI
MINIMAX_API_KEY = os.getenv("MINIMAX_API_KEY")
MINIMAX_BASE_URL = os.getenv("MINIMAX_BASE_URL")
