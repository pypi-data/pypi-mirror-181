import os
from pathlib import Path
from typing import Optional

import typer
from cli.common.store_client import store
from dotenv import load_dotenv

app = typer.Typer()


@app.command()
def show():
    typer.echo(store.dump())


@app.command("set")
def set_(
    discovery_url: str = typer.Option(
        None, help="Url for the empower discovery service."
    ),
    env_path: Optional[Path] = typer.Option(
        None,
        help="Relative or full path to optional .env file with context values.",
        resolve_path=True,
        exists=True,
    ),
):
    if discovery_url is None and env_path is None:
        typer.echo("Either discovery_url or env_path should be provided.")
        typer.Abort(1)

    if env_path is not None:
        load_dotenv(dotenv_path=env_path)
        empower_discovery_url: str = os.environ.get("DISCOVERY_URL")
        store.empower_discovery_url = empower_discovery_url
    else:
        store.empower_discovery_url = discovery_url
