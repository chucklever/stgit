#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- python -*-
from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import optparse
import os
import sys

from stgit import argparse, commands
from stgit.completion.bash import write_bash_completion
from stgit.completion.fish import write_fish_completion
import stgit.main


def main():
    op = optparse.OptionParser()
    op.add_option(
        '--asciidoc',
        metavar='CMD',
        help='Print asciidoc documentation for a command',
    )
    op.add_option(
        '--commands',
        action='store_true',
        help='Print list of all stg subcommands',
    )
    op.add_option(
        '--cmd-list', action='store_true', help='Print asciidoc command list'
    )
    op.add_option(
        '--py-cmd-list', action='store_true', help='Write Python command list'
    )
    op.add_option(
        '--bash-completion',
        action='store_true',
        help='Write bash completion code',
    )
    op.add_option(
        '--fish-completion',
        action='store_true',
        help='Write fish completion code',
    )
    options, args = op.parse_args()
    if args:
        op.error('Wrong number of arguments')
    if options.asciidoc:
        argparse.write_asciidoc(stgit.main.commands[options.asciidoc],
                                sys.stdout)
    elif options.commands:
        for cmd, _, _, _ in commands.get_commands(allow_cached=False):
            print(cmd)
    elif options.cmd_list:
        commands.asciidoc_command_list(
            commands.get_commands(allow_cached=False), sys.stdout
        )
    elif options.py_cmd_list:
        commands.py_commands(
            commands.get_commands(allow_cached=False), sys.stdout
        )
    elif options.bash_completion:
        write_bash_completion(sys.stdout)
    elif options.fish_completion:
        write_fish_completion(sys.stdout)
    else:
        op.error('No command')


if __name__ == '__main__':
    if os.environ.get('COVERAGE_PROCESS_START'):
        import coverage

        cov = coverage.process_startup()
        cov.switch_context('build')

    main()
