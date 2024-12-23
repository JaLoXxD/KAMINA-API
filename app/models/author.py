from sqlalchemy import Column, Integer, String, DateTime
from app.database import Base

class Author(Base):
    __tablename__ = "author"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    birth_date = Column(DateTime, nullable=True)