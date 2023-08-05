import typer
from cli.commands import context
from cli.commands.auth import login
from cli.commands.config_promotion import config_promotion_typer
from cli.commands.empower_api import empower_api_typer
from cli.commands.empower_discovery import discovery_typer
from cli.commands.user_service import user_service_typer

app = typer.Typer()
app.add_typer(context.app, name="context")
app.add_typer(login.app, name="auth")
app.add_typer(discovery_typer, name="discovery")
app.add_typer(empower_api_typer, name="api")
app.add_typer(config_promotion_typer, name="config-promotion")
app.add_typer(user_service_typer, name="user-service")


if __name__ == "__main__":
    app()
