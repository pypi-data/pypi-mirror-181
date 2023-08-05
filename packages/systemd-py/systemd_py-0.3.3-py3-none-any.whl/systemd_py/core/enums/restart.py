from typing import Literal

from ._enums import _Enum


class Restart(_Enum):
    """
    Service Restart
    """

    no: Literal['no'] = 'no'
    on_failure: Literal['on-failure'] = 'on-failure'
    on_abnormal: Literal['on-abnormal'] = 'on-abnormal'
    on_watchdog: Literal['on-watchdog'] = 'on-watchdog'
    on_abort: Literal['on-abort'] = 'on-abort'
