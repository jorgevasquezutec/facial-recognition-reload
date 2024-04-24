from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from starlette.middleware.cors import CORSMiddleware
from app.config.settings import api_settings
from app.api.api import api_router
import uvicorn


print(api_settings)


docs_url = f'{api_settings.API_PREFIX}/docs'

app = FastAPI(
    title=api_settings.TITLE,
    openapi_url=f'{api_settings.API_PREFIX}/openapi.json',
    docs_url=docs_url,
)

app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
)

app.include_router(api_router, prefix=api_settings.API_PREFIX)


@app.get("/",include_in_schema=False)
async def docs_redirect():
    return RedirectResponse(url=docs_url)


def run ():
    uvicorn.run(app, 
        host=api_settings.HOST, 
        port=api_settings.PORT
        )



if __name__ == "__main__":
    run()
