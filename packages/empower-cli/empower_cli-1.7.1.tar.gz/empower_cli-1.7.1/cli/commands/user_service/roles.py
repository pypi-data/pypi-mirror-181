import json
from enum import Enum
from typing import Optional

import typer
from cli.common.command_help import CRUD_FILE_PATH_HELP
from cli.common.command_util import handle_request_command
from cli.common.crud_command_base import CRUDCommandBase
from cli.common.enums import RequestMethods
from cli.common.service_type import ServiceType
from cli.common.util import get_json_data, get_request_url

app = typer.Typer()


class UserServiceObjectTypes(str, Enum):
    USERS = "users"
    GROUPS = "groups"


class RolesCRUD(CRUDCommandBase):
    def __init__(
        self,
        service_type: ServiceType = ServiceType.USER_SERVICE,
        endpoint: str = "roles",
    ) -> None:
        super().__init__(service_type, endpoint)

    def patch(self, role_id_: str, object_type: str, data: Optional[str] = None) -> str:
        self._guard_input(data)
        url: str = (
            f"{get_request_url(self.service_type)}/{self.endpoint}/"
            f"{role_id_}/{object_type}"
        )
        json_data = self._convert_to_j_object_list(data)

        created = [
            self._make_request(RequestMethods.PATCH, url, data=json.dumps(item)).json()
            for item in json_data
        ]
        return json.dumps(created, indent=2)

    def get_objects_by_role_id(self, role_id_: str, filters: str, object_type: str) -> str:
        url = f"{self.default_url(self.endpoint)}/{role_id_}/{object_type}"

        if filters:
            url = f"{url}?filters={filters}"

        response = self._make_request(RequestMethods.GET, url)
        typer.echo(f"request made to: {url}")

        return json.dumps(response.json(), indent=2)


@app.command("list")
@handle_request_command
def list_():
    typer.echo(RolesCRUD().get())


@app.command("users")
@handle_request_command
def show_users(
        role_id_: str = typer.Argument(..., metavar="Role ID"),
        filters: str = typer.Argument(None, metavar="Filter: must contain part of fullname, email or id")
):
    typer.echo(
        RolesCRUD().get_objects_by_role_id(role_id_, filters, UserServiceObjectTypes.USERS)
    )


@app.command("groups")
@handle_request_command
def show_groups(
        role_id_: str = typer.Argument(..., metavar="Role ID"),
        filters: str = typer.Argument(None, metavar="Filter: must contain part of name or id")
):
    typer.echo(
        RolesCRUD().get_objects_by_role_id(role_id_, filters, UserServiceObjectTypes.GROUPS)
    )


@app.command("update-users")
@handle_request_command
def update_users(
    role_id_: str = typer.Argument(..., metavar="Role ID"),
    json_: Optional[str] = typer.Option(None, "--json"),
    file_path: Optional[typer.FileText] = typer.Option(
        None,
        mode="r",
        encoding="utf-8",
        callback=get_json_data,
        help=CRUD_FILE_PATH_HELP,
    ),
):
    typer.echo(
        RolesCRUD().patch(role_id_, UserServiceObjectTypes.USERS, json_ or file_path)
    )


@app.command("update-groups")
@handle_request_command
def update_groups(
    role_id_: str = typer.Argument(..., metavar="Role ID"),
    json_: Optional[str] = typer.Option(None, "--json"),
    file_path: Optional[typer.FileText] = typer.Option(
        None,
        mode="r",
        encoding="utf-8",
        callback=get_json_data,
        help=CRUD_FILE_PATH_HELP,
    ),
):
    typer.echo(
        RolesCRUD().patch(role_id_, UserServiceObjectTypes.GROUPS, json_ or file_path)
    )
