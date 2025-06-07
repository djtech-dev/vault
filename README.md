# Vault

**Vault** is a flexible and lightweight data/file storage, retrieval, and caching system for Python applications.  

It enables developers to manage any Python object (given a proper `Datatype` implementation), store them locally or remotely, organize them by type, and access them efficiently using an in-memory cache, all this with just a few lines of code.  

Vault has only two dependencies (`psutil` and `requests`, which is optional), and will support non-blocking I/O operations.

---

## I. Project Structure

Vault is split into two libraries:

- **`vault`** – Core file storage and caching library. Also includes middleware for interacting with remote Vaults via the Vault API.
- **`vault-fastapi`** – Simplifies building custom FastAPI servers that expose Vault storage over the network.

There are also two usage examples: one for local use-cases where Vault is used within the same Python process, and one for remote use-cases where Vault is run on a separate machine.  

Additionally, the `datatypes/` directory contains example wrappers for using Python types from common libraries with Vault.

---

## II. Architecture

---

## III. Milestones

A main issue with Vault is the absence of ways to scale Vaults across multiple servers: those issue will be solved with Vault 2.0, which will introduce *Scalable Storage*, *Disk Caching* and *Data Streaming*.

These changes are intended to support large-scale applications and will likely require breaking changes; we are planning to recieve feedback and fix bugs during the 1.0 development cycle in order to have a stable base to build upon, before starting the 2.0 development cycle.

Before that, a key improvement planned for 1.x is support for *non-blocking data operations**, either through async-compatible methods for the already implement classes or async-specific variants of existing classes.

---

## IV. Vault API

The Remote API specification for Vault 1.0 is available in [`VAULT_API.md`](./VAULT_API.md).
