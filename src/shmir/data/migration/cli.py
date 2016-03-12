import argparse
import os

from alembic import command
from alembic import config as alembic_config

from shmir import settings


def do_version(config):
    return command.current(config)


def do_upgrade(config, revision=None):
    # Parser already shoud have a "revision" value, even it it's None,
    # therefore real default value is set here
    if revision is None:
        revision = 'head'
    return command.upgrade(config, revision)


def do_downgrade(config, revision=None):
    return command.downgrade(config, revision)


def do_stamp(config, revision=None):
    return command.stamp(config, revision)


def do_revision(config, message=None, autogenerate=False):
    return command.revision(config, message, autogenerate)


def get_alembic_config():
    config = alembic_config.Config('/etc/shmir/alembic.ini')
    config.set_main_option('sqlalchemy.url', settings.FCONN)

    return config


def main():
    parser = argparse.ArgumentParser(prog='shmir-db-manage')
    subparsers = parser.add_subparsers()

    version = subparsers.add_parser('version')
    version.set_defaults(func=do_version)

    upgrade = subparsers.add_parser('upgrade')
    upgrade.add_argument('revision', nargs='?')
    upgrade.set_defaults(func=do_upgrade)

    downgrade = subparsers.add_parser('downgrade')
    downgrade.add_argument('revision', nargs='?')
    downgrade.set_defaults(func=do_downgrade)

    stamp = subparsers.add_parser('stamp')
    stamp.add_argument('revision')
    stamp.set_defaults(func=do_stamp)

    revision = subparsers.add_parser('revision')
    revision.add_argument('-m', '--message')
    revision.add_argument('--autogenerate', action='store_true')
    revision.set_defaults(func=do_revision)

    config = get_alembic_config()
    parsed_args = parser.parse_args().__dict__
    func = parsed_args.pop('func')

    return func(config, **parsed_args)
