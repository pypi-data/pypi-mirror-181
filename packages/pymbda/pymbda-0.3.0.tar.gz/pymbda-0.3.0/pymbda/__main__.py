import sys

from .commands import resolve_command
from .templates import USAGE_TEXT
from .utils import pymbda_print


def main():
    if len(sys.argv[1:]) < 2:
        print(USAGE_TEXT)
        sys.exit(1)
    resource, command = sys.argv[1:3]
    try:
        command_callable = resolve_command(resource, command)
    except ValueError:
        print(USAGE_TEXT)
        sys.exit(1)
    pymbda_print(" ".join(sys.argv[1:]))
    try:
        command_callable(sys.argv[3:])
    except KeyboardInterrupt:
        print()
        pymbda_print("Operation canceled")
    except Exception as e:
        pymbda_print("Operation aborted:", e)
    sys.exit(0)


if __name__ == "__main__":
    main()
