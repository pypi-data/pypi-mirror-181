"""
External Command Executor

Runs the Specified Command, pass stdout/stderr
"""
import logging
import subprocess

from .utils import keyboard_interrupt_protection

log = logging.getLogger(__name__)


def execute(*command):
    """ Execute a command with args, return exit code"""

    with keyboard_interrupt_protection():
        proc = None
        try:
            proc = subprocess.run(command)

        except Exception as ex:
            log.error("Got Exception: %s", ex)
        exitcode = proc.returncode if proc else -1
        if exitcode == 0:
            log.info("Command successfully completed")
        elif exitcode != -1:
            log.warning("Command exit status/return code: %s", exitcode)
        else:
            log.warning("Command failed to run")
        return exitcode
