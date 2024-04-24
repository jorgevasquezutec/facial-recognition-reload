from typing import List, Optional
from fastapi import APIRouter, Form, Depends, HTTPException, Path, Query, UploadFile
from app.utils.security import get_current_active_user
from fastapi import Depends
from typing_extensions import Annotated
from app.api.facial.validations import validate_file_size_type
from app.api.facial.service import upload_face, detect_face, delete_face, update_face,get_doc_embeding,datatable
from app.dependency import get_db, get_face_detector

router = APIRouter(dependencies=[Depends(get_current_active_user)])


@router.get("") 
def facial_list(
    page: int = Query(0, title="Page", description="Page Number"),
    size: int = Query(10, title="Size", description="Page Size"),
    ids: List[str] = Query([], title="Ids", description="List of Ids"),
    include: List[str] = Query([], title="Include", description="List of Include", example=['embeddings'], alias="include"),
    db = Depends(get_db)
):
    try:
        return datatable(db,page, size, ids, include)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("{document_number}")
def facial_get(
    document_number: Annotated[str, Path(title="Document Number", description="Document Number")],
    db = Depends(get_db)
):
    try:
        return get_doc_embeding(db,document_number)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("",dependencies=[Depends(validate_file_size_type)])
def facial_upload(
    *,
    image : UploadFile,
    document_number: Annotated[str, Form(title="Document Number", description="Document Number")],
    db = Depends(get_db),
    detector = Depends(get_face_detector)
):
    try:
        result = upload_face(db,detector,image, document_number)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/detect")
def facial_detect(
    *,
    image :UploadFile,
    db = Depends(get_db),
    detector = Depends(get_face_detector)
):
    try:
        return detect_face(db,detector,image)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{document_number}")
def facial_delete(
    document_number: Annotated[str, Path(title="Document Number", description="Document Number")],
    db = Depends(get_db)
):
    try:
        return delete_face(db,document_number)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@router.put("/{document_number}")
def facial_update(
    *,
    image : UploadFile,
    document_number: Annotated[str, Path(title="Document Number", description="Document Number")],
    db = Depends(get_db),
    detector = Depends(get_face_detector)
):
    try:
        update_face(db,detector,image, document_number)
        
        return {
            "message": "Se actualizo el registro", 
            "document_number": document_number            
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))