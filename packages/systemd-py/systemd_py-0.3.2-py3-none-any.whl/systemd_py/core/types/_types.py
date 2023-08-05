from typing import Union
from typing import Literal

from ..enums import Type
from ..enums import Restart


TypeType = Union[
    Type,
    Literal["simple"],
    Literal["forking"],
    Literal["oneshot"],
    Literal["dbus"],
    Literal["notify"],
    Literal["idle"]
]

RestartType = Union[
    Restart,
    Literal["no"],
    Literal["on_failure", "on-failure"],
    Literal["on_abnormal", "on-abnormal"],
    Literal["on_watchdog", "on-watchdog"],
    Literal["on_abort", "on-abort"],
]
