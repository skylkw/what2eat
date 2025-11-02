from fastapi import FastAPI, Response, Depends
from core.config import Settings, get_settings


app = FastAPI()


@app.get("/")
def read_root(settings: Settings = Depends(get_settings)):
    return {"message": "Hello, World!", "app_name": settings.app_name}


@app.get("/health")
def health_check():
    return Response(content="OK", media_type="text/plain")
