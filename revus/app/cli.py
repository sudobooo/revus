# app/cli.py

import xml.etree.ElementTree as ET
from .logger import log_warning, console


def get_user_choice():
    choices = {"r": "re-review file", "c": "continue", "q": "quit"}
    while True:
        choice = console.input(
            "[bold blue]Choose an action: (r) re-review file, (c) continue, (q) quit: [/bold blue]"
        ).lower()
        if choice in choices:
            return choice
        else:
            log_warning("Invalid input. Please enter 'r', 'c', or 'q'.")


def format_review_output(review):
    root = ET.fromstring(f"<root>{review}</root>")
    output = []

    for idx, item in enumerate(root.findall("review_item"), start=1):
        code_section = (
            item.find("code_section").text.strip()
            if item.find("code_section") is not None
            else ""
        )
        comment = (
            item.find("comment").text.strip()
            if item.find("comment") is not None
            else ""
        )
        priority = (
            item.find("priority").text.strip()
            if item.find("priority") is not None
            else ""
        )
        output.extend(
            [
                f"[bold bright_cyan]CODE SECTION {idx}:[/bold bright_cyan]",
                f"{code_section}\n",
                "[bold]COMMENT:[/bold]",
                f"{comment}\n",
                "[bold]PRIORITY:[/bold]",
                f"{priority}\n[indian_red]{'_' * 15}[/indian_red]",
            ]
        )

    review_summary = (
        root.find("review_summary").text.strip()
        if root.find("review_summary") is not None
        else ""
    )
    output.append("[bold spring_green3]REVIEW SUMMARY:[/bold spring_green3]")
    output.append(review_summary)

    return "\n".join(output)
