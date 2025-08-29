# backend/app/models/todo.py
from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey
from app.database.database import Base

class Todo(Base):
    __tablename__ = "todos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    completed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    # Optional: if you attach todos to users later:
    # owner_id: Mapped[int] = mapped_column(Integer, nullable=True)
    
    # Foreign key to users table
    # owner_id: Mapped[str] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)


    # Many-to-one relationship
    owner = relationship("User", back_populates="todos")