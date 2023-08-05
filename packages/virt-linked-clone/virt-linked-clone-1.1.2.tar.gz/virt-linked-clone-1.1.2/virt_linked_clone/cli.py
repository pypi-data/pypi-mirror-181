import argparse
import os
import pathlib
import sys

from .version import __version__
from .virt_linked_clone import create_linked_clone


def env(key, *alternate_keys, default=None, environ=os.environ):
    """Fetch variables from environment, returning the first one or a default value."""
    if alternate_keys:
        return environ.get(key, env(*alternate_keys, default=default, environ=environ))
    else:
        return environ.get(key, default)


def parse_args():
    preparser = argparse.ArgumentParser(add_help=False)
    preparser.add_argument(
        '--zsh-completion',
        action='store_true',
        help="""Print out the zsh autocompletion code for this utility and exit.""",
    )
    args, _ = preparser.parse_known_args()
    if args.zsh_completion:
        here = pathlib.Path(__file__).parent
        print(pathlib.Path(here / 'zsh_completion.sh').read_text())
        sys.exit(0)

    default_connection = env('VIRSH_DEFAULT_CONNECT_URI', default='qemu:///session')

    parser = argparse.ArgumentParser(prog='virt-linked-clone', parents=[preparser])
    parser.add_argument(
        '--version',
        action='version',
        version=__version__,
    )
    parser.add_argument(
        '-c',
        '--connection',
        default=default_connection,
        help=f"""LibVirt URI to use for connecting to the domain controller. Will honor
                 the value of the VIRSH_DEFAULT_CONNECT_URI environment variable.
                 (default: {default_connection})""",
    )
    parser.add_argument(
        'source',
        help="""Virtual machine from which to create a clone where all writable
                qcow2-backed drives are linked using copy-on-write. It must be defined
                with libvirt and accessible via virsh commands.""",
    )
    parser.add_argument(
        'target',
        default='{source}-clone',
        help="""Name of the new virtual machine to define. Most of the settings of the
                source image will be copied into the new libvirt domain. Defaults to
                adding "-clone" to the source domain name.""",
    )

    args = parser.parse_args()
    args.target = args.target.format(source=args.source)
    return args


def main():
    args = parse_args()
    return create_linked_clone(args.source, args.target, connection=args.connection)
