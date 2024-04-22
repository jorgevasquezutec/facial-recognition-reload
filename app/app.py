from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.config.settings import api_settings
from app.api.api import api_router
import uvicorn
from app.dependency import ChromaInstance, DetectorInstance
from app.face_detector import FaceDetector
from app.dbchroma import DbChroma




app = FastAPI(
    title=api_settings.TITLE,
    openapi_url=f'{api_settings.PREFIX}/openapi.json',
    docs_url=f'{api_settings.PREFIX}/docs',
)

app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
)

app.include_router(api_router, prefix=api_settings.PREFIX)


if __name__ == "__main__":
    uvicorn.run(app, 
        host=api_settings.HOST, 
        port=api_settings.PORT
        )
