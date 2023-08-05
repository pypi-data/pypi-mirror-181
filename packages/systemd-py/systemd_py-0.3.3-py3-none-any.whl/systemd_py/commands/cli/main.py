from typer import Typer
from typer import Argument
from typer import Option

from ...builders import InstallBuilder
from ...builders import ServiceBuilder
from ...builders import UnitBuilder
from ...main import Systemd
from ...core.enums import Type, Restart

app = Typer(
    name="cli",
    help="Systemd-py CLI Builder",
)


@app.command()
def generate(
        name: str = Argument(
            ..., help="Service Name", metavar="NAME"),
        description: str = Argument(
            ..., help="Service Description", metavar="DESCRIPTION"),
        exec_start: str = Argument(
            ..., help="Service Exec Start", metavar="EXEC_START"),
        user: str = Option(
            None, help="Service User", metavar="USER"),
        after: str = Option(
            None, help="Service After", metavar="AFTER"),
        type: Type = Option(
            None, help="Service Type", metavar="TYPE"),
        restart: Restart = Option(
            None, help="Service Restart", metavar="RESTART"),
        restart_sec: int = Option(
            None, help="Service Restart Sec", metavar="RESTART_SEC"),
        wanted_by: str = Option(
            None, help="Service Wanted By", metavar="WANTED_BY"),
        save: bool = Option(
            False, help="Save Service", metavar="SAVE"),
        reload: bool = Option(
            False, help="Reload systemd daemon", metavar="RELOAD"),
        enable: bool = Option(
            False, help="Enable systemd service", metavar="ENABLE"),
        start: bool = Option(
            False, help="Start systemd service", metavar="START"),
) -> None:
    unit = UnitBuilder().with_description(description).with_after([after]).build()
    service = ServiceBuilder(). \
        with_type(type).with_user(user).with_exec_start([exec_start]). \
        with_restart(restart).with_restart_sec(restart_sec).build()
    install = InstallBuilder().with_wanted_by([wanted_by]).build()

    sysd = Systemd(name, [unit, service, install])

    print(f"\n\n{sysd}\n\n")

    if save:
        sysd.save_in_os()
        if reload:
            sysd.daemon.reload()

        if enable:
            sysd.daemon.enable()

        if start:
            sysd.daemon.start()
