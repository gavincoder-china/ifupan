from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from config.database import Base

class Prompt(Base):
    __tablename__ = "prompts"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def to_dict(self):
        return {
            'id': self.id,
            'code': self.code,
            'name': self.name,
            'content': self.content,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
