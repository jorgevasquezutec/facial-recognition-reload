from app.app import app
import uvicorn
from app.config.settings import api_settings


if __name__ == "__main__":
    uvicorn.run(app, 
        host=api_settings.HOST, 
        port=api_settings.PORT
        )
