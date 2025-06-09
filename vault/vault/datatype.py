import pickle
import json


## Data that can be managed by a Vault
## Every class stored in a Vault needs to inherit Datatype and implement `_dump` and `_load`
class Datatype:
    def _dump(self) -> bytes:
        pass

    def _load(raw: bytes) -> Datatype:
        pass


## Wrapper for data that can be managed by a Vault.
## This is useful if your code isn't implementing the original class so it can't add more methods
class Wrapper(Datatype):
    def __init__(self, data: any):
        self.data = data


## Datatype wrapper for using pickle on generic objects
## NOTE Data under this format might be insecure
## NOTE See https://docs.python.org/3/library/pickle.html#comparison-with-json
class PickleWrapper(Wrapper):
    def _dump(self) -> bytes:
        return pickle.dumps(self.data)

    def _load(raw: bytes) -> PickleWrapper:
        return PickleWrapper(pickle.loads(raw))


## Datatype wrapper for using JSON on generic objects
class JsonWrapper(Wrapper):
    def _dump(self) -> bytes:
        return json.dumps(self.data)

    def _load(raw: bytes) -> JsonWrapper:
        return JsonWrapper(json.loads(raw))


## Datatype class for using pickle on custom classes; those classes need to inherit PickleDatatype
## NOTE Data under this format might be insecure
## NOTE See https://docs.python.org/3/library/pickle.html#comparison-with-json
class PickleDatatype(Datatype):
    def _dump(self) -> bytes:
        return pickle.dumps(self)

    def _load(raw: bytes) -> PickleDatatype:
        return PickleDatatype(pickle.loads(raw))


## Datatype class for using JSON on custom classes; those classes need to inherit JsonDatatype
class JsonDatatype(Datatype):
    def _dump(self) -> bytes:
        return json.dumps(self)

    def _load(raw: bytes) -> JsonDatatype:
        return JsonDatatype(json.loads(raw))
