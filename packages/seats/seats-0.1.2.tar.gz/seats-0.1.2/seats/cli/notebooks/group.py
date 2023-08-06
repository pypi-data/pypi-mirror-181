import click
import site
from pathlib import Path


@click.group()
def notebooks():
    pass


@notebooks.command()
@click.argument('destination', type=click.Path())
def install(destination):
    """Copy notebooks from package to user's home folder"""
    print(Path.home())
    print(Path(destination))
    for location in site.getsitepackages():
        path = Path(location)
        package_path = path / "seats"
        if package_path.is_dir():
            print(package_path)

