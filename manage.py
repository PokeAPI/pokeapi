#!/usr/bin/env python
import os
import sys

# Added 4/4/21 - Ryan OConnor - to commit changes to forked project

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
