from typing import Literal

from ._enums import _Enum


class Type(_Enum):
    """
    Service Type
    """

    simple: Literal['simple'] = 'simple'
    forking: Literal['forking'] = 'forking'
    oneshot: Literal['oneshot'] = 'oneshot'
    dbus: Literal['dbus'] = 'dbus'
    notify: Literal['notify'] = 'notify'
    idle: Literal['idle'] = 'idle'
