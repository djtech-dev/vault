from typing import Optional
from .datatype import Datatype
from .cache import Cache, Ticket
import threading
import os
import time
import psutil
import uuid

import logging

logger = logging.getLogger("vault/vault")


def list_vault_files(directory: str) -> list[int]:
    # List Vault-managed files in a directory
    contents = os.listdir(directory)
    files = [
        f for f in files if os.path.isfile(directory + "/" + f) and f.endswith(".vault")
    ]

    # Extract the numerical IDs
    ids = []
    for file_path in files:
        try:
            id_string = file_path.removesuffix(".vault")
            ids.append(int(id_string))
        except:
            pass
    return ids


## Get amount of RAM used by the current process in MBs
## Thanks to https://stackoverflow.com/questions/938733/total-memory-used-by-python-process
def get_memory_used() -> int:
    proc = psutil.Process()
    return proc.memory_info().rss / 1024**2


## Core object that manages all of the stored data and their relative in-memory cache.
## `max_memory_used` indicates the threshold amount of RAM (expressed in MBs) used by the process before the Vault requires to deallocate all in-memory caches.
class Vault:
    def __init__(
        self,
        directory: str,
        structure: dict[str, tuple[type, int]],
        max_memory_used: int = 1000,
    ):
        self.directory: str = directory
        self.caches: dict[str, tuple[type, Cache]] = {}
        self.max_memory_used: int = max_memory_used

        # Populate caches using the given structure
        for unit_name in structure.keys():
            structure_value = structure[unit_name]
            datatype = structure_value[0]
            max_cached_value = structure_value[1]

            assert issubclass(datatype, Datatype)
            assert max_cached_value >= 0

            self.caches[unit_name] = Cache(
                unit_name, directory, datatype, max_cached_value
            )

    ## Check if data exists
    def exists(self, unit_name: str, data_id: int) -> bool:
        file_name = "{0}/{1}/{2}.vault".format(self.directory, unit_name, data_id)
        return os.path.isfile(file_name)

    ## Load data from disk; it will return a Ticket usable to work with the in-memory version of the data
    def load(self, unit_name: str, data_id: int) -> Optional[Ticket]:
        if self.exists(unit_name, data_id):
            cache = self.caches[unit_name]
            return cache._load(self.directory, unit_name, data_id)
        else:
            return None

    ## Store new data to disk; it will create a new file and return its ID
    def upload(self, unit_name: str, data: Datatype) -> int:
        # Generate a random data_id
        data_id = 0
        while True:
            data_id = uuid.uuid4().int & ((1 << 63) - 1)
            if not self.exists(unit_name, data_id):
                break

        # Write to file
        file_name = "{0}/{1}/{2}.vault".format(self.directory, unit_name, data_id)
        with open(file_name, "wb+") as file_obj:
            file_obj.write(data._dump())

        logger.info("New {0} element created on Vault".format(unit_name))

        return data_id

    ## Store new data to disk; it will create a new file and return its ID and an open Ticket
    def create(self, unit_name: str, data: Datatype) -> tuple[int, Optional[Ticket]]:
        data_id = self.upload(unit_name, data)
        ticket = self.load(unit_name, data_id)
        return (data_id, ticket)

    ## Update disk version of specific modified data
    def _update(self, unit_name: str, data_id: int, data: Datatype):
        file_name = "{0}/{1}/{2}.vault".format(self.directory, unit_name, data_id)
        with open(file_name, "wb+") as file_obj:
            file_obj.write(data._dump())

    ## Routine operation to manage in-memory cache
    def _upkeep(self):
        # Extract all Cache objects from the CacheCollector data structure
        caches = list(self.caches.values())
        memory_used = get_memory_used()

        if memory_used > self.max_memory_used:
            # Reset all in-memory caches
            logger.warn(
                "Excessive memory usage ({0}/{1}), cleaning up caches.".format(
                    memory_used, self.max_memory_used
                )
            )
            for cache in caches:
                cache.reset()
        else:
            # Clean up cached elements, considering the max_cached values
            for cache in caches:
                cache.upkeep()

    def _upkeep_timer(self, time_elapsed: int):
        while True:
            time.sleep(time_elapsed)
            self._upkeep()

    def spawn_upkeeping_thread(self, timer: int) -> threading.Thread:
        t = threading.Thread(target=_upkeep_timer, args=(self, timer))
        t.daemon = True  # Make daemon for clean shutdown
        t.start()
        return t

    # Get Datatype of a specific Vault's Unit (= managed subdirectory)
    def get_datatype(self, unit_name: str) -> type:
        return self.caches[unit_name].cached_type
