import sys
import os
from ifupan.utils.deepseek_v2_langchain import deepseek_analyze
from ifupan.app.services.prompt_fupan  import fupan_prompts

def analyze(text, prompt_type):
    task_description = fupan_prompts.get(prompt_type, fupan_prompts['diary'])
    result = deepseek_analyze(text, task_description)
    return result


