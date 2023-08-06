#!/usr/bin/env python

import os
import sys
from importlib.machinery import SourceFileLoader
from unittest import TestLoader, TextTestRunner

import click

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

sys.path.append(os.getcwd())


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version='1.0.0')
def process_request():
    pass


@process_request.command(short_help='run tags application')
@click.argument('input_device')
@click.option('-f', '--format', default='json', show_default=True, help='use this format to generate output',
              type=click.Choice(['json', 'pb'], case_sensitive=False))
@click.option('-o', '--output', help='the file name where the result should be stored; '
                                     'if missing or equal to "-", use stdout')
def tags(**kwargs):
    """
    NetSpyGlass tags assignment Python application
    """
    from apps import tags_app
    tags_app.script_run(kwargs['input_device'], kwargs['output'], kwargs['format'])


@process_request.command(short_help='run variable builder application')
@click.argument('input_device')
@click.option('-f', '--format', default='json', show_default=True, help='use this format to generate output',
              type=click.Choice(['json', 'report'], case_sensitive=False))
@click.option('-o', '--output', help='the file name where the result should be stored; '
                                     'if missing or equal to "-", use stdout')
def variables(**kwargs):
    """
    NetSpyGlass polling variable builder Python application
    """
    from apps import variables_app
    variables_app.script_run(kwargs['input_device'], kwargs['output'], kwargs['format'])


@process_request.command(short_help='run views application')
@click.argument('input_devices')
@click.option('-o', '--output', help='the file name where the result should be stored; '
                                     'if missing or equal to "-", use stdout')
def views(**kwargs):
    """
    NetSpyGlass views assignment Python application
    """
    from apps import views_app
    views_app.script_run(kwargs['input_devices'], kwargs['output'])


@process_request.command(short_help='run tests in the current repository')
@click.argument('path')
def test(**kwargs):
    path = kwargs['path']
    sys.path.append('scripts')

    if os.path.isdir(path):
        suite = TestLoader().discover(path)
    elif os.path.isfile(path):
        foo = SourceFileLoader('foo', path).load_module()
        suite = TestLoader().loadTestsFromModule(foo)
    else:
        print('Given path is neither a file or directory', file=sys.stderr)
        sys.exit(1)

    TextTestRunner(verbosity=1).run(suite)


if __name__ == '__main__':
    process_request()
