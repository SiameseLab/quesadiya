#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
# import quesadiya as queso
# projectName = None


def main():
    """Run administrative tasks."""
    os.environ["projectName"] = "xxx"
    # global projectName
    # projectName = "xxxxxxx"
    # settings_path = os.path.join(queso.get_base_path(), 'django_tool', 'apps', 'settings.py')
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', "apps.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
