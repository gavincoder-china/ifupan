from sqlalchemy.orm import Session
from app.entity.mind_map_model import MindMap

class MindMapDAO:
    @staticmethod
    def create(db: Session, input_text: str, prompt_type: str, mind_map_file: str, pdf_file: str, md_file: str):
        db_item = MindMap(input_text=input_text, prompt_type=prompt_type, mind_map_file=mind_map_file, pdf_file=pdf_file, md_file=md_file)
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item

    @staticmethod
    def get_by_id(db: Session, item_id: int):
        return db.query(MindMap).filter(MindMap.id == item_id).first()

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100):
        return db.query(MindMap).offset(skip).limit(limit).all()
