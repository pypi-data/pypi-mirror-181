from typer import Typer
from ...interactive.simple_builder import SimpleBuilder

app = Typer(
    name="interactive",
    help="Systemd-py Interactive Commands",
)


@app.command()
def simple_builder():
    """
    Run the simple systemd builder interactive interface
    """

    return SimpleBuilder().run()
