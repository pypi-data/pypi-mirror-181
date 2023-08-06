"""
fredlock - Package Entry Point

(used when calling as `python -m fredlock`)

"""
import re
import sys

from fredlock.cli import cli

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
    sys.exit(cli())
