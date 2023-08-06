class Customer:
    def __init__(self, name: str, customer_id: str, hosts: list = None):
        self.name = name
        self.id = customer_id
        self.hosts = hosts

    def get_details(self) -> list:
        pass

    def get_hosts(self, customer_id: str = "") -> list:
        pass

    def __str__(self):
        return self.name
