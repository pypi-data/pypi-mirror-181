from ._interactive import Interactive
from ..builders import InstallBuilder
from ..builders import ServiceBuilder
from ..builders import UnitBuilder
from ..main import Systemd
from ..utils.terminal.inputer import Inputer
from ..core.types import RestartType, TypeType


class SimpleBuilder(Interactive):
    def __init__(self):
        self._sysd = None

    @staticmethod
    def _get_name() -> str:
        _ = Inputer.input("Enter name: ")
        return _

    @staticmethod
    def _get_description() -> str:
        _ = Inputer.input("Enter description: ")
        return _

    @staticmethod
    def _get_user() -> str:
        _ = Inputer.input("Enter user: ", default="root")
        return _

    @staticmethod
    def _get_after() -> str:
        _ = Inputer.input("Enter after: ", default="network.target")
        return _

    @staticmethod
    def _get_type() -> TypeType:
        _ = Inputer.input(
            "Enter type: ", default="simple",
            choices=["simple", "forking", "oneshot", "dbus", "notify", "idle"],
            force=True
        )
        return _

    @staticmethod
    def _get_exec_start() -> str:
        _ = Inputer.input("Enter exec start: ")
        return _

    @staticmethod
    def _get_restart() -> RestartType:
        _ = Inputer.input(
            "Enter restart: ", default=Inputer.Empty,
            choices=["always", "on-failure", "on-abnormal", "on-watchdog", "on-abort", "no"],
            force=True
        )
        return _

    @staticmethod
    def _get_restart_sec() -> int:
        _ = Inputer.input_int("Enter restart sec: ", default=Inputer.Empty)
        return _

    @staticmethod
    def _get_wanted_by() -> str:
        _ = Inputer.input("Enter wanted by: ", default=Inputer.Empty)
        return _

    def create(self) -> None:
        name = self._get_name()
        description = self._get_description()
        exec_start = self._get_exec_start()
        user = self._get_user()
        after = self._get_after()
        type_ = self._get_type()
        restart = self._get_restart()
        restart_sec = self._get_restart_sec() if restart is not None else None
        wanted_by = self._get_wanted_by()

        unit = UnitBuilder().with_description(description).with_after([after]).build()
        service = ServiceBuilder().\
            with_type(type_).with_user(user).with_exec_start([exec_start]).\
            with_restart(restart).with_restart_sec(restart_sec).build()
        install = InstallBuilder().with_wanted_by([wanted_by]).build()

        self._sysd = Systemd(name, [unit, service, install])

        print(self._sysd)

    def ask_to_save(self):
        save = Inputer.input_bool("Save?", default=True)
        if save:
            from pathlib import Path
            print(f"Current path: {Path().resolve()}")
            path = Inputer.input("Enter path: ", default="/etc/systemd/system")
            path = Path(path).resolve()
            self._sysd.save(path)
        else:
            print("Not saved")
