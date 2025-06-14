# Vault Remote API v1.0

This document contains the specification for the first version of the Vault Remote API which allows to connect and operate with remote Vault.  

NOTE: Vault Remote API v1.0 doesn't support encryption, so instead of authentication we are using IP whitelisting, so it is needed to know (they can also be added/removed during runtime) the IPs of all the servers that will have access to the remove Vault.  

NOTE: The Remote API is not production-grade, and it might not be until Vault 2.0  

All requests and responses are formatted with JSON Schema.

## Data Processing

### - `/exists`: Checks if a file exists in the Vault
  
Parameters:
    - `unit_name` (`str`): Name of the Vault's Unit
    - `data_id` (`int`): UUID of the file

Response:
    - `exists` (`bool`): True if the file exists
  
### - `/load`: Downloads a file from the Vault 

Parameters:
    - `unit_name` (`str`): Name of the Vault's Unit
    - `data_id` (`int`): UUID of the file

Response:
    - `data` (`[byte]`): String of bytes that can be managed by Vault

### - `/upload`: Uploads a new file to the Vault



### - `/update`: Update an existing file on the Vault
