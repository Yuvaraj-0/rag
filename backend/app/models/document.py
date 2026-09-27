from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.database import Base
from sqlalchemy.orm import relationship

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True)

    knowledge_base_id = Column(
        Integer,
        ForeignKey("knowledge_bases.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    file_name = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    file_size = Column(Integer, nullable=False)

    status = Column(String, default="uploaded", nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    chunks = relationship(
    "DocumentChunk",
    back_populates="document",
    cascade="all, delete-orphan"
)
    knowledge_base = relationship(
        "KnowledgeBase",
        back_populates="documents"
    )