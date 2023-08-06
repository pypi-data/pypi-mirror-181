"""
Main entry points for fredlock commands
"""
from fredlock.fredlock import FRedLock


def run(config):
    """ main run """
    app = FRedLock(config)
    return app.run()


def check(config):
    """ Check if the  """
    app = FRedLock(config)
    return app.check(locked="Locked", available="Available")
