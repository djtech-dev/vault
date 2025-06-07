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


## Data structure for aligning Datatypes and their respective max_cached_values
class Structure:
    def __init__(self):
        # We can't use a Dictionary because we can't guarantee that Datatype is hashable
        # NOTE Entries can only be added, not removed or moved.

        self.datatypes: list[type] = []
        self.max_cached_values: list[int] = []

    def insert(self, datatype: type, max_cached: int):
        # We need to this to check if the given type actually inherits from Datatype
        assert datatype.type == Datatype
        assert len(self.datatypes) == len(self.max_cached_values)
        assert max_cached > 0

        self.datatypes.append(datatype)
        self.max_cached_values.append(max_cached)

    def iter_index(self) -> range:
        assert len(self.datatypes) == len(self.max_cached_values)
        return range(0, len(self.datatypes))


## Core object that manages all of the stored data and their relative in-memory cache.
## `max_memory_used` indicates the threshold amount of RAM (expressed in MBs) used by the process before the Vault requires to deallocate all in-memory caches.
class Vault:
    def __init__(
        self, directory: str, structure: Structure, max_memory_used: int = 1000
    ):
        self.directory: str = directory
        self.caches: CacheCollector = {}
        self.max_memory_used: int = max_memory_used

        # Populate caches using the given structure
        for structure_index in structure.iter_index():
            datatype = structure.datatypes[structure_index]
            max_cached_value = structure.max_cached_values[structure_index]
            self.caches[datatype] = Cache(datatype, structure[datatype])

    ## Update the Vault indexing based on the files present in the Vault's directory and subdirectories.
    def update_from_disk(self):
        pass  # TODO

    ## Check if data exists
    def _exists(self, datatype_name: str, data_id: int) -> bool:
        file_name = "{0}/{1}/{2}.vault".format(self.directory, data_type, data_id)
        return os.path.isfile(file_name)

    ## Load data from disk
    def _load(self, data_type: str, data_id: int) -> any:
        if _exists(data_type, data_id):
            file_name = "{0}/{1}/{2}.vault".format(self.directory, data_type, data_id)
            # TODO
        else:
            return None

    ## Store data to disk
    def _store(self, data_type: str, data: any) -> int:
        file_name = "{0}/{1}/{2}.vault".format(self.directory, data_type, data_id)
        # TODO

    ## Update disk version of modified data
    def _update(self, data_type: str, data_id: int, data: any):
        file_name = "{0}/{1}/{2}.vault".format(self.directory, data_type, data_id)
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
