"""
CLI Argument Parser

This uses click project that supports both command line args in addition
to env variables

"""
import logging
import sys
from dataclasses import asdict

import click
import yaml

from . import main
from .fredlock import Config

pass_config = click.make_pass_decorator(Config, ensure=True)

opt_args = dict(show_envvar=True)
FORMAT_LEVEL = "%(module)s:%(levelname)1.1s: %(message)s"
FORMAT = "%(module)s: %(message)s"

root_logger = logging.getLogger()
pkg_logger = logging.getLogger('fredlock')


@click.group()
@click.option('-v', '--verbose', count=True,
              help="Increase Verbosity")
@click.option('--name', default=None,
              help="Lock name. If not specified, derived from command name",
              **opt_args)
@click.option('--wait-timeout', default=15.0, type=float,
              help="Max amount of time, in seconds, to wait for lock."
                   "if 0, exit immediately if unable to get lock, "
                   "if -1, wait indefinitely",
              **opt_args)
# redis parameters
@click.option('--redis-url', '-u', envvar='REDIS_URL', default=None,
              help="If set, redis url to connect to.",
              **opt_args)
@click.option('--redis-host', '-h', envvar='REDIS_HOST', default='localhost',
              help="Redis host to connect to",
              **opt_args)
@click.option('--redis-port', '-p', envvar='REDIS_PORT', default=6379,
              help="Redis port to connect to", type=int,
              **opt_args)
@click.option('--redis-db', '-n', envvar='REDIS_DB', default=0,
              help="Redis database to connect to", type=int,
              **opt_args)
# @click.option('--redis-unix-socket-path', '-s', envvar='REDIS_UNIX_SOCKET_PATH',
#               default=None, help=" Server socket (overrides hostname and port).",
#               **opt_args)
@click.option('--redis-password', '-s', envvar='REDIS_PASSWORD', default=None,
              help="Password to use when connecting to the server",
              **opt_args)
# @click.option('--redis-ssl/--no-redis-ssl', envvar='REDIS_SSL', default=False,
#               help="SSL Mode", type=bool,
#               **opt_args)
@click.option('--auto-release-time', default=300.0, type=float,
              help="Time after which to release the lock, even if not done",
              **opt_args)
@click.option("--delay-after-acquire", type=float, default=0,
              help="Number of seconds to delay right after acquiring the lock",
              **opt_args)
@click.option("--delay-before-release", type=float, default=0,
              help="Number of seconds to delay right before releasing the lock",
              **opt_args)
@pass_config
def main_cli(config, verbose, **kwargs):
    """
        fredlock distributed locking utility

        fredlock is a distributed locking tool based on  Redis RedLock algorithm
        intended as a replacement for "flock" command line utility, it allows
        to run commands on multiple machines with a guarantee that no two
        instances will be running at the same time.

        fredlock requires a shared Redis instance to provide locking

    """
    config.update(**kwargs)
    if verbose > 1:
        pkg_logger.setLevel(logging.INFO)
    if verbose > 2:
        pkg_logger.setLevel(logging.DEBUG)
    if verbose > 3:
        root_logger.setLevel(logging.DEBUG)

    #click.echo(f"CLI Group: name={config.name}, Verb: {verbose}")


@main_cli.command(context_settings={"allow_interspersed_args": False})
@click.argument('cmd', required=True)
@click.argument('cmd_args', nargs=-1)
@pass_config
def run(config, cmd, cmd_args, **kwargs):
    """ Run command with lock """
    config.command = [cmd, *cmd_args]
    config.update(**kwargs)
    config.configure()
    #click.echo(f"Running {config.name} command: {' '.join(config.command)}")
    sys.exit(main.run(config))


@main_cli.command(context_settings={"allow_interspersed_args": False})
@click.argument('cmd', required=False, default=None)
@click.argument('cmd_args', nargs=-1, required=False, default=None)
@pass_config
def check(config, cmd, cmd_args):
    """ Check if lock is locked """
    config.command = [cmd, *cmd_args]
    config.configure()
    main.check(config)
    click.echo(f"Checking lock context for {config.name}")


@main_cli.command(context_settings={"allow_interspersed_args": False})
@click.argument('command', nargs=-1, required=False, default=None)
@pass_config
def show_config(config: Config, command):
    """ Show effective configuration """
    config.command = command
    config.configure()
    conf = dict(config=asdict(config))
    click.echo(f"\n\n{yaml.safe_dump(conf, default_flow_style=False)}")


def cli():
    """ Entry point for CLI processor """
    #click.echo("Starting CLI")
    logging.basicConfig(level=logging.WARNING, format=FORMAT)
    pkg_logger.setLevel(logging.INFO)
    main_cli(auto_envvar_prefix="FREDLOCK", show_default=True)
    click.echo("Ended CLI: this is never reached")
    return 1
