from typing import Optional
from .datatype import Datatype
import copy

import logging

logger = logging.getLogger("vault/cache")


## Ticket given in order to access data managed by a Cache
class Ticket:
    def __init__(self, cache: Cache, data_id: int, ticket_id: int):
        self.cache: Cache = cache
        self.data_id: int = data_id
        self.ticket_id: int = ticket_id

        self.edited: bool = False
        self.auto_deactivate: bool = True

    ## Run this method when you don't need to use this Ticket anymore.
    ## If you don't deactivate a ticket, it won't be deallocated from memory.
    def deactivate(self):
        # Notify cache in order to deactive ticket
        self.cache.deactivate_ticket(self)

        # Delete reference to object
        del self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.auto_deactivate:
            self.deactivate()

    ## Get the underlaying element.
    ## NOTE Run this if you are interested in reading the data
    def get_data(self) -> Datatype:
        return self.cache.cached_data[self.data_id]

    ## Get the underlaying element.
    ## NOTE Run this if you are interested in cloning the data
    ## NOTE Not all Datatypes might support cloning
    def get_clone(self) -> Optional[Datatype]:
        try:
            # Tries deep-copying
            return copy.deepcopy(self.cache.cached_data[self.data_id])
        except (TypeError, AttributeError) as e:
            try:
                # Tries shallow-copying
                return copy.copy(self.cache.cached_data[self.data_id])
            except (TypeError, AttributeError):
                return None

    ## Get the underlaying element.
    ## NOTE Run this if you are interested in editing the data
    def get_ref(self) -> Datatype:
        self.edited = True
        return self.cache.cached_data[self.data_id]


## In-memory cache for a specific Datatype
class Cache:
    def __init__(
        self, unit_name: str, main_directory: str, cached_type: type, max_cached: int
    ):
        self.unit_name: str = unit_name
        self.cached_type: type = cached_type
        self.cached_data: dict[int, cached_type] = {}

        # Maximum amount of cached elements
        self.max_cached: int = max_cached

        # Vault's directory
        self.directory: str = main_directory

        # Update data on disk as soon as an editing Ticket is closed.
        # If set to False, only one disk write operation will when all Tickets are closed.
        # If set to True, there will be some performance overhead, but it will provide better stability (in case of error, shutdown, etc)
        self.auto_update: bool = True

        # List of IDs of elements that were changed
        # Only used if `auto_update` is set to False
        self.updated_data: list[int] = []

        # Tickets assigned to an element
        self.tickets: dict[int, list[Ticket]] = {}
        self.current_ticket_id: int = 0

    def _load(self, unit_name: str, data_id: str) -> Ticket:
        # If data isn't loaded in memory, load it now
        if data_id not in self.cached_data.keys():
            file_name = "{0}/{1}/{2}.vault".format(self.directory, unit_name, data_id)

            # Use context manager for proper file handling
            with open(file_name, "rb") as file_obj:
                data: Datatype = self.cached_type._load(file_obj.read())

            self.cached_data[data_id] = data

        # Create Ticket and register it as open
        ticket: Ticket = Ticket(self, data_id, self.current_ticket_id)

        # Initialize tickets list if it doesn't exist
        if data_id not in self.tickets:
            self.tickets[data_id] = []

        open_tickets = self.tickets[data_id]
        open_tickets.append(ticket)
        self.current_ticket_id += 1
        logger.info("Element loaded on {0} cache.".format(self.unit_name))
        return ticket

    ## Deallocate in-memory cache
    def reset(self):
        # Removes all cached data without any Ticket
        data_with_tickets = list(self.tickets.keys())
        for cached in list(self.cached_data.keys()):
            if cached not in data_with_tickets:
                self.cached_data.pop(cached)
                logger.info("Element uncached on {0} cache.".format(self.unit_name))

    ## Deallocate in-memory cache if needed
    def upkeep(self):
        # If max_cached is equal to 0, limitations of amount of elements can't be applied
        if len(self.cached_data.keys()) > self.max_cached and self.max_cached != 0:
            self.reset()

    def _update(self, data_id: int):
        file_name = "{0}/{1}/{2}.vault".format(self.directory, self.unit_name, data_id)
        data = self.cached_data[data_id]
        with open(file_name, "wb+") as file_obj:
            file_obj.write(data._dump())

    def deactivate_ticket(self, ticket: Ticket):
        # Update files if auto-update is enabled or if this is the last edited Ticket.
        if ticket.edited:
            if self.auto_update:
                self._update(ticket.data_id)
            else:
                # Count edited open Tickets remaining
                edited_tickets_found: int = 0
                for searched_ticket in self.tickets[ticket.data_id]:
                    if searched_ticket.edited:
                        edited_ticket_found += 1

                # Update only if this is the last open edited Ticket
                if edited_tickets_found == 1:
                    self._update(ticket.data_id)

        # Remove ticket
        open_tickets = self.tickets[ticket.data_id]
        open_tickets.remove(ticket)

        # Clear self.tickets if there are datas with 0 open tickets
        if not self.tickets[ticket.data_id]:
            del self.tickets[ticket.data_id]

        # DO NOT RUN `self.upkeep()`, it's too slow to do every ticket deactivation
        # Let `Vault._upkeep()` handle all memory upkeeping tasks

        del ticket

        logger.info("Ticket deactivated on {0} cache.".format(self.unit_name))
