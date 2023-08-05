from typing import Optional
from typing import List
from typing import Union
from pydantic import Field

from ._models import Section
from ..types import TypeType, RestartType


class Service(Section):
    """
    Systemd [Service] Section Directives
    """

    type: Optional[TypeType] = Field(
        None,
        title="Type",
        description="The type of service to start. One of simple, forking, oneshot, dbus, notify, idle, or "
                    "exec. If this option is not specified, simple is assumed."
    )
    remain_after_exit: Optional[bool] = Field(
        None,
        title="RemainAfterExit",
        description="This directive is commonly used with the oneshot type. It indicates that "
                    "the service should be considered active even after the process exits."
    )
    pid_file: Optional[str] = Field(
        None,
        title="PIDFile",
        description="If the service type is marked as “forking”, this directive is used to set the "
                    "path of the file that should contain the process ID number of the main child "
                    "that should be monitored."
    )
    bus_name: Optional[str] = Field(
        None,
        title="BusName",
        description="This directive should be set to the D-Bus bus name that the service will attempt "
                    "to acquire when using the “dbus” service type."
    )
    notify_access: Optional[str] = Field(
        None,
        title="NotifyAccess",
        description='This specifies access to the socket that should be used to listen for notifications '
                    'when the “notify” service type is selected This can be “none”, “main”, or "all. '
                    'The default, “none”, ignores all status messages. The “main” option will listen to '
                    'messages from the main process and the “all” option will cause all members of '
                    'the service’s control group to be processed.'
    )
    exec_start: Optional[Union[str, List[str]]] = Field(
        None,
        title="ExecStart",
        description="This specifies the full path and the arguments of the command to be executed to "
                    "start the process. This may only be specified once (except for “oneshot” services). "
                    "If the path to the command is preceded by a dash “-” character, non-zero exit "
                    "statuses will be accepted without marking the unit activation as failed."
    )
    exec_start_pre: Optional[Union[str, List[str]]] = Field(
        None,
        title="ExecStartPre",
        description="This can be used to provide additional commands that should be executed before "
                    "the main process is started. This can be used multiple times. Again, "
                    "commands must specify a full path and they can be preceded by “-” to indicate that "
                    "the failure of the command will be tolerated."
    )
    exec_start_post: Optional[Union[str, List[str]]] = Field(
        None,
        title="ExecStartPost",
        description="This has the same exact qualities as `ExecStartPre=` except that it specifies "
                    "commands that will be run after the main process is started."
    )
    exec_reload: Optional[Union[str, List[str]]] = Field(
        None,
        title="ExecReload",
        description="This optional directive indicates the command necessary to reload the "
                    "configuration of the service if available"
    )
    exec_stop: Optional[Union[str, List[str]]] = Field(
        None,
        title="ExecStop",
        description="This indicates the command needed to stop the service. If this is not given, "
                    "the process will be killed immediately when the service is stopped."
    )
    exec_stop_post: Optional[Union[str, List[str]]] = Field(
        None,
        title="ExecStopPost",
        description="This can be used to specify commands to execute following the stop command"
    )
    restart_sec: Optional[int] = Field(
        None,
        title='RestartSec',
        description='If automatically restarting the service is enabled, this specifies the amount of time to '
                    'wait before attempting to restart the service.'
    )
    restart: Optional[RestartType] = Field(
        None,
        title='Restart',
        description='This indicates the circumstances under which systemd will attempt to automatically restart the '
                    'service. This can be set to values like “always”, “on-success”, “on-failure”, “on-abnormal”, '
                    '“on-abort”, or “on-watchdog”. These will trigger a restart according to the way that the service '
                    'was stopped.'
    )
    timeout_sec: Optional[int] = Field(
        None,
        title='TimeoutSec',
        description='This configures the amount of time that systemd will wait when stopping or stopping the service '
                    'before marking it as failed or forcefully killing it. You can set separate timeouts with '
                    'TimeoutStartSec= and TimeoutStopSec= as well.'
    )
    user: Optional[str] = Field(
        None,
        title='User',
        description='This specifies the user that the service should be run as. This can be a user name or a numeric '
                    'UID. If this is not specified, the service will be run as root.'
    )
    group: Optional[str] = Field(
        None,
        title='Group',
        description='This specifies the group that the service should be run as. This can be a group name or a numeric '
                    'GID. If this is not specified, the service will be run as root.'
    )
    nice: Optional[int] = Field(
        None,
        title='Nice',
        description='This specifies the nice level of the service. This can be a value between -20 and 19. '
                    'The default is 0.'
    )

    class Config:
        fields = {
            'remain_after_exit': 'RemainAfterExit',
            'pid_file': 'PIDFile',
            'bus_name': 'BusName',
            'notify_access': 'NotifyAccess',
            'exec_start': 'ExecStart',
            'exec_start_pre': 'ExecStartPre',
            'exec_start_post': 'ExecStartPost',
            'exec_reload': 'ExecReload',
            'exec_stop': 'ExecStop',
            'exec_stop_post': 'ExecStopPost',
            'restart_sec': 'RestartSec',
            'timeout_sec': 'TimeoutSec',
            'user': 'User',
            'group': 'Group',
            'nice': 'Nice',
        }
