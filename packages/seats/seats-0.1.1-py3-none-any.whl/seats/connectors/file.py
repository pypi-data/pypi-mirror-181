import yaml
import json
import xmltodict
from pathlib import Path
from seats.connectors.connector import Connector


class ConnectorFile(Connector):
    def __init__(self, target: str):
        super().__init__(target)
        self.target = target
        self.file = Path(target)
        self.format = self.file.suffix

    def __str__(self):
        return self.file.name

    def login(self):
        pass

    def logout(self):
        pass

    def load_file(self):
        match self.format:
            case ".yaml":
                return yaml.safe_load(self.file)
            case ".json":
                return json.loads(self.file.read_text())
            case ".xml":
                return xmltodict.parse(self.file.read_text())
            case _:
                raise NotImplementedError(
                    f"File extension {self.format} not supported."
                )
