# Vault
Vault is a flexible data/file storage, retrieval and caching system for Python applications.  
It allows developers to take any Python object (with the correct `Datatype` implementation), store them (in local or remote), organize them by type, access them using the in-memory cache system, and update the saved files with just a couple of modules.  
Also, Vault is an extremely light library, having only one dependency (`psutil`).  

The project is split into two libraries:  
- `vault` ~ The file storage system itself; this library also implemented a middleware for accessing remote Vaults using the Vault API.  
- `vault-fastapi` ~ Library for building with ease custom servers exposing the Vault API.      

The project also has two examples, one for a contained use-case (project where Vault runs in the same Python process as the application) and one for a remote use-case (project where Vault runs on a separate server).  
The project also has a directory (`datatypes`) contaning small code snippets for data wrappers, which allows to use Python classes from other libraries directly from Vault.  

## I. Architecture



## II. Milestones

The main issues of Vault is the fact that there aren't any scalability functions: we are planning to first get feedback on Vault 1.0, improving the design and fixing bugs, and then we are going to work on Vault 2.0, which will introduce Scalable Storage, Disk Cache and Data Streaming, in order to allow users to develop large-scale applications.  
We warn you that Vault 2.0 will probably be a breaking update, as the design of the library might change (changes will be decided before the start of the 2.0 development cycle) in order to allow large-scale applications.  

## III. Vault API 

Check `VAULT_API.md` for the standardized specification for Vault API 1.0  
