from pathlib import Path
from json import dumps
from typing import Optional, Dict, Any

import typer

from wargames import (
    ERRORS,
    __app_name__,
    __version__,
    config,
    database,
    wargames
)
from wargames.formatting import pprint

app = typer.Typer()

# =========================
#          Commands
# =========================

@app.command()
def init(
        db_path: str = typer.Option(
            str(database.DEFAULT_DB_PATH),
            "--db-path",
            "-db",
            prompt="wargames passwords database location"
        ),
) -> None:
    app_init_error = config.init_app(db_path)
    if app_init_error:
        typer.secho(
            f"Creating config file failed with {ERRORS[app_init_error]}",
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    db_init_error = database.init_database(Path(db_path))
    if db_init_error:
        typer.secho(
            f"Creating wargames passwords database failed with {ERRORS[db_init_error]}",
            fg=typer.colors.RED,
        )
    else:
        typer.secho(
            f"The wargames passwords database is {db_path}",
            fg=typer.colors.GREEN
        )

        
@app.command()
def list() -> Dict[str, Any]:
    controller = get_controller()
    data, error = controller.read()
    if error:
        typer.secho(
            f'Reading level info failed with "{ERRORS[error]}"',
            fg=typer.colors.RED
        )
        raise typer.Exit(1)
    else:
        pprint(data)
        return data
        
        
@app.command()
def add(level: str = typer.Argument(...),
        passwd: str = typer.Argument(...),
        description: str = typer.Option("", "--description", "-d"),
    ) -> None:
    controller = get_controller()
    level_info, error = controller.add({"level": level, "description": description, "passwd": passwd})
    if error:
        typer.secho(
            f'Adding level info failed with "{ERRORS[error]}"',
            fg=typer.colors.RED
        )
        raise typer.Exit(1)
    else:
        typer.secho(
            f"Info for level {level_info['level']} was added",
            fg=typer.colors.GREEN,
        )


# =========================
#          Functions
# =========================
def get_controller() -> wargames.WargamesController:
    if config.CONFIG_FILE_PATH.exists():
        db_path = database.get_database_path(config.CONFIG_FILE_PATH)
    else:
        typer.secho(
            "Config file not found. Please run 'wargames init'",
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    if db_path.exists():
        return wargames.WargamesController(db_path)
    else:
        typer.secho(
            "Database not found. Please run 'wargames init'",
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()
    

# =========================
#          Main
# =========================


@app.callback()
def main(
        version: Optional[bool] = typer.Option(
            None,
            "--version",
            "-v",
            help="Show the app's version and exit.",
            callback=_version_callback,
            is_eager=True,
        )
) -> None:
    return
    