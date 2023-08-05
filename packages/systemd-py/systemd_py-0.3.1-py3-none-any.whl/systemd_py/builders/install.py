"""
# Install Builder 🏗️
Builder for the `install` section of a systemd service file.
"""

from typing import Optional
from typing import List
from typing import Union

from ._builder import _Builder
from ..core.models import Install


class InstallBuilder(_Builder):
    """
    Builder for the `install` section of a systemd service file.
    """

    __slots__ = (
        '_wanted_by',
        '_required_by',
        '_alias',
        '_also',
        '_default_instance',
    )

    @property
    def allowed_none_fields(self) -> List[str]:
        """
        Returns a list of fields that are allowed to be None


        :return: List of fields that are allowed to be None
        :rtype: List[str]
        """

        return [
            '_wanted_by', '_required_by', '_alias', '_also', '_default_instance'
        ]

    def build(self) -> Install:
        """
        Builds the `install` section of a systemd service file.

        :return: The `install` section of a systemd service file
        :rtype: Install
        """

        self._check()
        return Install(
            wanted_by=self._wanted_by,
            required_by=self._required_by,
            alias=self._alias,
            also=self._also,
            default_instance=self._default_instance
        )

    def __init__(self):
        self._wanted_by: Optional[List[str]] = None
        self._required_by: Optional[List[str]] = None
        self._alias: Optional[List[str]] = None
        self._also: Optional[List[str]] = None
        self._default_instance: Optional[str] = None

    def with_wanted_by(self, wanted_by: Union[str, List[str]]) -> 'InstallBuilder':
        """
        Sets the `wanted_by` field of the `install` section of a systemd service file.

        :param wanted_by: The `wanted_by` field of the `install` section of a systemd service file
        :type wanted_by: List[str]

        :return: The `InstallBuilder` object
        :rtype: InstallBuilder
        """

        self._wanted_by = wanted_by
        return self

    def with_required_by(self, required_by: Union[str, List[str]]) -> 'InstallBuilder':
        """
        Sets the `required_by` field of the `install` section of a systemd service file.

        :param required_by: The `required_by` field of the `install` section of a systemd service file
        :type required_by: List[str]

        :return: The `InstallBuilder` object
        :rtype: InstallBuilder
        """

        self._required_by = required_by
        return self

    def with_alias(self, alias: Union[str, List[str]]) -> 'InstallBuilder':
        """
        Sets the `alias` field of the `install` section of a systemd service file.

        :param alias: The `alias` field of the `install` section of a systemd service file
        :type alias: List[str]

        :return: The `InstallBuilder` object
        :rtype: InstallBuilder
        """

        self._alias = alias
        return self

    def with_also(self, also: Union[str, List[str]]) -> 'InstallBuilder':
        """
        Sets the `also` field of the `install` section of a systemd service file.

        :param also: The `also` field of the `install` section of a systemd service file
        :type also: List[str]

        :return: The `InstallBuilder` object
        :rtype: InstallBuilder
        """

        self._also = also
        return self

    def with_default_instance(self, default_instance: str) -> 'InstallBuilder':
        """
        Sets the `default_instance` field of the `install` section of a systemd service file.

        :param default_instance: The `default_instance` field of the `install` section of a systemd service file
        :type default_instance: str

        :return: The `InstallBuilder` object
        :rtype: InstallBuilder
        """

        self._default_instance = default_instance
        return self
