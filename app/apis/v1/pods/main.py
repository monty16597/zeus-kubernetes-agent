from app.core.utils import return_json_resp
from kubernetes import client
from fastapi import Depends, APIRouter, Query
from app.core.auth_controller import decode_jwt_token
from typing import Optional

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
    return return_json_resp(message='ListPod', data=pods)


@router.get('/namespace/{namespace}/pod/{pod_name}/')
@router.get('/namespace/{namespace}/pod/{pod_name}/')
def namespaced_pod_description(namespace: str, pod_name: str):
    v1 = client.CoreV1Api()
    pod = v1.read_namespaced_pod(namespace=namespace, name=pod_name).to_dict()
    if pod.get('metadata', None):
        pod['metadata'].pop('managed_fields')
        if pod['metadata'].get('annotations', None):
            pod['metadata']['annotations'].pop('kubectl.kubernetes.io/last-applied-configuration', None)
    return return_json_resp(message='DescribePod', data=pod)


@router.get('/namespace/{namespace}/pod/{pod_name}/log/')
@router.get('/namespace/{namespace}/pod/{pod_name}/logs/')
def namespaced_pod_logs(
    namespace: str,
    pod_name: str,
    container: Optional[str] = Query(None),
    tail: Optional[int] = Query(None),
    timestamps: Optional[bool] = Query(False),
    since: Optional[int] = Query(None),
):
    """
    param: namespace: (path: str): name of the namespace
    param: pods_name: (path: str): name of the pod
    param: container: (query param: str): name of the container in the pod
    param: tail: (query param: int): the number of lines from the end of the logs to show.
    param: timestamps: (query param: bool): add timestamps to each log line.
    param: since: (query param: int): A relative time in seconds before the current time from which to show logs.
    """
    v1 = client.CoreV1Api()
    try:
        pod = v1.read_namespaced_pod(namespace=namespace, name=pod_name).to_dict()
        if container or len(pod['spec'].get('containers', [])) == 1:
            log = v1.read_namespaced_pod_log(
                namespace=namespace,
                name=pod_name,
                container=container,
                tail_lines=tail,
                timestamps=timestamps,
                since_seconds=since
            )
        elif not container and len(pod['spec'].get('containers', [])) > 1:
            log = ''
            for container in pod['spec'].get('containers', []):
                log = log + v1.read_namespaced_pod_log(
                    namespace=namespace,
                    name=pod_name,
                    container=container.get('name'),
                    tail_lines=tail,
                    timestamps=timestamps,
                    since_seconds=since
                )
    except Exception as e:
        print('Error while getting logs:', e)
        log = None
    return return_json_resp(message='GetPodLog', data=log)
