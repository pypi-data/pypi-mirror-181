# Copyright (c) 2022 International Institute for Applied Systems Analysis.
# All rights reserved. The use and distribution terms for this software
# are covered by the MIT License (http://opensource.org/licenses/MIT)
# which can be found in the file LICENSE at the root of this distribution.
# By using this software in any fashion, you are agreeing to be bound by
# the terms of this license.
# You must not remove this notice, or any other, from this software.
"""Execution command checker."""

__author__ = "Anna Shchiptsova"
__copyright__ = "Copyright (c) 2022 IIASA"
__license__ = "MIT"

from getopt import getopt, GetoptError


def _fail(arg, label, vals):
    """Terminate execution with invalid arguments error message."""
    print(
        'Failed to validate: ' +
        arg +
        ' not supported ' +
        label +
        '\n(supported ' +
        ' '.join(map(str, vals)) +
        ')')


def parse(argv, options):
    """Parse command line arguments."""
    help_msg = 'Usage: dice-climate-simulator' + \
        ' -e <emissions> -r <ratio> -f <folder>'

    try:
        opts, _ = getopt(
            argv,
            'h:e:r:f:',
            ['emissions=', 'ratio=', 'folder='])
    except GetoptError:
        print(help_msg)
        return None

    args = {}
    args['folder'] = None
    for opt, arg in opts:
        if opt == '-h':
            print(help_msg)
            return None
        if opt in ('-e', '--emissions'):
            args['emissions'] = arg
        if opt in ('-r', '--ratio'):
            args['ratio'] = arg
        if opt in ('-f', '--folder'):
            args['folder'] = arg

    if 'emissions' not in args:
        print(help_msg)
        return None

    if args['emissions'] == 'hansel2020':
        args['ratio'] = 'hansel2020'

    if args['emissions'] not in options['emissions']:
        _fail(args['emissions'], 'emissions', options['emissions'])
    elif (args['emissions'] != 'hansel2020') and \
        ('ratio' in args) and \
            (args['ratio'] not in options['ratio']):
        _fail(args['ratio'], 'ratio', options['ratio'])
    elif ('ratio' not in args) or \
            ((args['emissions'] != 'hansel2020') and (args['folder'] is None)):
        print(help_msg)
    else:
        return args

    return None
