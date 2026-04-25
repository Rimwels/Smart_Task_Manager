from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String, nullable=False)

    email = Column(String, nullable=False, unique=True, index=True)

    password = Column(String, nullable=False)

    role = Column(String,default="user", nullable=False)

    tasks = relationship("Task", back_populates="owner")