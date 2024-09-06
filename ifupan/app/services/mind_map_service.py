from sqlalchemy.orm import Session
from ifupan.app.dao.do.mind_map_dao import MindMapDAO
from ifupan.app.services.mind_map_generator import generate

class MindMapService:
    @staticmethod
    async def generate_and_save(db: Session, input_text: str, prompt_type: str):
        mind_map_file, pdf_file = generate(input_text, prompt_type)
        return await MindMapDAO.create(db, input_text, prompt_type, mind_map_file, pdf_file)

    @staticmethod
    async def get_mind_map_by_id(db: Session, mind_map_id: int):
        return await MindMapDAO.get_by_id(db, mind_map_id)

    @staticmethod
    async def get_all_mind_maps(db: Session, skip: int = 0, limit: int = 100):
        return await MindMapDAO.get_all(db, skip, limit)
