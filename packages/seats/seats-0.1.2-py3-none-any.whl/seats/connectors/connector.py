from abc import ABC, abstractmethod


class Connector(ABC):
    def __init__(self, target, username: str = "", password: str = ""):
        self.target = target
        self.username = username
        self.password = password

    @abstractmethod
    def login(self):
        pass

    @abstractmethod
    def logout(self):
        pass

    @abstractmethod
    def __str__(self):
        pass


class ConnectorSSH(Connector):
    @abstractmethod
    def send_command(self):
        pass


class ConnectorAPI(Connector):
    @abstractmethod
    def get(self):
        pass

    @abstractmethod
    def post(self):
        pass

    @abstractmethod
    def put(self):
        pass

    @abstractmethod
    def delete(self):
        pass
