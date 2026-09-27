import os
import shutil

from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session

from app.services.chunker import chunk_text
from app.models.document_chunk import DocumentChunk

from app.database import get_db
from app.models.document import Document
from app.models.knowledge_base import KnowledgeBase
from app.schemas.document import DocumentResponse
from app.services.document_extractor import (
    extract_text,
    extract_csv_records
)

router = APIRouter(
    prefix="/documents",    
    tags=["Documents"]
)


UPLOAD_DIR = "uploads/documents"

os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload", response_model=DocumentResponse)
def upload_document(
    knowledge_base_id: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    # --------------------------------
    # 1. Check Knowledge Base
    # --------------------------------

    knowledge_base = (
        db.query(KnowledgeBase)
        .filter(KnowledgeBase.id == knowledge_base_id)
        .first()
    )

    if not knowledge_base:
        raise HTTPException(
            status_code=404,
            detail="Knowledge Base not found"
        )

    # --------------------------------
    # 2. Check file type
    # --------------------------------

    allowed_extensions = {
        ".pdf",
        ".txt",
        ".csv"
    }

    file_extension = os.path.splitext(
        file.filename
    )[1].lower()

    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Only PDF, TXT, and CSV files are allowed"
        )

    # --------------------------------
    # 3. Create file path
    # --------------------------------

    file_path = os.path.join(
        UPLOAD_DIR,
        file.filename
    )

    # --------------------------------
    # 4. Save file locally
    # --------------------------------

    with open(file_path, "wb") as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )

    # --------------------------------
    # 5. Get file size
    # --------------------------------

    file_size = os.path.getsize(file_path)

    # --------------------------------
    # 6. Save document information
    # --------------------------------

    document = Document(
        knowledge_base_id=knowledge_base_id,
        file_name=file.filename,
        file_path=file_path,
        file_type=file.content_type,
        file_size=file_size,
        status="uploaded"
    )

    db.add(document)
    db.commit()
    db.refresh(document)

        # --------------------------------
    # 7. Extract text and create chunks
    # --------------------------------

    try:

        if file_extension == ".csv":

            # --------------------------------
            # Extract CSV records
            # --------------------------------

            records = extract_csv_records(
                file_path
            )

            print(
                f"Total CSV records: {len(records)}"
            )

            total_chunks = 0

            # --------------------------------
            # Process each record separately
            # --------------------------------

            for record_index, record in enumerate(records):

                record_text = record["text"]

                # Chunk this record
                chunks = chunk_text(
                    record_text
                )

                print(
                    f"Record {record_index}: "
                    f"{len(chunks)} chunks"
                )

                # Save chunks
                for chunk in chunks:

                    document_chunk = DocumentChunk(
                        document_id=document.id,
                        chunk_index=total_chunks,
                        content=chunk
                    )

                    db.add(document_chunk)

                    total_chunks += 1

            print(
                f"Total chunks created: {total_chunks}"
            )

        else:

            # --------------------------------
            # PDF / TXT
            # --------------------------------

           

            extracted_text = extract_text(
                file_path,
                file.filename
            )

            print(
                "\n========== EXTRACTED TEXT ==========\n"
            )

            print(
                extracted_text[:1000]
            )

            print(
                "\n========== END ==========\n"
            )

            chunks = chunk_text(
                extracted_text
            )

            print(
                f"Total chunks created: {len(chunks)}"
            )

            for index, chunk in enumerate(chunks):

                document_chunk = DocumentChunk(
                    document_id=document.id,
                    chunk_index=index,
                    content=chunk
                )

                db.add(document_chunk)

        # --------------------------------
        # Update document status
        # --------------------------------

        document.status = "chunked"

        db.commit()
        db.refresh(document)

    except Exception as e:

        print(
            "Processing failed:",
            str(e)
        )

        document.status = "processing_failed"

        db.commit()

        raise HTTPException(
            status_code=500,
            detail="Failed to process document"
        )
    # --------------------------------
    # 8. Return document
    # --------------------------------

    return document