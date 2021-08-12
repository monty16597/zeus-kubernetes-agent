from kubernetes import client
from fastapi import Depends, APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from app.core.auth_controller import decode_jwt_token

router = APIRouter(
    tags=['apis', 'v1', 'pods'],
    dependencies=[Depends(decode_jwt_token)],
)


@router.get('/namespaces/{namespace}/pods/')
def namespaced_pods(namespace):
    v1 = client.CoreV1Api()
    pods = [
        pods.metadata.name for pods in v1.list_namespaced_pod(namespace=namespace).items
    ]
    return JSONResponse(
        status_code=200,
        content={'message': 'ListPod', 'data': jsonable_encoder(pods)}) \
        if pods else JSONResponse(
            status_code=404, content={'message': 'NoPodExist', 'data': ''}
        )


@router.get('/namespace/{namespace}/pod/{pod}/')
@router.get('/namespace/{namespace}/pod/{pod}/')
def namespaced_pod(namespace: str, pod: str):
    v1 = client.CoreV1Api()
    pod = v1.read_namespaced_pod(namespace=namespace, name=pod).to_dict()
    pod['metadata'].pop('managed_fields')
    pod['metadata']['annotations'].pop('kubectl.kubernetes.io/last-applied-configuration', None)
    return JSONResponse(status_code=200, content={'message': 'DescribePod', 'data': jsonable_encoder(pod)}) \
        if pod else JSONResponse(status_code=404, content={'message': 'NoPodExist', 'data': ''})
