import click
from pathlib import Path
import ssf.files
import os


@click.command()
@click.argument("src")
@click.argument("dst")
def main(src: str, dst: str) -> None:
    ssf.files.symlink(Path(os.path.expanduser(src)), Path(os.path.expanduser(dst)))
