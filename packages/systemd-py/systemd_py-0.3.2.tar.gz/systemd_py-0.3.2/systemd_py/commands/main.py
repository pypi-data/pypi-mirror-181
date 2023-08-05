from typer import Typer

from .interactive.main import app as interactive_app
from .cli.main import app as cli_app

app = Typer(
    name="systemd-py",
    help="Systemd-py Commands",
)

app.add_typer(interactive_app, name="interactive")
app.add_typer(cli_app, name="cli")

if __name__ == "__main__":
    app()
