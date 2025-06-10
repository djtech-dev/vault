"""
░█▀▀░▀█▀░█░░░█▀▀░█░█░█▀▀░█▀▀░█▀█░█▀▀░█▀▄░
░█▀▀░░█░░█░░░█▀▀░█▀▄░█▀▀░█▀▀░█▀▀░█▀▀░█▀▄░
░▀░░░▀▀▀░▀▀▀░▀▀▀░▀░▀░▀▀▀░▀▀▀░▀░░░▀▀▀░▀░▀░
░░░Simple document keeping application░░░
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░

        Version 1 ~ 09.06.2025
         Built for Vault 1.0
      Released under MIT License
"""

from vault.vault import Vault
from vault.cache import Cache, Ticket
from vault.datatype import Datatype
import json


# Document, rappresented as a Vault-compatible class
class Document(Datatype):
    def __init__(self, text: str):
        self.text = text

    def _dump(self) -> bytes:
        return self.text.encode("utf-8")

    def _load(raw: bytes) -> "Document":
        text = str(raw, encoding="utf-8")
        return Document(text)


# Set of references of Documents, rappresented as a Vault-compatible class
class Folder(Datatype):
    def __init__(self, documents_uuid: list[int]):
        self.documents_uuid: list[int] = document_uuid

    def _dump(self) -> bytes:
        return json.dumps(self.documents_uuid)

    def _load(raw: bytes) -> "Folder":
        return Folder(json.loads(raw))


# Vault's structure, with correct types and cache sizes
FILEKEEPER_STRUCTURE: dict[str, tuple[type, int]] = {
    "documents": (Document, 10),
    "folders": (Folder, 10),
}


class FileKeeper:
    def __init__(self, directory: str):
        # Working directory for the DB and the Vault
        self.directory = directory

        # NOTE A key-value system for string-based data retrieval will be implemented
        #      in Vault in a future version of the 1.x branch.
        #      For now, we'll use a dictionary for each Vault's Unit.
        # ----------
        # The keys are the document's name, the values are the data's UUID
        self.documents: dict[str, int] = {}
        # The keys are the folder's name, the values are the data's UUID
        self.folders: dict[str, int] = {}

        self.vault = Vault(
            directory,  # Working directory
            FILEKEEPER_STRUCTURE,  # Vault's typed structure
            max_memory_used=512,  # Maximum 512MB of cache
        )


print("Test")
fk = FileKeeper("test-filekeeper")
