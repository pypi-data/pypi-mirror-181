"""
# Unit Builder 🏗️
Builder for the `uni` section of a systemd service file.
"""

from typing import Optional
from typing import List

from ._builder import _Builder
from ..core.models import Unit


class UnitBuilder(_Builder):
    """
    Builder for the `unit` section of a systemd service file.
    """

    __slots__ = (
        "_description",
        "_documentation",
        "_requires",
        "_wants",
        "_binds_to",
        "_before",
        "_after",
        "_conflicts",
        "_condition",
        "_assert_",
    )

    @property
    def allowed_none_fields(self) -> List[str]:
        """
        Returns a list of fields that are allowed to be None


        :return: List of fields that are allowed to be None
        :rtype: List[str]
        """

        return [
            "_documentation", "_requires", "_wants", "_binds_to", "_before",
            "_after", "_conflicts", "_condition", "_assert_",
        ]

    def build(self) -> Unit:
        """
        Builds the `unit` section of a systemd service file.

        :return: The `unit` section of a systemd service file
        :rtype: Unit
        """

        self._check()
        return Unit(
            description=self._description,
            documentation=self._documentation,
            requires=self._requires,
            wants=self._wants,
            binds_to=self._binds_to,
            before=self._before,
            after=self._after,
            conflicts=self._conflicts,
            condition=self._condition,
            assert_=self._assert_,
        )

    def __init__(self):
        self._description: str = ...
        self._documentation: Optional[str] = ...
        self._requires: Optional[List[str]] = ...
        self._wants: Optional[List[str]] = ...
        self._binds_to: Optional[List[str]] = ...
        self._before: Optional[List[str]] = ...
        self._after: Optional[List[str]] = ...
        self._conflicts: Optional[List[str]] = ...
        self._condition: Optional[str] = ...
        self._assert_: Optional[str] = ...

    def with_description(self, description: str) -> 'UnitBuilder':
        """
        Sets the `description` field of the `unit` section of a systemd service file.

        :param description: The `description` field of the `unit` section of a systemd service file
        :type description: str

        :return: The `unit` section of a systemd service file
        :rtype: Unit

        :return: The SocketBuilder object
        :rtype: SocketBuilder
        """

        self._description = description
        return self

    def with_documentation(self, documentation: str) -> 'UnitBuilder':
        """
        Sets the `documentation` field of the `unit` section of a systemd service file.

        :param documentation: The `documentation` field of the `unit` section of a systemd service file
        :type documentation: str

        :return: The `unit` section of a systemd service file
        :rtype: Unit
        """

        self._documentation = documentation
        return self

    def with_requires(self, requires: List[str]) -> 'UnitBuilder':
        """
        Sets the `requires` field of the `unit` section of a systemd service file.

        :param requires: The `requires` field of the `unit` section of a systemd service file
        :type requires: List[str]

        :return: The `unit` section of a systemd service file
        :rtype: Unit
        """

        self._requires = requires
        return self

    def with_wants(self, wants: List[str]) -> 'UnitBuilder':
        """
        Sets the `wants` field of the `unit` section of a systemd service file.

        :param wants: The `wants` field of the `unit` section of a systemd service file
        :type wants: List[str]

        :return: The `unit` section of a systemd service file
        :rtype: Unit
        """

        self._wants = wants
        return self

    def with_binds_to(self, binds_to: List[str]) -> 'UnitBuilder':
        """
        Sets the `binds_to` field of the `unit` section of a systemd service file.

        :param binds_to: The `binds_to` field of the `unit` section of a systemd service file
        :type binds_to: List[str]

        :return: The `unit` section of a systemd service file
        :rtype: Unit
        """

        self._binds_to = binds_to
        return self

    def with_before(self, before: List[str]) -> 'UnitBuilder':
        """
        Sets the `before` field of the `unit` section of a systemd service file.

        :param before: The `before` field of the `unit` section of a systemd service file
        :type before: List[str]

        :return: The `unit` section of a systemd service file
        :rtype: Unit
        """

        self._before = before
        return self

    def with_after(self, after: List[str]) -> 'UnitBuilder':
        """
        Sets the `after` field of the `unit` section of a systemd service file.

        :param after: The `after` field of the `unit` section of a systemd service file
        :type after: List[str]

        :return: The `unit` section of a systemd service file
        :rtype: Unit
        """

        self._after = after
        return self

    def with_conflicts(self, conflicts: List[str]) -> 'UnitBuilder':
        """
        Sets the `conflicts` field of the `unit` section of a systemd service file.

        :param conflicts: The `conflicts` field of the `unit` section of a systemd service file
        :type conflicts: List[str]

        :return: The `unit` section of a systemd service file
        :rtype: Unit
        """

        self._conflicts = conflicts
        return self

    def with_condition(self, condition: str) -> 'UnitBuilder':
        """
        Sets the `condition` field of the `unit` section of a systemd service file.

        :param condition: The `condition` field of the `unit` section of a systemd service file
        :type condition: str

        :return: The `unit` section of a systemd service file
        :rtype: Unit
        """

        self._condition = condition
        return self

    def with_assert(self, assert_: str) -> 'UnitBuilder':
        """
        Sets the `assert` field of the `unit` section of a systemd service file.

        :param assert_: The `assert` field of the `unit` section of a systemd service file
        :type assert_: str

        :return: The `unit` section of a systemd service file
        :rtype: Unit
        """

        self._assert_ = assert_
        return self
