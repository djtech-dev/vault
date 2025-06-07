from .datatype import Datatype


## In-memory cache for a specific Datatype
class Cache:
    def __init__(self, cached_type: type, max_cached: int):
        self.cached_type: type = cached_type
        self.cached_data: dict[int, cached_type] = {}
        self.max_cached: int = max_cached
        self.updated_data: list[int] = []

    ## Deallocate in-memory cache
    def reset(self):
        pass  # TODO

    ## Deallocate in-memory cache if the amount of elements is greater than `max_cached`
    def upkeep(self):
        if len(self.cached_data.keys()) > self.max_cached:
            self.reset()


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
