import typer
import ujson
from rich import print, print_json
from rich.table import Column, Table

from pyxrayc import __version__
from pyxrayc.enums import SupportedProtocol
from pyxrayc.utils import (
    create_user,
    get_user,
    get_users,
    load_config,
    restart_xray,
    rollback,
    save_backup,
    save_config,
    validate_email,
)

state = {
    "apply": False,
}
app = typer.Typer(name="PyXrayC", help="Xray VPN user management made easy!")


def version_callback(value: bool) -> None:
    if value:
        print(f"[bold cyan]PyXrayC version[/]: [red]{__version__}[/]")
        raise typer.Exit()


def email_callback(value: str) -> str:
    if not validate_email(value):
        raise typer.BadParameter(repr(value))
    return value


@app.callback()
def main(
    version: bool = typer.Option(  # noqa
        None,
        "--version",
        callback=version_callback,
        is_eager=True,
        help="Show the PyXrayC version number.",
    ),
    apply: bool = typer.Option(
        False,
        help="Apply the changes by restarting Xray.",
    ),
) -> None:
    if apply:
        state["apply"] = True


@app.command()
def list(
    proto: SupportedProtocol = typer.Option(
        SupportedProtocol.VLESS,
        help="The protocol to list users for.",
    ),
    port: int = typer.Option(
        1080,
        help="The port to list users for.",
    ),
) -> None:
    """List users for a given protocol and port."""
    users = get_users(load_config(), proto, port)
    if not users:
        print("[bold red]No users found.[/]")
        raise typer.Exit()

    table = Table(
        Column("ID", justify="center", style="green", no_wrap=True),
        Column("Flow", justify="center", style="yellow"),
        Column("Level", justify="center", style="bold white"),
        Column("Email", justify="center", style="bold white"),
        Column("Created At", justify="center", style="cyan"),
        title=(
            f"Users found for [bold red]{proto.upper()}[/] on port [bold red]{port}[/]"
        ),
        show_header=True,
        header_style="bold magenta",
        show_lines=True,
    )
    for user in users:
        table.add_row(*(str(v) for v in user.values()))
    print(table)


@app.command()
def add(
    email: str = typer.Argument(
        ...,
        callback=email_callback,
        help="The email address of the user to add.",
    ),
    proto: SupportedProtocol = typer.Option(
        SupportedProtocol.VLESS,
        help="The protocol to add the user to.",
    ),
    port: int = typer.Option(
        1080,
        help="The port to add the user to.",
    ),
) -> None:
    """Add a user to the given protocol and port."""
    config = load_config()
    users = get_users(config, proto, port)
    if user := get_user(email, users):
        print(f"[bold red]User {email} already exists.[/]")
        print_json(ujson.dumps(user), indent=4)
        raise typer.Exit()
    else:
        user = create_user(email)

    save_backup()

    for inbound in config["inbounds"]:
        if inbound["port"] == port and inbound["protocol"] == proto.value:
            inbound["settings"]["clients"].append(user)
            break

    save_config(config)

    print(f"[bold green]Successfully added user {email}[/]")
    print_json(ujson.dumps(user), indent=4)

    if state["apply"]:
        restart_xray()


@app.command()
def remove(
    email: str = typer.Argument(
        ...,
        callback=email_callback,
        help="The email address of the user to remove.",
    ),
    proto: SupportedProtocol = typer.Option(
        SupportedProtocol.VLESS,
        help="The protocol to remove the user from.",
    ),
    port: int = typer.Option(
        1080,
        help="The port to remove the user from.",
    ),
) -> None:
    """Remove a user from the given protocol and port."""
    config = load_config()
    users = get_users(config, proto, port)
    if not (user := get_user(email, users)):
        print(f"[bold red]User {email} not found.[/]")
        raise typer.Exit()

    save_backup()

    for inbound in config["inbounds"]:
        if inbound["port"] == port and inbound["protocol"] == proto.value:
            inbound["settings"]["clients"].remove(user)
            break

    save_config(config)

    print(f"[bold green]Successfully removed user {email}[/]")
    print_json(ujson.dumps(user), indent=4)

    if state["apply"]:
        restart_xray()


@app.command()
def apply() -> None:
    """Apply the changes by restarting Xray."""
    restart_xray()


@app.command("rollback")
def rollback_changes() -> None:
    """Rollback the last changes made."""
    rollback()
    print("[bold green]Successfully rolled back.[/]")

    if state["apply"]:
        restart_xray()
