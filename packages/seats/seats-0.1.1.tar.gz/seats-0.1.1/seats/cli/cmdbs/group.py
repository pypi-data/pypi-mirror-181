import click
from seats.cmdbs.file import FromFile


@click.group()
def cmdb():
    pass


@cmdb.command()
@click.argument('config', type=click.File())
def file(config):
    """Loads cmdb information from file"""
    srv = FromFile(config_path=config)
    customers = srv.get_customers()
    for customer in customers:
        print(customer)
        print(customer.hosts)
