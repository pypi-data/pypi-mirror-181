import json
from enum import Enum
from pathlib import Path
from typing import Any, Union

import pickledb
from pickledb import PickleDB


class StoreContainers(str, Enum):
    environment = "environment"
    user = "user"


class Store:
    """Client class for working with the data store."""

    def __init__(self):
        self._db = self.load(Path.home() / ".empowercli" / ".store.db")
        for container in StoreContainers:
            self._initialize_dict(container.value)

    def get_all(self, container_name: str) -> dict[str, Any]:
        """Get context storage key/value pairs for particular container name.

        :param container_name: context storage container name string
        :return: dict of container values
        """
        return self._db.dgetall(container_name)

    @staticmethod
    def load(path: Union[str, Path]) -> PickleDB:
        """Load context storage.

        :param path: path to the context storage file
        :return: context storage instance
        """
        return pickledb.load(path, False)

    def dump(self) -> str:
        """Dump context storage.

        :return: JSON string with context storage dump
        """
        return json.dumps(
            {collection: self.get_all(collection) for collection in self._db.getall()},
            indent=2,
        )

    def save(self, container_name: str, **kwargs) -> None:
        """
        Save a set of key value pair arguments
        """
        for key, value in kwargs.items():
            self._set(container_name, key, value)

    @property
    def empower_discovery_url(self) -> str:
        if url := (
            self._db.get(StoreContainers.environment).get("empower_discovery_url")
        ):
            return url
        raise ValueError("empower_discovery_url value is not present in the context.")

    @empower_discovery_url.setter
    def empower_discovery_url(self, value: str) -> None:
        self._set(StoreContainers.environment, "empower_discovery_url", value)

    def _set(self, container_name: str, key: str, value: Any) -> None:
        """Set context storage key-value pair for particular container name.

        :param container_name: context storage container name
        :param key: key to set
        :param value: value to set
        """
        self._db.dadd(container_name, (key, value))
        self._db.dump()
        print(f"{key} has been set")

    # only initialize a dictionary in the store if it doesn't exist,
    # otherwise it will clear them out
    def _initialize_dict(self, name: str) -> None:
        """Create a context storage dict if one doesn't exist.

        :param name: name of a dict
        """
        if not self._db.get(name):
            self._db.dcreate(name)


store = Store()
