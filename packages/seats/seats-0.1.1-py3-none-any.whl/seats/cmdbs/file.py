from seats.cmdbs.cmdb import CMDB
from seats.connectors.file import ConnectorFile
from seats.models.customer import Customer


class FromFile(CMDB):
    """
    Service defined in file.

    Attributes
    ----------

    config : str


    Methods
    -------

    """

    def __init__(
        self, config: dict = None, config_path: str = "config.json"
    ):
        """
        Parameters
        ----------
        config : None
            Is not used for this connector and is set to None by default
        config_path: str
            The default value is 'config.json'
            Must point to a valid cmdb file.
            The file must be in JSON, YAML or XML formats.
            The file should have the extension .json, .yaml or .xml.
            The file should contain a list of customers.
            For an example of a valid file check notebooks/cmdb.json
        """
        super().__init__(config, config_path)
        self.config = config
        self.config_path = config_path
        self.connector = ConnectorFile(self.config_path)
        self.file = self.connector.load_file()
        self.customers = self.get_customers()

    def __str__(self):
        return f"{self.config_path}: {self.connector}"

    def get_customers(self) -> list:
        """
        Iterates over provided file to retrieve customers information.
        Loads name, id and hosts for customer and instantiates a Customer.

        returns: List of Customers
        """
        if type(self.file) != list:
            raise Exception("File does not seem to contain a valid list")
        customers = []
        for customer in self.file:
            customers.append(
                Customer(
                    name=customer.get("name"),
                    customer_id=customer.get("id"),
                    hosts=customer.get("hosts"),
                )
            )
        return customers

    def get_customer_by_name(self, customer_name: str) -> dict:
        return next(x for x in self.customers if x.get("name") == customer_name)

    def get_customer_by_id(self, customer_id: str) -> dict:
        return next(x for x in self.customers if x.get("id") == customer_id)

    def get_hosts(self, customer_id: str) -> list:
        customer = next(x for x in self.customers if x.id == customer_id)
        return customer.hosts

    def get_host_config(self, customer_id: str, host_id: str) -> str:
        hosts = self.get_hosts(customer_id)
        host = next(x for x in hosts if x.get("id") == host_id)
        return host.get("config")
