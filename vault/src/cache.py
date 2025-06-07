from typing import Optional
from .datatype import Datatype
import copy

## Ticket given in order to access data managed by a Cache
class Ticket:
    def __init__(self, cache: Cache, data_id: int):
        self.cache: Cache = cache
        self.data_id: int = data_id
        self.edited: bool = False

    ## Run this method when you don't need to use this Ticket anymore.
    ## If you don't deactivate a ticket, it won't be deallocated from memory.
    def deactivate(self):
        # Notify cache in order to deactive ticket
        self.cache.deactivate_ticket(self)

        # Delete reference to object
        del self

    ## Get the underlaying element.
    ## NOTE Run this if you are interested in reading the data
    def get_data(self) -> Datatype:
        return self.cache.cached_data[data_id]

    ## Get the underlaying element.
    ## NOTE Run this if you are interested in cloning the data
    ## NOTE Not all Datatypes might support cloning
    def get_clone(self) -> Optional[Datatype]:
        try:
            # Try deep-copying
            return copy.deepcopy(self.cache.cached_data[data_id])
        except:
            try:
                # Try shallow-copying
                return copy.copy(self.cache.cached_data[data_id])
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
    def __init__(self, cached_type: type, max_cached: int):
        self.cached_type: type = cached_type
        self.cached_data: dict[int, cached_type] = {}
        self.max_cached: int = max_cached
        # List of IDs of elements that were changed
        self.updated_data: list[int] = []
        # List of Tickets assigned to an element
        self.tickets = dict[int, list[Ticket]] = {}

    ## Deallocate in-memory cache
    def reset(self):
        # TODO Disk updates

        # Removes all cached data without any Ticket
        data_with_tickets = list(self.tickets.keys())
        for cached in self.cached_data:
            if !(cached in data_with_tickets):
                self.cached.pop(cached)

    ## Deallocate in-memory cache if the amount of elements is greater than `max_cached`
    def upkeep(self):
        # If max_cached is equal to 0, limitations of amount of elements can't be applied
        if len(self.cached_data.keys()) > self.max_cached and self.max_cached != 0:
            self.reset()

    def deactivate_ticket(self, ticket: Ticket):
        pass # TODO


## Data structure for aligning Datatypes and their respective Cache
class CacheCollector:
    def __init__(self):
        # We can't use a Dictionary because we can't guarantee that Datatype is hashable
        # NOTE Entries can only be added, not removed or moved.

        self.datatypes: list[type] = []
        self.caches: list[Cache] = []

    def insert(self, datatype: type, cache: Cache):
        # We need to this to check if the given type actually inherits from Datatype
        assert datatype.type == Datatype
        assert len(self.datatypes) == len(self.caches)

        self.datatypes.append(datatype)
        self.caches.append(cache)

    def iter_index(self) -> range:
        assert len(self.datatypes) == len(self.caches)
        return range(0, len(self.datatypes))
