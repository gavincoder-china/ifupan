import sys
import os
from deepseek_v2_langchain import deepseek_analyze
from ifupan.prompt_fupan import fupan_prompts

def analyze(text, prompt_type):
    task_description = fupan_prompts.get(prompt_type, fupan_prompts['diary'])
    result = deepseek_analyze(text, task_description)
    return result


