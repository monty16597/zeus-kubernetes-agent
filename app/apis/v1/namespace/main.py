from kubernetes import client
from fastapi import Depends, APIRouter
from app.core.auth_controller import decode_jwt_token
from app.core.utils import return_json_resp

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
    return return_json_resp(data=namespaces, message='ListNamespace')


@router.get('/namespaces/{namespace}/')
@router.get('/namespace/{namespace}/')
def namespace(namespace):
    v1 = client.CoreV1Api()
    try:
        namespace = v1.read_namespace(name=namespace).to_dict()
        namespace['metadata'].pop('managed_fields', None)
    except Exception as e:
        print('Error:', e)
        namespace = None
    return return_json_resp(data=namespace, message='DescribeNamespace')
