from fastapi import APIRouter, Form, Depends, HTTPException, File, UploadFile
from app.utils.security import get_current_active_user
from fastapi import Depends, Query, Path


router = APIRouter()



@router.get("")
def facial(
    *,
    current_user: dict = Depends(get_current_active_user)
):
    return {"message": "Facial Recognition"}