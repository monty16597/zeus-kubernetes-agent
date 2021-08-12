from kubernetes import client
from fastapi import Depends, APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from app.core.auth_controller import decode_jwt_token

router = APIRouter(
    tags=['apis', 'v1', 'namespace'],
    dependencies=[Depends(decode_jwt_token)]
)


@router.get('/namespaces/')
@router.get('/namespace/')
async def namespaces():
    v1 = client.CoreV1Api()
    namespaces = [
        namespace.metadata.name for namespace in v1.list_namespace().items
    ]
    return JSONResponse(status_code=200, content={'message': 'ListNamespace', 'data': jsonable_encoder(namespaces)}) \
        if namespaces else JSONResponse(status_code=404, content={'message': 'NoNamespaceExist', 'data': ''})


@router.get('/namespaces/{namespace}/')
@router.get('/namespace/{namespace}/')
def namespace(namespace):
    v1 = client.CoreV1Api()
    result = None
    namespace =  v1.read_namespace(name=namespace).to_dict()
    namespace['metadata'].pop('managed_fields', None)
    return JSONResponse(status_code=200, content={'message': 'DescribeNamespace', 'data': jsonable_encoder(namespaces)}) \
        if namespaces else JSONResponse(status_code=404, content={'message': 'NoNamespaceExist', 'data': ''})
