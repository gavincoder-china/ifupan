from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

# 加载 .env 文件
load_dotenv()
# 获取环境变量
api_key = os.getenv("deepseek_api_key")
base_url = os.getenv("deepseek_base_url")

# 初始化 DeepSeek LLM
llm = ChatOpenAI(
    model='deepseek-chat', 
    openai_api_key=api_key,
    openai_api_base=base_url
)

def deepseek_analyze(text, task_description):
    prompt = f"{task_description}\n\n内容：\n{text}"
    response = llm.invoke(prompt)
    return response.content