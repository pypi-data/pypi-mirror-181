from typing import Optional
from typing import List
from typing import Union
from pydantic import Field

from ._models import Section


class Unit(Section):
    """
    Systemd [Unit] Section Directives
    """

    description: str = Field(
        None,
        title='Description',
        description='A short, one-line description of the service.'
    )
    documentation: Optional[str] = Field(
        None,
        title='Documentation',
        description='A space-separated list of URLs to documentation for this unit.'
    )
    requires: Optional[Union[str, List[str]]] = Field(
        None,
        title='Requires',
        description='A space-separated list of units that must be started before this unit.'
    )
    wants: Optional[Union[str, List[str]]] = Field(
        None,
        title='Wants',
        description='A space-separated list of units that should be started if this unit is.'
    )
    binds_to: Optional[Union[str, List[str]]] = Field(
        None,
        title='BindsTo',
        description='A space-separated list of units that this unit is bound to.'
    )
    before: Optional[Union[str, List[str]]] = Field(
        None,
        title='Before',
        description='A space-separated list of units that should be stopped if this unit is.'
    )
    after: Optional[Union[str, List[str]]] = Field(
        None,
        title='After',
        description='A space-separated list of units that must be stopped before this unit is.'
    )
    conflicts: Optional[Union[str, List[str]]] = Field(
        None,
        title='Conflicts',
        description='A space-separated list of units that this unit conflicts with.'
    )
    condition: Optional[str] = Field(
        None,
        title='Condition',
        description='A boolean expression that must be true for the unit to be started.'
    )
    assert_: Optional[str] = Field(
        None,
        title='Assert',
        description='A boolean expression that must be true for the unit to be started.'
    )

    class Config:
        fields = {
            'Description': 'description',
            'Documentation': 'documentation',
            'Requires': 'requires',
            'Wants': 'wants',
            'BindsTo': 'binds_to',
            'Before': 'before',
            'After': 'after',
            'Conflicts': 'conflicts',
            'Condition': 'condition',
            'Assert': 'assert_'
        }
