from typing import Optional
from typing import List
from typing import Union
from pydantic import Field

from ._models import Section


class Install(Section):
    """
    Systemd [Install] Section Directives
    """

    wanted_by: Optional[Union[str, List[str]]] = Field(
        None,
        title='WantedBy',
        description='A space-separated list of units that should be started when this unit is.',
    )
    required_by: Optional[Union[str, List[str]]] = Field(
        None,
        title='RequiredBy',
        description='A space-separated list of units that must be started when this unit is.'
    )
    alias: Optional[Union[str, List[str]]] = Field(
        None,
        title='Alias',
        description='A space-separated list of additional names for this unit.'
    )
    also: Optional[Union[str, List[str]]] = Field(
        None,
        title='Also',
        description='A space-separated list of units that should be installed when this unit is.'
    )
    default_instance: Optional[str] = Field(
        None,
        title='DefaultInstance',
        description='The default instance name for this template unit.'
    )

    class Config:
        fields = {
            'WantedBy': 'wanted_by',
            'RequiredBy': 'required_by',
            'Alias': 'alias',
            'Also': 'also',
            'DefaultInstance': 'default_instance'
        }
