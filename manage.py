#!/usr/bin/env python
import os
import sys


def main():
    """Encaminha os comandos do terminal para o sistema de gerenciamento do Django."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "inventario.settings")
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
