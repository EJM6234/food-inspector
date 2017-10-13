#!/usr/bin/env python
import os
import sys

from eatsmart import load_env

if __name__ == "__main__":
    load_env.load_env()

    # Default to the safest settings
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "eatsmart.settings.deploy")
    print(os.environ['DJANGO_SETTINGS_MODULE'])

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
