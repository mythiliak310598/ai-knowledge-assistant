import os
from app.utils.text_extractor import extract_text
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from app.db.database import get_db
from sqlalchemy.orm import Session
from app.db.models import Document, DocumentChunk
from app.services.text_chunker import chunk_text
from app.services.embedding_services import generate_embedding
from app.schemas.documents import DocumentCreate, DocumentUpdate, DocumentResponse
import zipfile
from io import BytesIO

router = APIRouter()
@router.post("/documents/upload")
def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    allowed_extension = ['.pdf', '.docx']
    extension = os.path.splitext(file.filename)[1].lower()

    if extension not in allowed_extension:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type. Only PDF and DOCX files are allowed."
        )
    
    # STEP 1: Create upload directory
    upload_dir = "uploads"      
    # Create the uploads folder if it doesn't already exist.
    os.makedirs(upload_dir, exist_ok=True)

    # STEP 2: Create file path
    file_path = os.path.join(upload_dir, file.filename)

    # STEP 3: File Duplication Handling
    if os.path.exists(file_path):
        print('Filename already exists')
        # It splits a filename into two parts: filename -> name + extension
        name, extension = os.path.splitext(file.filename)

        counter = 1

        while True:
            new_file_name = f"{name}-{counter}{extension}"
            new_file_path = os.path.join(upload_dir, new_file_name)
            if not os.path.exists(new_file_path):
                file_path = new_file_path
                break
            counter += 1

    # STEP 3.1: Validate actual PDF file
    if extension == ".pdf":
        # Read first 5 bytes of the uploaded file
        file_header = file.file.read(5)

        # Reset file pointer back to the beginning
        # because STEP 4 needs to read the complete file
        file.file.seek(0)

        # A valid PDF should start with %PDF-
        if file_header != b"%PDF-":
            raise HTTPException(
                status_code=400,
                detail="Invalid PDF file"
            )

    # STEP 3.2: Validate actual DOCX file
    if extension == ".docx":
        # Read uploaded DOCX into memory
        file_bytes = file.file.read()

        # Reset pointer because STEP 4 will read the file again
        file.file.seek(0)
        try:
            # DOCX is internally a ZIP file
            with zipfile.ZipFile(BytesIO(file_bytes)) as docx_zip:

                file_names = docx_zip.namelist()

                # These files should exist inside a valid Word DOCX
                if (
                    "[Content_Types].xml" not in file_names
                    or "word/document.xml" not in file_names
                ):
                    raise HTTPException(
                        status_code=400,
                        detail="Invalid DOCX file"
                    )

        except zipfile.BadZipFile:
            raise HTTPException(
                status_code=400,
                detail="Invalid DOCX file"
            )

    # STEP 4: Save uploaded file
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())

    # STEP 5: Extract text from PDF/DOCX
    try:
        text = extract_text(file_path)
        print(text)
    except Exception:
        # Try to remove the corrupted/invalid uploaded file
        try:
                if os.path.exists(file_path):
                    os.remove(file_path)

        # If Windows is still locking the file,
        # don't allow the cleanup error to become a 500 error
        except (PermissionError, OSError):
                pass

        # The actual problem is invalid/corrupted user input
        raise HTTPException(
            status_code=400,
            detail="Unable to read the document. The file may be corrupted or invalid."
        )
    try:
        # STEP 6: Split extracted text into chunks
        chunks = chunk_text(text)
        print(chunks)
        
        # STEP 7: Create the parent Document record 
        document = Document(
            filename = file.filename,
            file_path = file_path
        )
        db.add(document)
        # Flush sends the INSERT to the database. 
        # Once database is inserted we will get the id right
        db.flush()

        # STEP 8: Create one DocumentChunk for every chunk
        # why start 1 -> instead of starting chunk from 0 it will start from 1
        for index, chunk in enumerate(chunks, start = 1):
                embedding = generate_embedding(chunk)
                document_chunks = DocumentChunk(
                    document_id = document.id,
                    chunk_index = index,
                    content = chunk,
                    embedding = embedding
                )
                db.add(document_chunks)

        db.commit()
        db.refresh(document)
        return document
    except Exception:
        db.rollback()
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except OSError:
            pass
        raise HTTPException(
            status_code=500,
            detail="Failed to process the document"
        )
@router.post("/documents", response_model = DocumentResponse)
def create_document(
    document_data : DocumentCreate,
    db: Session = Depends(get_db)
):
        document = Document(
            filename=document_data.filename,
            file_path=document_data.file_path
        )
        if document is None:
                    db.rollback()
                    raise HTTPException(
                        status_code=500,
                        details="Failed to create document"
                    )
        
        db.add(document)
        db.commit()
        db.refresh(document)
        return document
   

@router.get("/documents", response_model=list[DocumentResponse])
def get_documents(db:Session = Depends(get_db)):
    try:
        document = db.query(Document).all()
        return document
    except Exception:
        db.rollback()
        raise Exception(
            status_code=400,
            detail="Failed to retrieve documents"
        )

@router.put("/documents/{document_id}", response_model=DocumentResponse)
def update_documents(
    document_id: int,
    document_data:  DocumentUpdate,
    db : Session = Depends(get_db)
):
        documents = db.get(Document, document_id)
         # Document doesn't exist
        if documents is None:
            raise HTTPException(
                status_code=404,
                detail="Document not found"
            )
        try:
            if documents:
                documents.filename = document_data.filename
                documents.file_path = document_data.file_path
                db.commit()
                db.refresh(documents)
        except Exception:
            # Undo database changes if update fails
            db.rollback()

            raise HTTPException(
                status_code=500,
                detail="Failed to update document"
            )

        else:
            print('Document not found')
        return documents


@router.delete('/documents/{document_id}')
def delete_document(document_id:int, db: Session = Depends(get_db)):
    document = db.get(Document, document_id)
    try:
        if document:
            db.delete(document)
            db.commit()
    except Exception:
        # Undo delete if database operation fails
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail="Failed to delete document"
        )
    else: 
        print('Document not available')