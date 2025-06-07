from .vault import Structure, Vault
from .datatype import Datatype


## Create a new Structure giving a list of Datatypes with their max_cached_values
def new_structure(datatypes: list[Datatype], max_cached_values: list[int]) -> Structure:
    assert len(datatypes) == len(max_cached_values)

    structure = Structure()

    for index in range(0, len(datatypes)):
        data_type = type(datatypes[index])
        max_cached = max_cached_values[index]

        structure.insert(data_type, max_cached)

    return structure


## Create a new Vault with cache limits for each Datatype
def new_vault_with_cached_limits(
    directory: str, datatypes: list[Datatype], max_cached_values: list[int]
) -> Vault:
    structure = new_structure(datatypes, max_cached_values)
    vault = Vault(directory, structure)
    return vault


## Create a new Vault given the Vault's directory and the different Datatypes stored.
## If you want to use cache limits, see `new_vault_with_cached_limits`
def new_vault(directory: str, datatypes: list[Datatype]) -> Vault:
    # Create the list of max_cached_values with values equal to 0, disabling the cache limit
    max_cached_values = []
    for _ in datatypes:
        max_cached_values = [0]
    return new_vault_with_cached_limits(directory, datatypes, max_cached_values)
