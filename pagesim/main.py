#!/usr/bin/env python3
import click
import enum


class ReplacementAlgo(enum.Enum):
    FIFO = enum.auto()
    LRU = enum.auto()
    OTIMO = enum.auto()
    SEGUNDA_CHANCE = enum.auto()
    CLOCK = enum.auto()
    NRU = enum.auto()
    LFU = enum.auto()
    MFU = enum.auto()


@click.command(
    # context_settings={
    #     "color": (False if getenv("TERM") == "dumb" or getenv("NO_COLOR") else None),
    # },
    no_args_is_help=True,
)
@click.option(
    "--algo",
    metavar="ALGO",
    type=click.Choice(ReplacementAlgo, case_sensitive=False),
    required=True,
    help="Algoritmo de substituição de página",
)
@click.option(
    "--frames",
    metavar="N",
    type=click.IntRange(min=1),
    required=True,
    help="Número de frames (quadros)",
)
@click.option(
    "--trace",
    metavar="ARQUIVO",
    type=click.Path(exists=True, dir_okay=False),
    required=True,
    help="Arquivo de trace",
)
@click.option(
    "--verbose",
    is_flag=True,
    help="Habilita modo verboso",
)
@click.help_option("-h", "--help")
def cli(algo: str, frames: int, trace: str, verbose: bool) -> None:
    """Pager simulator."""

    click.echo(f"Algorithm: {algo}")
    click.echo(f"Frames: {frames}")
    click.echo(f"Trace file: {trace}")


# if __name__ == "__main__":
#     cli()
