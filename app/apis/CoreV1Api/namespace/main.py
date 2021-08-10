from kubernetes import client
from fastapi import Depends, APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from app.core.auth_controller import decode_jwt_token

router = APIRouter(
    tags=["apis", "corev1api", "namespace"],
    dependencies=[Depends(decode_jwt_token)]
)


@router.get("/namespaces/")
async def namespaces():
    v1 = client.CoreV1Api()
    namespaces = [
        namespace.metadata.name for namespace in v1.list_namespace().items
    ]
    if namespaces:
        return JSONResponse(
            status_code=200,
            content={
                "message": "list of namespaces",
                "data": jsonable_encoder(namespaces)
            }
        )
    else:
        return JSONResponse(
            status_code=404,
            content={
                "message": "No namespace exists",
                "data": ""
            }
        )


@router.get("/namespaces/{namespace}/")
def namespace(namespace):
    v1 = client.CoreV1Api()
    result = None
    for item in v1.list_namespace().items:
        if item.metadata.name == namespace:
            result = item
    if result:
        return JSONResponse(
            status_code=200,
            content={
                "message": "Describe Namespace",
                "data": jsonable_encoder(result.to_dict())
            }
        )
    else:
        return JSONResponse(
            status_code=404,
            content={
                "message": "No namespace exists",
                "data": ""
            }
        )
