from app.core import auth
from app.apis.CoreV1Api import namespace, pods
from fastapi import FastAPI
from fastapi.responses import JSONResponse
app = FastAPI()

app.include_router(auth.router)
app.include_router(namespace.router)
app.include_router(pods.router)

@app.get("/")
def namespaces():
    return JSONResponse(status_code=200, content={"message": "App is running", "data": True})