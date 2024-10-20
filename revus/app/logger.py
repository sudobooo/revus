# app/logger.py

from rich.console import Console
from rich.traceback import install

install(show_locals=True)

console = Console(
    soft_wrap=True,
    highlight=True,
)


def log_warning(message: str):
    console.print(f"[bold yellow]{message}[/bold yellow]")


def log_error(message: str):
    console.print(f"[bold red]{message}[/bold red]")


def log_info(message: str):
    console.print(f"{message}")


def log_success(message: str):
    console.print(f"[bold green]{message}[/bold green]")
