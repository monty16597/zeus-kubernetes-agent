from kubernetes import client
from fastapi import Depends, APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from app.core.auth_controller import decode_jwt_token

router = APIRouter(
    tags=['apis', 'v1', 'all'],
    dependencies=[Depends(decode_jwt_token)],
)


def get_pod_restart_status(container_statuses):
    total_restart = 0
    for container in container_statuses:
        total_restart = container.restart_count + total_restart
    return total_restart


def get_pod_status(container_statuses):
    for container in container_statuses:
        if container.state.waiting:
            return False, container.state.waiting.reason
    return True, 'Running'


@router.get('/all/pods/')
@router.get('/all/pod/')
@router.get('/all/po/')
def all_pod():
    v1 = client.CoreV1Api()
    pods = v1.list_pod_for_all_namespaces(watch=False)
    pods = [
        {
            'name': pod.metadata.name,
            'start_time': pod.status.start_time,
            'status': {
                'restart': get_pod_restart_status(pod.status.container_statuses),
                'state': get_pod_status(pod.status.container_statuses)[1]
            }
        } for pod in pods.items
    ]

    return JSONResponse(status_code=200, content={'message': 'All pods', 'data': jsonable_encoder(pods)}) \
        if pods else JSONResponse(status_code=404, content={'message': 'No any pod exists', 'data': ''})


@router.get('/all/services/')
@router.get('/all/service/')
@router.get('/all/svc/')
def all_svc():
    v1 = client.CoreV1Api()
    services = v1.list_service_for_all_namespaces(watch=False)
    services = [
        service.metadata.name for service in services.items
    ]
    return JSONResponse(status_code=200, content={'message': 'All services', 'data': jsonable_encoder(services)}) \
        if services else JSONResponse(status_code=404, content={'message': 'No any service exists', 'data': ''})


@router.get('/all/pvcs/')
@router.get('/all/pvc/')
def all_pvc():
    v1 = client.CoreV1Api()
    pvcs = v1.list_persistent_volume_claim_for_all_namespaces(watch=False)
    pvcs = [
        pvc.metadata.name for pvc in pvcs.items
    ]
    return JSONResponse(status_code=200, content={'message': 'All pvc', 'data': jsonable_encoder(pvcs)}) \
        if pvcs else JSONResponse(status_code=404, content={'message': 'No any pvc exists', 'data': ''})


@router.get('/all/secrets/')
@router.get('/all/secret/')
def all_secret():
    v1 = client.CoreV1Api()
    secrets = v1.list_secret_for_all_namespaces(watch=False)
    secrets = [
        secret.metadata.name for secret in secrets.items
    ]
    return JSONResponse(status_code=200, content={'message': 'All secrets', 'data': jsonable_encoder(secrets)}) \
        if secrets else JSONResponse(status_code=404, content={'message': 'No any secret exists', 'data': ''})


@router.get('/all/configmaps/')
@router.get('/all/configmap/')
@router.get('/all/cm/')
def all_cm():
    v1 = client.CoreV1Api()
    cms = v1.list_config_map_for_all_namespaces(watch=False)
    cms = [
        cm.metadata.name for cm in cms.items
    ]
    return JSONResponse(status_code=200, content={'message': 'All configmap', 'data': jsonable_encoder(cms)}) \
        if cms else JSONResponse(status_code=404, content={'message': 'No any configmap exists', 'data': ''})


@router.get('/all/jobs/')
@router.get('/all/job/')
def all_job():
    v1 = client.BatchV1Api()
    jobs = v1.list_job_for_all_namespaces(watch=False)
    jobs = [
        job.metadata.name for job in jobs.items
    ]
    return JSONResponse(status_code=200, content={'message': 'All jobs', 'data': jsonable_encoder(jobs)}) \
        if jobs else JSONResponse(status_code=404, content={'message': 'No any job exists', 'data': ''})


@router.get('/all/cronjobs/')
@router.get('/all/cronjob/')
def all_cj():
    v1 = client.BatchV1Api()
    jobs = v1.list_cron_job_for_all_namespaces(watch=False)
    jobs = [
        job.metadata.name for job in jobs.items
    ]
    return JSONResponse(status_code=200, content={'message': 'All cronjobs', 'data': jsonable_encoder(jobs)}) \
        if jobs else JSONResponse(status_code=404, content={'message': 'No any cronjob exists', 'data': ''})


@router.get('/all/ingresses/')
@router.get('/all/ingress/')
def all_ingress():
    v1 = client.NetworkingV1beta1Api()
    data = v1.list_ingress_for_all_namespaces(watch=False)
    ingresses = list([
        ingress.metadata.name for ingress in data.items
    ])
    return JSONResponse(status_code=200, content={'message': 'All ingress', 'data': jsonable_encoder(ingresses)}) \
        if ingresses else JSONResponse(status_code=404, content={'message': 'No any ingress exists', 'data': ''})
