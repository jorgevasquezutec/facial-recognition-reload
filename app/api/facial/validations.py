
import filetype
from fastapi import HTTPException, status
from fastapi import HTTPException, File, UploadFile
from app.config.constants import ALOWED_FILE_TYPES,MAX_FILE_SIZE


async def validate_file_size_type(image: UploadFile):
    FILE_SIZE = MAX_FILE_SIZE
    file_info = filetype.guess(image.file)
    if file_info is None:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Unable to determine file type",
        )

    detected_content_type = file_info.extension.lower()

    if (
        image.content_type not in ALOWED_FILE_TYPES
        or detected_content_type not in ALOWED_FILE_TYPES
    ):
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Unsupported file type",
        )

    if(image.size > FILE_SIZE):
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="File too large",
        )

    return image