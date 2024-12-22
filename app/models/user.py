from sqlalchemy import Column, Integer, String, DateTime
from app.database import Base

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    hashedPassword = Column(String(255), nullable=False) 
    registerDate = Column(DateTime, nullable=False)