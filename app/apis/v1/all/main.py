from app.core.utils import return_json_resp
from kubernetes import client
from fastapi import Depends, APIRouter
from app.core.auth_controller import decode_jwt_token
from .utils import get_pod_restart_status, get_pod_status

router = APIRouter(
    tags=['apis', 'v1', 'all'],
    dependencies=[Depends(decode_jwt_token)],
)


@router.get('/all/pods/')
@router.get('/all/pod/')
@router.get('/all/po/')
def all_pod():
    v1 = client.CoreV1Api()
    pods = v1.list_pod_for_all_namespaces(watch=False)
    pods = [
        {
            'name': pod.metadata.name,
            'namespace': pod.metadata.namespace,
            'start_time': pod.status.start_time,
            'status': {
                'restart': get_pod_restart_status(pod.status.container_statuses),
                'state': get_pod_status(pod.status.container_statuses)[1]
            }
        } for pod in pods.items
    ]
    return return_json_resp(message='AllPod', data=pods)


@router.get('/all/services/')
@router.get('/all/service/')
@router.get('/all/svc/')
def all_svc():
    v1 = client.CoreV1Api()
    services = v1.list_service_for_all_namespaces(watch=False)
    services = [
        service.metadata.name for service in services.items
    ]
    return return_json_resp(message='AllService', data=services)


@router.get('/all/pvcs/')
@router.get('/all/pvc/')
def all_pvc():
    v1 = client.CoreV1Api()
    pvcs = v1.list_persistent_volume_claim_for_all_namespaces(watch=False)
    pvcs = [
        pvc.metadata.name for pvc in pvcs.items
    ]
    return return_json_resp(message='AllPvc', data=pvcs)


@router.get('/all/secrets/')
@router.get('/all/secret/')
def all_secret():
    v1 = client.CoreV1Api()
    secrets = v1.list_secret_for_all_namespaces(watch=False)
    secrets = [
        secret.metadata.name for secret in secrets.items
    ]
    return return_json_resp(message='AllSecret', data=secrets)


@router.get('/all/configmaps/')
@router.get('/all/configmap/')
@router.get('/all/cm/')
def all_cm():
    v1 = client.CoreV1Api()
    cms = v1.list_config_map_for_all_namespaces(watch=False)
    cms = [
        cm.metadata.name for cm in cms.items
    ]
    return return_json_resp(message='AllConfigMap', data=cms)


@router.get('/all/jobs/')
@router.get('/all/job/')
def all_job():
    v1 = client.BatchV1Api()
    jobs = v1.list_job_for_all_namespaces(watch=False)
    jobs = [
        job.metadata.name for job in jobs.items
    ]
    return return_json_resp(message='AllJob', data=jobs)


@router.get('/all/cronjobs/')
@router.get('/all/cronjob/')
def all_cj():
    v1 = client.BatchV1Api()
    jobs = v1.list_cron_job_for_all_namespaces(watch=False)
    jobs = [
        job.metadata.name for job in jobs.items
    ]
    return return_json_resp(message='AllCronJob', data=jobs)


@router.get('/all/ingresses/')
@router.get('/all/ingress/')
def all_ingress():
    v1 = client.NetworkingV1beta1Api()
    data = v1.list_ingress_for_all_namespaces(watch=False)
    ingresses = list([
        ingress.metadata.name for ingress in data.items
    ])
    return return_json_resp(message='AllIngress', data=ingresses)
