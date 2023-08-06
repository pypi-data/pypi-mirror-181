import time

from airflow.providers.cncf.kubernetes.utils.pod_manager import PodManager, PodPhase
from kubernetes.client import V1Pod


def container_is_completed(pod: V1Pod, container_name: str) -> bool:
    """
    Examines V1Pod ``pod`` to determine whether ``container_name`` is completed.
    If that container is present and completed, returns True.  Returns False otherwise.
    """
    container_statuses = pod.status.container_statuses if pod and pod.status else None
    if not container_statuses:
        return False
    container_status = next(iter([x for x in container_statuses if x.name == container_name]), None)
    if not container_status:
        return False
    return container_status.state.terminated is not None


def container_is_succeeded(pod: V1Pod, container_name: str) -> bool:
    """
    Examines V1Pod ``pod`` to determine whether ``container_name`` is completed and succeeded.
    If that container is present and completed and succeeded, returns True.  Returns False otherwise.
    """
    if not container_is_completed(pod, container_name):
        return False
    container_statuses = pod.status.container_statuses if pod and pod.status else None
    container_status = next(iter([x for x in container_statuses if x.name == container_name]), None)
    return container_status.state.terminated.exit_code == 0


class IstioPodManager(PodManager):
    def container_is_completed(self, pod: V1Pod, container_name: str) -> bool:
        """Reads pod and checks if container is completed"""
        remote_pod = self.read_pod(pod)
        return container_is_completed(pod=remote_pod, container_name=container_name)

    def container_is_succeeded(self, pod: V1Pod, container_name: str) -> bool:
        """Reads pod and checks if container is completed"""
        remote_pod = self.read_pod(pod)
        return container_is_succeeded(pod=remote_pod, container_name=container_name)

    def await_pod_completion(self, pod: V1Pod) -> V1Pod:
        """
        Monitors a pod and returns the final state
        (neglect sidecar state e.g. istio-proxy, vault-agent)
        :param pod: pod spec that will be monitored
        :return:  Tuple[State, Optional[str]]
        """
        while True:
            remote_pod = self.read_pod(pod)
            if remote_pod.status.phase in PodPhase.terminal_states:
                break
            if remote_pod.status.phase == PodPhase.RUNNING and self.container_is_completed(remote_pod, 'base'):
                break
            self.log.info('Pod %s has phase %s', pod.metadata.name, remote_pod.status.phase)
            time.sleep(2)
        return remote_pod


class IstioKubernetesPodOperator(KubernetesPodOperator):
    @cached_property
    def pod_manager(self) -> IstioPodManager:
        return IstioPodManager(kube_client=self.client)

    def cleanup(self, pod: V1Pod, remote_pod: V1Pod):
        pod_phase = remote_pod.status.phase if hasattr(remote_pod, 'status') else None
        if pod_phase != PodPhase.SUCCEEDED and not self.pod_manager.container_is_succeeded(pod, 'base'):
            if self.log_events_on_failure:
                with _suppress(Exception):
                    for event in self.pod_manager.read_pod_events(pod).items:
                        self.log.error("Pod Event: %s - %s", event.reason, event.message)
            if not self.is_delete_operator_pod:
                with _suppress(Exception):
                    self.patch_already_checked(pod)
            with _suppress(Exception):
                self.process_pod_deletion(pod)
            raise AirflowException(f'Pod {pod and pod.metadata.name} returned a failure: {remote_pod}')
        else:
            with _suppress(Exception):
                self.process_pod_deletion(pod)
