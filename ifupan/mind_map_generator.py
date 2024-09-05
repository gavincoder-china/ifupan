import ast
import logging
import re
import os

import graphviz
import markdown
from weasyprint import HTML, CSS

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Create a 'files' directory if it doesn't exist
if not os.path.exists('files'):
    os.makedirs('files')

def generate(text, prompt_type):
    # Use the prompt_type in your mind map generation logic
    # ...
    mind_map_file = None
    pdf_file = None

    try:
        # 生成思维导图
        mind_map_file = generate_mind_map(text)
        logging.info(f"思维导图已生成：{mind_map_file}")
    except Exception as e:
        logging.error(f"生成思维导图时发生错误: {str(e)}")

    try:
        # 生成PDF复盘报告
        pdf_file = generate_pdf_report(text)
        logging.info(f"复盘报告已生成：{pdf_file}")
    except Exception as e:
        logging.error(f"生成PDF报告时发生错误: {str(e)}")

    return mind_map_file, pdf_file


def generate_mind_map(text):
    # 使用 DeepSeek 模型分析文本并生成思维导图结构
    mind_map_prompt = """
    请分析以下文本，并生成一个思维导图结构。
    输出格式应为一个嵌套的字典，其中键为节点名，值为子节点列表或字典。
    主题应该是最顶层的键。
    输出应该只包含 Python 字典，不需要其他解释或代码块标记。

    例如：
    {
        "主题": [
            {"子主题1": ["要点1", "要点2"]},
            {"子主题2": ["要点3", "要点4"]}
        ]
    }
    """

    structure_str = deepseek_analyze(text, mind_map_prompt)

    # 提取字典字符串
    dict_match = re.search(r'\{.*\}', structure_str, re.DOTALL)
    if dict_match:
        dict_str = dict_match.group()
    else:
        raise ValueError("无法从模型输出中提取字典结构")

    # 将字符串转换为字典
    try:
        structure = ast.literal_eval(dict_str)
    except:
        raise ValueError("无法解析模型输出为有效的Python字典")

    # 使用 Graphviz 创建思维导图
    dot = graphviz.Digraph(comment='Mind Map')
    dot.attr(rankdir='LR')  # 从左到右布局

    def add_nodes(parent, items):
        if isinstance(items, dict):
            for key, value in items.items():
                node_id = str(hash(key))
                dot.node(node_id, key)
                if parent:
                    dot.edge(parent, node_id)
                add_nodes(node_id, value)
        elif isinstance(items, list):
            for item in items:
                if isinstance(item, dict):
                    add_nodes(parent, item)
                else:
                    node_id = str(hash(item))
                    dot.node(node_id, item)
                    dot.edge(parent, node_id)

    add_nodes(None, structure)

    # 保存思维导图
    mind_map_filename = os.path.join('files', 'mind_map.gv')
    dot.render(mind_map_filename, format='png', cleanup=True)
    return mind_map_filename + '.png'


from deepseek_v2_langchain import deepseek_analyze


def generate_pdf_report(text):
    # 生成复盘内容
    review_prompt = """
    请对以下内容进行全面的复盘分析。包括但不限于：
    1. 主要观点和关键信息总结
    2. 优点和成功之处
    3. 存在的问题或可改进的地方
    4. 未来的行动建议或改进方向

    请提供一个结构化的复盘分析报告，使用Markdown格式。
    使用适当的Markdown语法来组织内容，如标题、列表、强调等。
    """
    review_content = deepseek_analyze(text, review_prompt)

    # 将内容保存为Markdown文件
    md_filename = os.path.join('files', 'review_report.md')
    with open(md_filename, 'w', encoding='utf-8') as f:
        f.write("# 复盘报告\n\n")
        f.write(review_content)

    # 将Markdown转换为HTML
    with open(md_filename, 'r', encoding='utf-8') as f:
        md_content = f.read()
    html_content = markdown.markdown(md_content)

    # 添加一些基本的CSS样式
    css = CSS(string='''
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC&display=swap');
        body { font-family: 'Noto Sans SC', sans-serif; }
        h1 { color: #333366; }
        h2 { color: #666699; }
    ''')

    # 创建PDF
    pdf_filename = os.path.join('files', 'review_report.pdf')
    HTML(string=html_content).write_pdf(pdf_filename, stylesheets=[css])

    return pdf_filename


# 测试函数
if __name__ == "__main__":
    test_text = '''昨天在杨老师阿里服务器上构建了一系列基础设施，比如obsidian同步、halo站点、1panel管理平台等。
遇到一个小插曲，http域名添加ssl转https后一直无法访问，我一直以为是1panel的问题，最后发现是云服务器的443端口没有对外开放。果真要考虑的东西在不同地方藏着，需要一个大脑袋，或者是checklist。

都说现在算法工程师在市场上不如运维实施工程师抢手，这一点我还是有些认同的。算法模型的开源化，让大家都躺平了，定制化二次开发、运维部署成了普通科技企业能做的性价比最高的事情。况且目前成本都在设备端，计算资源成了最大瓶颈，很有意思，这些年软件工程师不断往app里塞各种玩意，就是因为硬件成本的不断降低、硬件配置的不断提高。但是今天大模型成了资源吞噬巨兽，这使得工程师不得不关注硬件资源的使用效率。
Deepseek的模型价格最低，据说就是因为他们有一支强大的运维团队，能够把资源价值用到极致。'''
    mind_map_file, pdf_file = generate(test_text)
    if mind_map_file:
        print(f"思维导图已生成：{mind_map_file}")
    else:
        print("思维导图生成失败")
    if pdf_file:
        print(f"复盘报告已生成：{pdf_file}")
    else:
        print("复盘报告生成失败")
