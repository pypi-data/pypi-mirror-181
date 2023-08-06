from abc import ABC, abstractmethod


class CMDB(ABC):
    def __init__(
        self, config: dict = None, config_path: str = "config.json"
    ):
        self.config = config
        self.config_path = config_path

    @abstractmethod
    def get_customers(self) -> list:
        pass

    @abstractmethod
    def get_customer_by_name(self, customer_name: str):
        pass

    @abstractmethod
    def get_customer_by_id(self, customer_id: str):
        pass

    @abstractmethod
    def get_hosts(self, customer_id: str) -> list:
        pass

    @abstractmethod
    def get_host_config(self, customer_id: str, host_id: str) -> str:
        pass
