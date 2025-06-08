from typing import Optional
from .datatype import Datatype
import copy


## Ticket given in order to access data managed by a Cache
class Ticket:
    def __init__(self, cache: Cache, data_id: int, ticket_id: int):
        self.cache: Cache = cache
        self.data_id: int = data_id
        self.edited: bool = False
        self.ticket_id: int = ticket_id
        self.auto_deactivate: bool = True

    ## Run this method when you don't need to use this Ticket anymore.
    ## If you don't deactivate a ticket, it won't be deallocated from memory.
    def deactivate(self):
        # Notify cache in order to deactive ticket
        self.cache.deactivate_ticket(self)

        # Delete reference to object
        del self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self.auto_deactivate:
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
            # Try deep-copying
            return copy.deepcopy(self.cache.cached_data[self.data_id])
        except:
            try:
                # Try shallow-copying
                return copy.copy(self.cache.cached_data[self.data_id])
            except:
                # Datatype impossible to clone
                return None

    ## Get the underlaying element.
    ## NOTE Run this if you are interested in editing the data
    def get_ref(self) -> Datatype:
        self.edited = True
        return self.cache.cached_data[data_id]


## In-memory cache for a specific Datatype
class Cache:
    def __init__(self, unit_name: str, cached_type: type, max_cached: int):
        self.unit_name: str = unit_name
        self.cached_type: type = cached_type
        self.cached_data: dict[int, cached_type] = {}
        self.max_cached: int = max_cached
        # List of IDs of elements that were changed
        self.updated_data: list[int] = []
        # List of Tickets assigned to an element
        self.tickets: dict[int, list[Ticket]] = {}
        self.current_ticket_id: int = 0

    def _load(self, directory: str, unit_name: str, data_id: str) -> Ticket:
        # If data isn't loaded in memory, load it now
        if data_id not in self.cached_data.keys():
            file_name = "{0}/{1}/{2}.vault".format(self.directory, unit_name, data_id)
            file_obj = open(file_name, "rb")
            data: Datatype = data_type._load(file_obj.read())  # using Datatype methods
            self.cached_data[data_id] = data

        # Create Ticket and register it as open
        ticket: Ticket = Ticket(self, data_id, self.current_ticket_id)
        open_tickets = self.tickets[data_id]
        open_tickets.append(ticket)
        self.current_ticket_id += 1
        return ticket

    ## Deallocate in-memory cache
    def reset(self):
        # Removes all cached data without any Ticket
        data_with_tickets = list(self.tickets.keys())
        for cached in self.cached_data.keys():
            if cached not in data_with_tickets:
                self.cached.pop(cached)

    ## Deallocate in-memory cache if needed
    def upkeep(self):
        # If max_cached is equal to 0, limitations of amount of elements can't be applied
        if len(self.cached_data.keys()) > self.max_cached and self.max_cached != 0:
            self.reset()

    def deactivate_ticket(self, ticket: Ticket):
        # Update files
        # TODO

        # Remove ticket
        open_tickets = self.tickets[data_id]
        open_tickets.remove(ticket)

        del ticket
