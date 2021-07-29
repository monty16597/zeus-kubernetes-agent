from kubernetes import client
from fastapi import Depends, APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from app.core.auth_controller import decode_jwt_token

router = APIRouter(
    tags=["apis", "corev1api", "pods"],
    dependencies=[Depends(decode_jwt_token)]
)

@router.get("/namespaces/{namespace}/pods/")
def namespaced_pods(namespace):
    v1 = client.CoreV1Api()
    pods = [
        pods.metadata.name for pods in v1.list_namespaced_pod(namespace=namespace).items
    ]
    return JSONResponse(status_code=200, content={"message": "List of pods", "data": jsonable_encoder(pods)}) \
        if pods else JSONResponse(status_code=404, content={"message": "No any pod exists", "data": ""})

@router.get("/namespaces/{namespace}/pods/{pod}/")
def namespaced_pod(namespace: str, pod: str):
    v1 = client.CoreV1Api()
    pod = next(pods for pods in v1.list_namespaced_pod(namespace=namespace).items if pods.metadata.name == pod)
    return JSONResponse(status_code=200, content={"message": "Describe pod", "data": jsonable_encoder(pod.to_dict())}) \
        if pod else JSONResponse(status_code=404, content={"message": "No any pod exists", "data": ""})