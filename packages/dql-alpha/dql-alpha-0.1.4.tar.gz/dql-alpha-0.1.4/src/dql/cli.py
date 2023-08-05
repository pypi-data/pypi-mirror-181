import logging
import sys
import traceback
from argparse import ArgumentParser, ArgumentTypeError, Namespace
from typing import Iterator, Optional, Tuple, Union

from dql import __version__, utils
from dql.catalog import Catalog
from dql.client import Client
from dql.data_storage import DefaultDataStorage
from dql.node import long_line_str

logger = logging.getLogger("dql")

TTL_HUMAN = "4h"
TTL_INT = 4 * 60 * 60


def human_time_type(
    value_str: str, can_be_none: bool = False
) -> Optional[int]:
    value = utils.human_time_to_int(value_str)

    if value:
        return value
    if can_be_none:
        return None

    raise ArgumentTypeError(
        "This option supports only a human-readable time "
        "interval like 12h or 4w."
    )


def add_sources_arg(
    parser: ArgumentParser, nargs: Union[str, int] = "+"
) -> None:
    parser.add_argument(
        "sources",
        type=str,
        nargs=nargs,
        help="Data sources - paths to cloud storage dirs",
    )


def get_parser() -> ArgumentParser:
    parser = ArgumentParser(description="DQL: Data Query Language", prog="dql")

    parser.add_argument("--version", action="version", version=__version__)

    parent_parser = ArgumentParser(add_help=False)
    parent_parser.add_argument(
        "--aws-endpoint-url",
        type=str,
        help="AWS endpoint URL",
    )
    parent_parser.add_argument(
        "--aws-anon",
        action="store_true",
        help="AWS anon (aka awscli's --no-sign-request)",
    )
    parent_parser.add_argument(
        "--ttl",
        type=human_time_type,
        default=TTL_HUMAN,
        help="Time-to-live of data source cache. Negative equals forever.",
    )
    parent_parser.add_argument(
        "-u", "--update", action="count", default=0, help="Update cache"
    )
    parent_parser.add_argument(
        "-v", "--verbose", action="count", default=0, help="Verbose"
    )
    parent_parser.add_argument(
        "-q", "--quiet", action="count", default=0, help="Be quiet"
    )

    subp = parser.add_subparsers(help="Sub-command help", dest="command")
    parse_get = subp.add_parser(
        "get", parents=[parent_parser], help="Fetch a dataset"
    )
    parse_get.add_argument(
        "source", type=str, help="Data source - a path to a cloud storage dir"
    )
    parse_get.add_argument("-o", "--output", type=str, help="Output")
    parse_get.add_argument(
        "-f",
        "--force",
        action="count",
        default=0,
        help="Force creating outputs",
    )
    parse_get.add_argument("-d", "--descr", type=str, help="Description")

    parse_cp = subp.add_parser(
        "cp", parents=[parent_parser], help="Copy data files from the cloud"
    )
    add_sources_arg(parse_cp)
    parse_cp.add_argument("output", type=str, help="Output")
    parse_cp.add_argument(
        "-f",
        "--force",
        default=False,
        action="store_true",
        help="Force creating outputs",
    )
    parse_cp.add_argument(
        "-r",
        "-R",
        "--recursive",
        default=False,
        action="store_true",
        help="Copy directories recursively",
    )
    parse_cp.add_argument(
        "--dql-file",
        help="Use a different filename for the resulting DQL file",
    )
    parse_cp.add_argument(
        "--dql-only",
        default=False,
        action="store_true",
        help=(
            "Only create the resulting DQL file, "
            "do not download or copy files"
        ),
    )
    parse_cp.add_argument(
        "--no-glob",
        default=False,
        action="store_true",
        help="Do not expand globs (such as * or ?)",
    )

    parse_ls = subp.add_parser(
        "ls", parents=[parent_parser], help="List storage contents"
    )
    add_sources_arg(parse_ls, nargs="*")
    parse_ls.add_argument(
        "-l",
        "--long",
        action="count",
        default=0,
        help="List files in the long format",
    )

    parse_du = subp.add_parser(
        "du", parents=[parent_parser], help="Display space usage"
    )
    add_sources_arg(parse_du)

    parse_find = subp.add_parser(
        "find", parents=[parent_parser], help="Walk a file hierarchy"
    )
    add_sources_arg(parse_find)
    parse_find.add_argument(
        "-name",
        "--name",
        type=str,
        action="append",
        help="Filename to match pattern.",
    )
    parse_find.add_argument(
        "-iname",
        "--iname",
        type=str,
        action="append",
        help="Like -name but case insensitive.",
    )
    parse_find.add_argument(
        "-type",
        "--type",
        type=str,
        help='File type: "f" - regular, "d" - directory',
    )
    parse_find.add_argument(
        "-jmespath",
        "--jmespath",
        type=str,
        action="append",
        help="JMESPath query to annotation",
    )

    parse_index = subp.add_parser(
        "index", parents=[parent_parser], help="Index storage location"
    )
    add_sources_arg(parse_index)
    return parser


def get_logging_level(args: Namespace) -> int:
    if args.quiet:
        return logging.CRITICAL
    elif args.verbose:
        return logging.DEBUG
    return logging.INFO


def get(source, output, **kwargs):
    data_storage = DefaultDataStorage()
    catalog = Catalog(data_storage)
    catalog.get(source, output, **kwargs)


def cp(sources, output, **kwargs):
    data_storage = DefaultDataStorage()
    catalog = Catalog(data_storage)
    catalog.cp(sources, output, **kwargs)


def ls_urls(
    sources,
    long: bool = False,
    *,
    client_config=None,
    **kwargs,
) -> Iterator[Tuple[str, Iterator[str]]]:
    if client_config is None:
        client_config = {}
    data_storage = DefaultDataStorage()
    catalog = Catalog(data_storage)
    for source in sources:
        if Client.get_implementation(source).is_root_url(source):
            buckets = Client.get_implementation(source).ls_buckets(
                **client_config
            )
            if long:
                values = (
                    long_line_str(b.name, b.created, "") for b in buckets
                )
            else:
                values = (b.name for b in buckets)
            yield source, values
        else:
            for data_source, nodes in catalog.ls(
                [source], client_config=client_config, **kwargs
            ):
                if long:
                    values = (n.long_line_str() for n in nodes)
                else:
                    values = (n.name_with_dir_ending for n in nodes)
                yield data_source.node.path, values


def ls_indexed_storages(long: bool = False) -> Iterator[str]:
    storages = Catalog(DefaultDataStorage()).ls_storages()
    if long:
        for s in storages:
            # TODO: add Storage.created so it can be used here
            yield long_line_str(s.uri, None, "")
    else:
        for s in storages:
            yield s.uri


def ls(sources, long: bool = False, **kwargs):
    if sources:
        if len(sources) == 1:
            for _, entries in ls_urls(sources, long=long, **kwargs):
                for entry in entries:
                    print(entry)
        else:
            for source, entries in ls_urls(sources, long=long, **kwargs):
                print(f"{source}:")
                for entry in entries:
                    print(entry)
    else:
        for entry in ls_indexed_storages(long=long):
            print(entry)


def du(sources, **kwargs):
    data_storage = DefaultDataStorage()
    catalog = Catalog(data_storage)
    for path, size in catalog.du(sources, **kwargs):
        print("{: >7} {}".format(utils.sizeof_fmt(size), path))


def find(sources, **kwargs):
    data_storage = DefaultDataStorage()
    catalog = Catalog(data_storage)
    yield from catalog.find(sources, **kwargs)


def index(sources, **kwargs):
    data_storage = DefaultDataStorage()
    catalog = Catalog(data_storage)
    catalog.index(sources, **kwargs)


def main():  # noqa: C901
    parser = get_parser()
    args = parser.parse_args()

    logger.addHandler(logging.StreamHandler())
    logging_level = get_logging_level(args)
    logger.setLevel(logging_level)

    client_config = {
        "aws_endpoint_url": args.aws_endpoint_url,
        "aws_anon": args.aws_anon,
    }

    try:
        if args.command == "get":
            # TODO: descr = args.descr
            get(
                args.source,
                args.output,
                force=bool(args.force),
                update=bool(args.update),
                ttl=args.ttl,
                client_config=client_config,
            )
        elif args.command == "cp":
            cp(
                args.sources,
                args.output,
                force=bool(args.force),
                update=bool(args.update),
                recursive=bool(args.recursive),
                dql_file=args.dql_file,
                dql_only=args.dql_only,
                no_glob=args.no_glob,
                ttl=args.ttl,
                client_config=client_config,
            )
        elif args.command == "ls":
            ls(
                args.sources,
                ttl=args.ttl,
                update=bool(args.update),
                long=bool(args.long),
                client_config=client_config,
            )
        elif args.command == "du":
            du(
                args.sources,
                ttl=args.ttl,
                update=bool(args.update),
                client_config=client_config,
            )
        elif args.command == "find":
            for result in find(
                args.sources,
                ttl=args.ttl,
                update=bool(args.update),
                names=args.name,
                inames=args.iname,
                typ=args.type,
                jmespath=args.jmespath,
                client_config=client_config,
            ):
                print(result)
        elif args.command == "index":
            index(
                args.sources,
                ttl=args.ttl,
                update=bool(args.update),
                client_config=client_config,
            )

    except Exception as exc:  # pylint: disable=broad-except
        print("Error:", exc, file=sys.stderr)
        if logging_level <= logging.DEBUG:
            traceback.print_exception(
                type(exc),
                exc,
                exc.__traceback__,
                file=sys.stderr,
            )
        sys.exit(1)
