#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

import pyfiglet


def print_banner():
    text = "Payroll System"
    figlet_text = pyfiglet.figlet_format(text)
    print(figlet_text)  # noqa: T201


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "runserver" and os.environ.get("RUN_MAIN") != "true":
        print_banner()
    main()
