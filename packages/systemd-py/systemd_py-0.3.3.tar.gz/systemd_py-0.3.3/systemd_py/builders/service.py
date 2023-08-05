"""
# Service Builder 🏗️
Builder for the `service` section of a systemd service file.

"""

from typing import Optional
from typing import List

from ._builder import _Builder
from ..core.models import Service
from ..core.types import TypeType, RestartType


class ServiceBuilder(_Builder):
    """
    Builder for the `service` section of a systemd service file.
    """

    __slots__ = (
        '_type',
        '_remain_after_exit',
        '_pid_file',
        '_bus_name',
        '_notify_access',
        '_exec_start',
        '_exec_start_pre',
        '_exec_start_post',
        '_exec_reload',
        '_exec_stop',
        '_exec_stop_post',
        '_restart_sec',
        '_restart',
        '_timeout_sec',
        '_user',
        '_group',
        '_nice'
    )

    @property
    def allowed_none_fields(self) -> List[str]:
        """
        Returns a list of fields that are allowed to be None


        :return: List of fields that are allowed to be None
        :rtype: List[str]
        """

        return [
            "_type", "_remain_after_exit", "_pid_file", "_bus_name", "_notify_access",
            "_exec_start", "_exec_start_pre", "_exec_start_post", "_exec_reload", "_exec_stop",
            "_exec_stop_post", "_restart_sec", "_restart", "_timeout_sec", "_user", "_group",
            "_nice"
        ]

    def __init__(self):
        self._type: Optional[TypeType] = None
        self._remain_after_exit: Optional[bool] = None
        self._pid_file: Optional[str] = None
        self._bus_name: Optional[str] = None
        self._notify_access: Optional[str] = None
        self._exec_start: Optional[List[str]] = None
        self._exec_start_pre: Optional[List[str]] = None
        self._exec_start_post: Optional[List[str]] = None
        self._exec_reload: Optional[List[str]] = None
        self._exec_stop: Optional[List[str]] = None
        self._exec_stop_post: Optional[List[str]] = None
        self._restart_sec: Optional[int] = None
        self._restart: Optional[RestartType] = None
        self._timeout_sec: Optional[int] = None
        self._user: Optional[str] = None
        self._group: Optional[str] = None
        self._nice: Optional[int] = None

    def build(self) -> Service:
        """
        Builds the `service` section of a systemd service file.

        :return: The `service` section of a systemd service file
        :rtype: Service
        """

        self._check()
        return Service(
            type=self._type,
            remain_after_exit=self._remain_after_exit,
            pid_file=self._pid_file,
            bus_name=self._bus_name,
            notify_access=self._notify_access,
            exec_start=self._exec_start,
            exec_start_pre=self._exec_start_pre,
            exec_start_post=self._exec_start_post,
            exec_reload=self._exec_reload,
            exec_stop=self._exec_stop,
            exec_stop_post=self._exec_stop_post,
            restart_sec=self._restart_sec,
            restart=self._restart,
            timeout_sec=self._timeout_sec,
            user=self._user,
            group=self._group,
            nice=self._nice
        )

    def with_type(self, type: TypeType) -> 'ServiceBuilder':
        """
        Sets the `type` field of the `service` section of a systemd service file.

        :param type: The `type` field of the `service` section of a systemd service file
        :type type: TypeType

        :return: The `ServiceBuilder` object
        :rtype: ServiceBuilder
        """

        self._type = type
        return self

    def with_remain_after_exit(self, remain_after_exit: bool) -> 'ServiceBuilder':
        """
        Sets the `remain_after_exit` field of the `service` section of a systemd service file.

        :param remain_after_exit: The `remain_after_exit` field of the `service` section of a systemd service file
        :type remain_after_exit: bool

        :return: The `ServiceBuilder` object
        :rtype: ServiceBuilder
        """

        self._remain_after_exit = remain_after_exit
        return self

    def with_pid_file(self, pid_file: str) -> 'ServiceBuilder':
        """
        Sets the `pid_file` field of the `service` section of a systemd service file.

        :param pid_file: The `pid_file` field of the `service` section of a systemd service file
        :type pid_file: str

        :return: The `ServiceBuilder` object
        :rtype: ServiceBuilder
        """

        self._pid_file = pid_file
        return self

    def with_bus_name(self, bus_name: str) -> 'ServiceBuilder':
        """
        Sets the `bus_name` field of the `service` section of a systemd service file.

        :param bus_name: The `bus_name` field of the `service` section of a systemd service file
        :type bus_name: str

        :return: The `ServiceBuilder` object
        :rtype: ServiceBuilder
        """

        self._bus_name = bus_name
        return self

    def with_notify_access(self, notify_access: str) -> 'ServiceBuilder':
        """
        Sets the `notify_access` field of the `service` section of a systemd service file.

        :param notify_access: The `notify_access` field of the `service` section of a systemd service file
        :type notify_access: str

        :return: The `ServiceBuilder` object
        :rtype: ServiceBuilder
        """

        self._notify_access = notify_access
        return self

    def with_exec_start(self, exec_start: List[str]) -> 'ServiceBuilder':
        """
        Sets the `exec_start` field of the `service` section of a systemd service file.

        :param exec_start: The `exec_start` field of the `service` section of a systemd service file
        :type exec_start: List[str]

        :return: The `ServiceBuilder` object
        :rtype: ServiceBuilder
        """

        self._exec_start = exec_start
        return self

    def with_exec_start_pre(self, exec_start_pre: List[str]) -> 'ServiceBuilder':
        """
        Sets the `exec_start_pre` field of the `service` section of a systemd service file.

        :param exec_start_pre: The `exec_start_pre` field of the `service` section of a systemd service file
        :type exec_start_pre: List[str]

        :return: The `ServiceBuilder` object
        :rtype: ServiceBuilder
        """

        self._exec_start_pre = exec_start_pre
        return self

    def with_exec_start_post(self, exec_start_post: List[str]) -> 'ServiceBuilder':
        """
        Sets the `exec_start_post` field of the `service` section of a systemd service file.

        :param exec_start_post: The `exec_start_post` field of the `service` section of a systemd service file
        :type exec_start_post: List[str]

        :return: The `ServiceBuilder` object
        :rtype: ServiceBuilder
        """

        self._exec_start_post = exec_start_post
        return self

    def with_exec_reload(self, exec_reload: List[str]) -> 'ServiceBuilder':
        """
        Sets the `exec_reload` field of the `service` section of a systemd service file.

        :param exec_reload: The `exec_reload` field of the `service` section of a systemd service file
        :type exec_reload: List[str]

        :return: The `ServiceBuilder` object
        :rtype: ServiceBuilder
        """

        self._exec_reload = exec_reload
        return self

    def with_exec_stop(self, exec_stop: List[str]) -> 'ServiceBuilder':
        """
        Sets the `exec_stop` field of the `service` section of a systemd service file.

        :param exec_stop: The `exec_stop` field of the `service` section of a systemd service file
        :type exec_stop: List[str]

        :return: The `ServiceBuilder` object
        :rtype: ServiceBuilder
        """

        self._exec_stop = exec_stop
        return self

    def with_exec_stop_post(self, exec_stop_post: List[str]) -> 'ServiceBuilder':
        """
        Sets the `exec_stop_post` field of the `service` section of a systemd service file.

        :param exec_stop_post: The `exec_stop_post` field of the `service` section of a systemd service file
        :type exec_stop_post: List[str]

        :return: The `ServiceBuilder` object
        :rtype: ServiceBuilder
        """

        self._exec_stop_post = exec_stop_post
        return self

    def with_restart_sec(self, restart_sec: int) -> 'ServiceBuilder':
        """
        Sets the `restart_sec` field of the `service` section of a systemd service file.

        :param restart_sec: The `restart_sec` field of the `service` section of a systemd service file
        :type restart_sec: int

        :return: The `ServiceBuilder` object
        :rtype: ServiceBuilder
        """

        self._restart_sec = restart_sec
        return self

    def with_restart(self, restart: RestartType) -> 'ServiceBuilder':
        """
        Sets the `restart` field of the `service` section of a systemd service file.

        :param restart: The `restart` field of the `service` section of a systemd service file
        :type restart: RestartType

        :return: The `ServiceBuilder` object
        :rtype: ServiceBuilder
        """

        self._restart = restart
        return self

    def with_timeout_sec(self, timeout_sec: int) -> 'ServiceBuilder':
        """
        Sets the `timeout_sec` field of the `service` section of a systemd service file.

        :param timeout_sec: The `timeout_sec` field of the `service` section of a systemd service file
        :type timeout_sec: int

        :return: The `ServiceBuilder` object
        :rtype: ServiceBuilder
        """

        self._timeout_sec = timeout_sec
        return self

    def with_user(self, user: str) -> 'ServiceBuilder':
        """
        Sets the `user` field of the `service` section of a systemd service file.

        :param user: The `user` field of the `service` section of a systemd service file
        :type user: str

        :return: The `ServiceBuilder` object
        :rtype: ServiceBuilder
        """

        self._user = user
        return self

    def with_group(self, group: str) -> 'ServiceBuilder':
        """
        Sets the `group` field of the `service` section of a systemd service file.

        :param group: The `group` field of the `service` section of a systemd service file
        :type group: str

        :return: The `ServiceBuilder` object
        :rtype: ServiceBuilder
        """

        self._group = group
        return self

    def with_nice(self, nice: int) -> 'ServiceBuilder':
        """
        Sets the `nice` field of the `service` section of a systemd service file.

        :param nice: The `nice` field of the `service` section of a systemd service file
        :type nice: int

        :return: The `ServiceBuilder` object
        :rtype: ServiceBuilder
        """

        self._nice = nice
        return self
