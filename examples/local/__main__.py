from vault import new_vault
from vault.datatype import *

# We are using the `new_vault` to create/load a Vault with a 2 JSON Datatypes
vault = new_vault("vault01", [JsonDatatype, JsonDatatype])
