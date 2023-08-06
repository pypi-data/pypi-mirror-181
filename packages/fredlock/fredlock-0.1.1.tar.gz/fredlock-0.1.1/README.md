[![Build Status](https://travis-ci.com/mlasevich/fredlock.svg?branch=main)](https://travis-ci.com/github/mlasevich/fredlock)
[![Coverage Status](https://coveralls.io/repos/github/mlasevich/fredlock/badge.svg?branch=master)](https://coveralls.io/github/mlasevich/fredlock?branch=main)
[![PyPI version](https://badge.fury.io/py/fredlock.svg)](https://badge.fury.io/py/fredlock)

![fredlock](docs/fredlock-logo-sm.png)
# fredlock - Redis RedLock based distributed locking tool 

fredlock distributed locking utility

fredlock is a distributed locking tool based on  Redis RedLock algorithm
intended as a replacement for "flock" command line utility, it allows
to run commands on multiple machines with a guarantee that no two
instances will be running at the same time.

fredlock requires a shared Redis instance to provide locking


## Release Notes

* 0.1.1 - Bugfixes
  * Removed `--redis_ssl` and `--redis-unix-socket-path` command line options for now,
  not compatible with older redis clients
  * Fixed sleep after acquire/before release


* 0.1.0 - Initial version
  * Features
    * Auto-release of a lock after x seconds if command does not 
      complete in allotted time. (`--auto-release-time x`)
    * Specify how long to wait for lock
      * Indefinitely (`--wait-timeout -1`)
      * Limited Time (`--wait-timeout x` (x > 0))
      * Do not wait (`--wait-timeout 0`)
    * Custom Optional Delays:
      * After lock acquire, before command execution (`--delay-after-acquire x`)
      * After command execution, before lock release (` --delay-before-release x`)

## TODOs:

Some other ideas/desired features:

* Quiet timeouts (no output/failure if not run due to timeout trying to get lock)
* Config file (currently we support cli and env variables)
* Redis Cluster support
* Lock Namespacing


## Installation

From PyPi:

    pip install fredlock

## Usage

Full build-in usage is available with `--help` flag.

### Run command with automatically-generated name lock

Simplest usage to run a command `command arg1 arg2` with lock _command_:

    fredlock run command arg1 arg2

### Run command with a specified name lock

Simplest usage to run a command `command arg1 arg2` with lock _lockname_:

    fredlock --name lockname run command arg1 arg2

