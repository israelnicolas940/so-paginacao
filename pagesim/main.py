#!/usr/bin/env python3
import click
from pagesim.core.pager_service import PagerService
from pagesim.core.models import ReplacementAlgo


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
def cli(algo: ReplacementAlgo, frames: int, trace: str, verbose: bool) -> None:
    """Pager simulator."""
    service = PagerService(algo, frames, trace)
    report = service.run_pager()
    click.echo(report)


if __name__ == "__main__":
    cli()
