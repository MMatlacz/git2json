#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Generate a json log of a git repository.
"""

from __future__ import print_function
import json
import sys
from .parser import parse_commits

__author__ = 'Tavish Armstrong'
__email__ = 'tavisharmstrong@gmail.com'
__version__ = '0.2.3'


# -------------------------------------------------------------------
# Main


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--git-dir',
        default=None,
        help='Path to the .git/ directory of the repository you are targeting'
    )
    parser.add_argument(
        '--since',
        default=None,
        help=('Show commits more recent than a specific date. If present, '
              'this argument is passed through to "git log" unchecked. ')
    )
    parser.add_argument(
        '--origin',
        default=None,
        help='Custom origin for getting log without making full clone of the repository'
    )
    args = parser.parse_args()
    if sys.version_info < (3, 0):
        print(git2json(run_git_log(git_dir=args.git_dir, git_since=args.since, git_origin=args.origin)))
    else:
        print(git2jsons(run_git_log(git_dir=args.git_dir, git_since=args.since, git_origin=args.origin)))


# -------------------------------------------------------------------
# Main API functions


def git2jsons(s):
    return json.dumps(list(parse_commits(s)), ensure_ascii=False)


def git2json(fil):
    return json.dumps(list(parse_commits(fil.read())), ensure_ascii=False)


# -------------------------------------------------------------------
# Functions for interfacing with git


def run_git_log(git_dir=None, git_since=None, git_origin=None):
    '''run_git_log([git_dir]) -> File

    Run `git log --numstat --pretty=raw` on the specified
    git repository and return its stdout as a pseudo-File.'''
    import subprocess
    if git_dir and git_origin:
        command = [
            'git',
            '--git-dir=' + git_dir,
            'log',
            git_origin,
            '--numstat',
            '--pretty=raw'
        ]
    elif git_dir:
        command = [
            'git',
            '--git-dir=' + git_dir,
            'log',
            git_origin,
            '--numstat',
            '--pretty=raw'
        ]
    else:
        if git_origin:
            command = ['git', 'log', git_origin, '--numstat', '--pretty=raw']
        else:
            command = ['git', 'log', '--numstat', '--pretty=raw']

    if git_since is not None:
        command.append('--since=' + git_since)
    raw_git_log = subprocess.Popen(
        command,
        stdout=subprocess.PIPE
    )
    if sys.version_info < (3, 0):
        return raw_git_log.stdout
    else:
        return raw_git_log.stdout.read().decode('utf-8', 'ignore')
