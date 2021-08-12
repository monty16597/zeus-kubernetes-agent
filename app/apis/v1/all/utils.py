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
