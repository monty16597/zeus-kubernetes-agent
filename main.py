import os
import jwt
from typing import Optional
from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from kubernetes import client, config
from kubernetes.client.models.v1_namespace import V1Namespace

# Configs can be set in Configuration class directly or using helper utility
if os.environ.get("APP_ENV") == "production":
    config.load_incluster_config()
else:
    config.load_kube_config()
app = FastAPI()

JWT_KEY = os.environ.get('APP_JWT_KEY', 'cLSYLkHwQcznat89JcgWTwqM6innaUufHmLVjAf4EQT9FDQVnsz6LkBtjo78GUQP')
JWT_ALGORITHM = os.environ.get('APP_JWT_ALGO', 'HS256')

FakeDb = {
    'admin': {
        'username': 'admin',
        'password': 'EQu8KsnFs9X9lJhuU7rFgz4gIFT7qtLy24eDoDCOLh65ElVOWtZTV8BMalBpCMEw'
    }
}

def check_user_in_db(username, password):
    return True if FakeDb.get(username) and FakeDb.get(username).get("password") == password else False

oauth_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/token")
async def token_generator(form_data: OAuth2PasswordRequestForm = Depends()):
    return {'access_token': jwt.encode({'username': form_data.username, "password": form_data.password}, JWT_KEY, algorithm=JWT_ALGORITHM), 'token_type': 'bearer'} 

@app.get("/")
def namespaces():
    return JSONResponse(status_code=200, content={"message": "App is running", "data": True})

@app.get("/namespaces/")
def namespaces(token: str = Depends(oauth_scheme)):
    payload = jwt.decode(token, JWT_KEY, algorithms=[JWT_ALGORITHM])
    if check_user_in_db(payload.get('username'), payload.get('password')):
        v1 = client.CoreV1Api()
        namespaces = [
            namespace.metadata.name for namespace in v1.list_namespace().items
        ]
        if namespaces:
            return JSONResponse(status_code=200, content={"message": "list of namespaces", "data": jsonable_encoder(namespaces)})
        else:
            return JSONResponse(status_code=404, content={"message": "No namespace exists", "data": ""})
    else:
        return JSONResponse(status_code=403, content={"message": "Invalid user", "data": ""})

@app.get("/namespaces/{namespace}/")
def namespace(namespace, token: str = Depends(oauth_scheme)):
    payload = jwt.decode(token, JWT_KEY, algorithms=[JWT_ALGORITHM])
    if check_user_in_db(payload.get('username'), payload.get('password')):
        v1 = client.CoreV1Api()
        for namespace in v1.list_namespace().items:
            if namespace.metadata.name == namespace:
                namespace = namespace
        if namespace:
            return JSONResponse(status_code=200, content={"message": "Describe Namespace", "data": jsonable_encoder(namespace.to_dict())})
        else:
            return JSONResponse(status_code=404, content={"message": "No namespace exists", "data": ""})
    else:
        return JSONResponse(status_code=403, content={"message": "Invalid user", "data": ""})


@app.get("/namespaces/{namespace}/pods/")
def namespaced_pods(namespace, token: str = Depends(oauth_scheme)):
    payload = jwt.decode(token, JWT_KEY, algorithms=[JWT_ALGORITHM])
    if check_user_in_db(payload.get('username'), payload.get('password')):
        v1 = client.CoreV1Api()
        pods = [
            pods.metadata.name for pods in v1.list_namespaced_pod(namespace=namespace).items
        ]
        if pods:
            return JSONResponse(status_code=200, content={"message": "List of pods", "data": jsonable_encoder(pods)})
        else:
            return JSONResponse(status_code=404, content={"message": "No any pod exists", "data": ""})
    else:
        return JSONResponse(status_code=403, content={"message": "Invalid user", "data": ""})

@app.get("/namespaces/{namespace}/pods/{pod}/")
def namespaced_pod(namespace: str, pod: str, token: str = Depends(oauth_scheme)):
    payload = jwt.decode(token, JWT_KEY, algorithms=[JWT_ALGORITHM])
    if check_user_in_db(payload.get('username'), payload.get('password')):
        v1 = client.CoreV1Api()
        pod = next(pods for pods in v1.list_namespaced_pod(namespace=namespace).items if pods.metadata.name == pod)
        if pod:
            return JSONResponse(status_code=200, content={"message": "Describe pod", "data": jsonable_encoder(pod.to_dict())})
        else:
            return JSONResponse(status_code=404, content={"message": "No any pod exists", "data": ""})
    else:
        return JSONResponse(status_code=403, content={"message": "Invalid user", "data": ""})