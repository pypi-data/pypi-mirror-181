from typing import Optional

import typer
from cli.common.command_help import CRUD_FILE_PATH_HELP
from cli.common.command_util import handle_request_command
from cli.common.crud_command_base import CRUDCommandBase
from cli.common.enums import RequestMethods
from cli.common.service_type import ServiceType
from cli.common.util import get_json_data

app = typer.Typer()


class ConfigPromotionCRUD(CRUDCommandBase):
    def __init__(
        self,
        service_type: ServiceType = ServiceType.EMPOWER_DISCOVERY,
        endpoint: str = "config-promotion",
    ) -> None:
        super().__init__(service_type, endpoint)


@app.command(
    short_help="Configure current environment settings for Azure DevOps integration."
)
@handle_request_command
def configure_ado(
    json_: Optional[str] = typer.Option(None, "--json"),
    file_path: Optional[typer.FileText] = typer.Option(
        None,
        mode="r",
        encoding="utf-8",
        callback=get_json_data,
        help=CRUD_FILE_PATH_HELP,
    ),
):
    ConfigPromotionCRUD().create(
        json_ or file_path, endpoint="config-promotion/configure-azure-devops"
    )
    typer.echo("Azure DevOps integrations settings applied.")


@app.command(short_help="Configure current environment settings for GitHub integration.")
@handle_request_command
def configure_git(
    json_: Optional[str] = typer.Option(None, "--json"),
    file_path: Optional[typer.FileText] = typer.Option(
        None,
        mode="r",
        encoding="utf-8",
        callback=get_json_data,
        help=CRUD_FILE_PATH_HELP,
    ),
):
    ConfigPromotionCRUD().create(
        json_ or file_path, endpoint="config-promotion/configure-git"
    )
    typer.echo("GitHub integration settings applied.")


@app.command(
    short_help=(
        "Create branches for each environment "
        "using 'dv' environment branch as HEAD (parent)."
    )
)
@handle_request_command
def init():
    ConfigPromotionCRUD()._make_request(
        RequestMethods.POST,
        "config-promotion/init-environments",
    )
    typer.echo("Environments initialized.")


@app.command(
    short_help="Dump promotable entities data from database to configured repository."
)
@handle_request_command
def dump(
    json_: Optional[str] = typer.Option(None, "--json"),
    file_path: Optional[typer.FileText] = typer.Option(
        None,
        mode="r",
        encoding="utf-8",
        callback=get_json_data,
        help=CRUD_FILE_PATH_HELP,
    ),
):
    ConfigPromotionCRUD().create(
        json_ or file_path,
        endpoint="config-promotion/dump",
    )
    typer.echo("Source environment data has been dumped.")


@app.command(
    short_help="Start promoting all promotable entities (creates PR in repository)."
)
@handle_request_command
def run(
    json_: Optional[str] = typer.Option(None, "--json"),
    file_path: Optional[typer.FileText] = typer.Option(
        None,
        mode="r",
        encoding="utf-8",
        callback=get_json_data,
        help=CRUD_FILE_PATH_HELP,
    ),
):
    ConfigPromotionCRUD().create(json_ or file_path)
    typer.echo("Configuration promotion started.")


@app.command(
    short_help=(
        "Complete promoting all promotable entities and apply all "
        "promoted to target environment (completes PR in repository)."
    )
)
@handle_request_command
def complete():
    ConfigPromotionCRUD()._make_request(RequestMethods.PUT, url="config-promotion")
    typer.echo("Configuration promotion completed.")
