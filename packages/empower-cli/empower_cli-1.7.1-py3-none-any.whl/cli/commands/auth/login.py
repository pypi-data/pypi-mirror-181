import requests
import typer
from cli.common.auth import BrowserAuthManager, credentials_flow_auth
from cli.common.service_type import ServiceType
from cli.common.validation import validate_domain
from typer import Argument

app = typer.Typer()
ENDPOINT = "auth"
SERVICE_TYPE = ServiceType.EMPOWER_AUTH


@app.command(help="Login user within an opened browser tab.")
def login(domain: str = Argument(..., callback=validate_domain)) -> None:
    login_manager = BrowserAuthManager(domain)
    typer.echo("Processing login. Wait for the browser window to open.")

    try:
        login_manager.browser_auth()
    except RuntimeError as e:
        typer.echo(e)
    except Exception as e:
        typer.echo(f"Authentication error: {e}")
    else:
        login_manager.store_enterprise()
        typer.echo("Logged in successfully.")


@app.command(help="Pipeline authentication using 'client_credentials' flow.")
def login_pipeline() -> None:
    typer.echo("Processing login.")
    try:
        credentials_flow_auth()
    except requests.HTTPError:
        typer.echo("Error occurred while getting authentication credentials.")
        typer.Abort(1)
    else:
        typer.echo("Logged in successfully.")
