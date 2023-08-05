import typer
from cli.common.command_util import handle_request_command
from cli.common.crud_command_base import CRUDCommandBase
from cli.common.service_type import ServiceType

app = typer.Typer()


class PrincipalsCRUD(CRUDCommandBase):
    def __init__(
        self,
        service_type: ServiceType = ServiceType.USER_SERVICE,
        endpoint: str = "principals",
    ) -> None:
        super().__init__(service_type, endpoint)


@app.command("filter")
@handle_request_command
def list_(
    filters: str = typer.Argument(
        None,
        metavar="Filter: must contain part of name, surname, fullname, email or MS Active Directory object id",
    )
):
    typer.echo(PrincipalsCRUD().get_by_id({"filters": filters}))
