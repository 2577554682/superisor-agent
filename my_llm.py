from langchain_openai import ChatOpenAI
from env_utils import  DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL

deepseek = ChatOpenAI(
    model="deepseek-v4-flash",
    api_key=DEEPSEEK_API_KEY,
    base_url=DEEPSEEK_BASE_URL,
    temperature=1,
)