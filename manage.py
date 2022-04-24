#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ledger_django.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    # When running in test mode, some flags need to be set
    if sys.argv[1:2] == ['test']:
        os.environ.setdefault('TESTING', 'True')

    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
