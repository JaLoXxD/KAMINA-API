from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Book(Base):
  __tablename__ = "book"

  id = Column(Integer, primary_key=True, index=True)
  title = Column(String(50), nullable=False)
  published_year = Column(Integer, nullable=True)
  author_id = Column(Integer, ForeignKey('author.id'), nullable=False)
  user_id = Column(Integer, ForeignKey('user.id'), nullable=True)

  author = relationship("Author")
  user = relationship("User")