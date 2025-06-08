from typing import Optional
import threading

def index_files(directory: str) -> [int]:
    # List JSON files in a directory
    contents = os.listdir(directory)
    files = [
        f for f in files if os.path.isfile(Direc + "/" + f) and f.endswith(".vault")
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


'''
## Data structure for aligning Datatypes and their respective max_cached_values
## NOTE NEVER modify a Structure directly, always use the exposed methods
class Structure:
    def __init__(self):
        # We can't use a Dictionary because we can't guarantee that Datatype is hashable
        # NOTE Entries can only be added, not removed or moved.

        self.unit_names: list[str] = []
        self.datatypes: list[type] = []
        self.max_cached_values: list[int] = []

    def insert(self, unit_name: str, datatype: type, max_cached: int):
        # We need to this to check if the given type actually inherits from Datatype
        assert datatype.type == Datatype
        assert len(self.unit_names) == len(self.datatypes) == len(self.max_cached_values)
        assert max_cached > 0
        assert unit_name not in self.unit_names

        self.unit_names.append(unit_name)
        self.datatypes.append(datatype)
        self.max_cached_values.append(max_cached)

    def iter_index(self) -> range:
        assert len(self.unit_names) == len(self.datatypes) == len(self.max_cached_values)

        return range(0, len(self.unit_names))
'''

## Core object that manages all of the stored data and their relative in-memory cache.
## `max_memory_used` indicates the threshold amount of RAM (expressed in MBs) used by the process before the Vault requires to deallocate all in-memory caches.
class Vault:
    def __init__(
        self, directory: str, structure: dict[str, tuple[type, int]], max_memory_used: int = 1000
    ):
        self.directory: str = directory
        self.caches: dict[str, tuple[type, Cache]] = {}
        self.max_memory_used: int = max_memory_used

        # Populate caches using the given structure
        '''
        for structure_index in structure.iter_index():
            datatype = structure.datatypes[structure_index]
            max_cached_value = structure.max_cached_values[structure_index]
            self.caches[datatype] = Cache(datatype, structure[datatype])
        '''
        for unit_name in structure.keys():
            structure_value = structure[unit_name]
            datatype = structure_value[0]
            max_cached_value = structure_value[1]
            self.caches[unit_name] = Cache(datatype, max_cached_value)

    ## Update the Vault indexing based on the files present in the Vault's directory and subdirectories.
    def update_from_disk(self):
        pass  # TODO

    ## Check if data exists
    def _exists(self, datatype_name: str, data_id: int) -> bool:
        file_name = "{0}/{1}/{2}.vault".format(self.directory, data_type, data_id)
        return os.path.isfile(file_name)

    ## Load data from disk
    def _load(self, data_type: type, data_id: int) -> Optional[Datatype]:
        datatype_name = data_type.__name__
        if _exists(data_type, data_id):
            file_name = "{0}/{1}/{2}.vault".format(self.directory, datatype_name, data_id)
            file_obj = open(file_name, 'rb')
            data = data_type._load(file_obj) # using Datatype methods
            return data
            # TODO add cache support
        else:
            return None

    ## Store data to disk
    def _store(self, data_type: type, data: Datatype) -> int:
        datatype_name = data_type.__name__
        file_name = "{0}/{1}/{2}.vault".format(self.directory, datatype_name, data_id)
        # TODO

    ## Update disk version of modified data
    def _update(self, data_type: type, data_id: int, data: Datatype):
        datatype_name = data_type.__name__
        file_name = "{0}/{1}/{2}.vault".format(self.directory, datatype_name, data_id)
        # TODO

    ## Routine operation to manage in-memory cache
    def _upkeep(self):
        # Extract all Cache objects from the CacheCollector data structure
        caches = self.caches.caches

        if get_memory_used() > self.max_memory_used:
            # Reset all in-memory caches
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

    def spawn_upkeeping_thread(self) -> threading.Thread:
        threading.Thread(target=_upkeep_timer, args=(self, timer))

    # Load a Datatype and obtain a Ticket that can be used to access this data.
    # This is the core function to work with the data archived
    def load(self, data_type: type, data_id: int) -> Optional[Ticket]:
        pass

    # Store a Datatype and obtain an ID that can be used in the future to access this data.
    # This is the core function to archive data
    def store(self, data_type: type, data: Datatype) -> int:
        pass
