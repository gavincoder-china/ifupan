from sqlalchemy.orm import Session
from ifupan.app.dao.do.mind_map_dao import MindMapDAO
from ifupan.utils.deepseek_v2_langchain import deepseek_analyze
from ifupan.app.services.text_analysis_service import TextAnalysisService
import ast
import logging
import re
import os
import graphviz
import markdown
from weasyprint import HTML, CSS

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

if not os.path.exists('files'):
    os.makedirs('files')

class MindMapService:
    @staticmethod
    async def generate_and_save(db: Session, input_text: str, prompt_type: str):
        mind_map_file, pdf_file = MindMapService.generate(input_text, prompt_type)
        return await MindMapDAO.create(db, input_text, prompt_type, mind_map_file, pdf_file)

    @staticmethod
    async def get_mind_map_by_id(db: Session, mind_map_id: int):
        return await MindMapDAO.get_by_id(db, mind_map_id)

    @staticmethod
    async def get_all_mind_maps(db: Session, skip: int = 0, limit: int = 100):
        return await MindMapDAO.get_all(db, skip, limit)

    @staticmethod
    def generate(text, prompt_type):
        mind_map_file = None
        pdf_file = None

        try:
            mind_map_file = MindMapService.generate_mind_map(text)
            logging.info(f"思维导图已生成：{mind_map_file}")
        except Exception as e:
            logging.error(f"生成思维导图时发生错误: {str(e)}")

        try:
            pdf_file = MindMapService.generate_pdf_report(text, prompt_type)
            logging.info(f"复盘报告已生成：{pdf_file}")
        except Exception as e:
            logging.error(f"生成PDF报告时发生错误: {str(e)}")

        return mind_map_file, pdf_file

    @staticmethod
    def generate_mind_map(text):
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
        dict_match = re.search(r'\{.*\}', structure_str, re.DOTALL)
        if dict_match:
            dict_str = dict_match.group()
        else:
            raise ValueError("无法从模型输出中提取字典结构")

        try:
            structure = ast.literal_eval(dict_str)
        except:
            raise ValueError("无法解析模型输出为有效的Python字典")

        dot = graphviz.Digraph(comment='Mind Map')
        dot.attr(rankdir='LR')

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

        mind_map_filename = os.path.join('files', 'mind_map.gv')
        dot.render(mind_map_filename, format='png', cleanup=True)
        return mind_map_filename + '.png'

    @staticmethod
    def generate_pdf_report(text, prompt_type):
        review_content = TextAnalysisService.analyze(text, prompt_type)

        md_filename = os.path.join('files', 'review_report.md')
        with open(md_filename, 'w', encoding='utf-8') as f:
            f.write("# 复盘报告\n\n")
            f.write(review_content)

        with open(md_filename, 'r', encoding='utf-8') as f:
            md_content = f.read()
        html_content = markdown.markdown(md_content)

        css = CSS(string='''
            @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC&display=swap');
            body { font-family: 'Noto Sans SC', sans-serif; }
            h1 { color: #333366; }
            h2 { color: #666699; }
        ''')

        pdf_filename = os.path.join('files', 'review_report.pdf')
        HTML(string=html_content).write_pdf(pdf_filename, stylesheets=[css])

        return pdf_filename
