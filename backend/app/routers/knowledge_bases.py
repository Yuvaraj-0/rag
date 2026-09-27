from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.knowledge_base import KnowledgeBase

from app.schemas.knowledge_base import (
    KnowledgeBaseCreate,
    KnowledgeBaseUpdate,
    KnowledgeBaseResponse
)


router = APIRouter(
    prefix="/knowledge-bases",
    tags=["Knowledge Bases"]
)


@router.post(
    "/",
    response_model=KnowledgeBaseResponse,
    status_code=status.HTTP_201_CREATED
)
def create_knowledge_base(
    data: KnowledgeBaseCreate,
    db: Session = Depends(get_db)
):

    knowledge_base = KnowledgeBase(
        name=data.name,
        description=data.description,
        domain=data.domain
    )

    db.add(knowledge_base)
    db.commit()
    db.refresh(knowledge_base)

    return knowledge_base


@router.get(
    "/",
    response_model=list[KnowledgeBaseResponse]
)
def get_knowledge_bases(
    db: Session = Depends(get_db)
):

    knowledge_bases = db.query(
        KnowledgeBase
    ).order_by(
        KnowledgeBase.created_at.desc()
    ).all()

    return knowledge_bases


@router.get(
    "/{knowledge_base_id}",
    response_model=KnowledgeBaseResponse
)
def get_knowledge_base(
    knowledge_base_id: int,
    db: Session = Depends(get_db)
):

    knowledge_base = db.query(
        KnowledgeBase
    ).filter(
        KnowledgeBase.id == knowledge_base_id
    ).first()

    if not knowledge_base:
        raise HTTPException(
            status_code=404,
            detail="Knowledge base not found"
        )

    return knowledge_base


@router.put(
    "/{knowledge_base_id}",
    response_model=KnowledgeBaseResponse
)
def update_knowledge_base(
    knowledge_base_id: int,
    data: KnowledgeBaseUpdate,
    db: Session = Depends(get_db)
):

    knowledge_base = db.query(
        KnowledgeBase
    ).filter(
        KnowledgeBase.id == knowledge_base_id
    ).first()

    if not knowledge_base:
        raise HTTPException(
            status_code=404,
            detail="Knowledge base not found"
        )

    update_data = data.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(
            knowledge_base,
            key,
            value
        )

    db.commit()
    db.refresh(knowledge_base)

    return knowledge_base


@router.delete(
    "/{knowledge_base_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_knowledge_base(
    knowledge_base_id: int,
    db: Session = Depends(get_db)
):

    knowledge_base = db.query(
        KnowledgeBase
    ).filter(
        KnowledgeBase.id == knowledge_base_id
    ).first()

    if not knowledge_base:
        raise HTTPException(
            status_code=404,
            detail="Knowledge base not found"
        )

    db.delete(knowledge_base)
    db.commit()

    return None