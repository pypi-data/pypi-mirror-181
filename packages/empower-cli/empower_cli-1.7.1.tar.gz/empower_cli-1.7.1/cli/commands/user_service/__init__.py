import typer
from cli.commands.user_service import principals, roles

user_service_typer = typer.Typer()

user_service_typer.add_typer(principals.app, name="principals")
user_service_typer.add_typer(roles.app, name="roles")
