import click

from .cmdbs.group import cmdb
from .connectors.group import fortigate
from .notebooks.group import notebooks


@click.group()
def entry_point():
    pass


entry_point.add_command(cmdb)
entry_point.add_command(fortigate)
entry_point.add_command(notebooks)
