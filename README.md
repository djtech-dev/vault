# Vault

**Vault** is a flexible and lightweight data/file storage, retrieval, and caching system for Python applications.  

It enables developers to manage any Python object (given a proper `Datatype` implementation), store them locally or remotely, organize them by type, and access them efficiently using an in-memory cache, all this with just a few lines of code.  

Vault has only two dependencies (`psutil` and `requests`), encourages memory usage monitoring, and will support non-blocking I/O operations.

## I. Project Structure

Vault is split into two libraries:

- **`vault`** – Core data storage library, which also includes the ability to connect to remote Vaults.
- **`vault-fastapi`** – Library for building custom servers that expose Vault storage over the network.

There are also two usage examples: one for local use-cases where Vault is used within the same Python process, and one for remote use-cases where Vault is run on a separate machine.  

Additionally, the `datatypes/` directory contains example wrappers for using Python types from common libraries with Vault.


## II. Architecture

(todo)

![Diagram for showing the core in-memory cache for accessing data](https://github.com/djtech-dev/vault/blob/fe1bf1beffe63cf73cb1e049c6383c0a762f2aa8/.readme_assets/system_architecture_1.png)

## III. Milestones

## III.I. Milestones for 1.x

There are 3 objectives to be met during the 1.x development cycle:  

- Async I/O: All I/O operations will have an async equivalent, allowing for fully asynchronus managment of I/O tasks
- Indexing DB: The new `IndexingEngine` class and the `vault-redis` package will allow to index files with names or tags instead of UUID and will allow for checksum testing.
- Easy CLI: As other data storage platforms ship CLI tools to use with their service, we want to release a `vault-click` package to help developers ship custom CLI tools for their Vaults.

We hope that at the end of the 1.x development cycle Vault will be a great solution for small to medium projects; for larger and more complex projects, check the milestones for the 2.0 development cycle.

## III.II. Milestones for 2.0

A main issue with Vault is the absence of ways to scale Vaults across multiple servers: those issue will be solved with Vault 2.0, which will introduce *Scalable Storage* (horizontal scaling), *Disk Caching* (managment of multiple copies of the same file), *Remote Channel Encryption* (use of encrypeted tunnels for communicating with remote Vaults) and *Data Streaming*.

These changes are intended to support large-scale applications and will likely require breaking changes; we are planning to recieve feedback and fix bugs during the 1.0 development cycle in order to have a stable base to build upon, before starting the 2.0 development cycle.

## IV. Vault API

The Remote API specification for Vault 1.0 is available in [`VAULT_API.md`](./VAULT_API.md).
