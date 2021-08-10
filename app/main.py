from app.core import auth
from app.apis.v1 import namespace, pods, all
from fastapi import FastAPI
from fastapi.responses import JSONResponse
app = FastAPI(
    title='Zeus K8S Agent',
    description='Connect your kubernetes to the Zeus',
    version='1.0.0',
)

app.include_router(auth.router)
app.include_router(namespace.router)
app.include_router(pods.router)
app.include_router(all.router)


@app.get('/')
def namespaces():
    return JSONResponse(
        status_code=200, content={'message': 'App is running', 'data': True}
    )
