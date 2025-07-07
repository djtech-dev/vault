from .vault import VaultProxy
from .datatype import Datatype
from .cache import Cache, Ticket
import requests

## Vault Proxy usable to connect to a remote Vault server
class NetworkVault(VaultProxy):
    def __init__(self, ip_addr: str, port: int):
        pass # TODO

    def _exists(self, vault: "Vault", unit_name: str, data_id: int) -> bool:
        file_name = "{0}/{1}/{2}.vault".format(self.directory, unit_name, data_id)
        return os.path.isfile(file_name)

    def _load(self, vault: "Vault", unit_name: str, data_id: int) -> Optional[bytes]:
        if self.exists(unit_name, data_id):
            cache = self.caches[unit_name]
            return cache._load(self.directory, unit_name, data_id)
        else:
            return None

    def _upload(self, vault: "Vault", unit_name: str, data: Datatype) -> int:
        data_id = 0
        while True:
            data_id = uuid.uuid4().int & ((1 << 63) - 1)
            if not self.exists(unit_name, data_id):
                break

            # Write to file
            file_name = "{0}/{1}/{2}.vault".format(
                self.directory, unit_name, data_id
            )
            with open(file_name, "wb+") as file_obj:
                file_obj.write(data._dump())

            logger.info("New {0} element created on Vault".format(unit_name))

            return data_id

    def _update(self, vault: "Vault", unit_name: str, data_id: int, data: Datatype):
        file_name = "{0}/{1}/{2}.vault".format(self.directory, unit_name, data_id)
        with open(file_name, "wb+") as file_obj:
            file_obj.write(data._dump())
