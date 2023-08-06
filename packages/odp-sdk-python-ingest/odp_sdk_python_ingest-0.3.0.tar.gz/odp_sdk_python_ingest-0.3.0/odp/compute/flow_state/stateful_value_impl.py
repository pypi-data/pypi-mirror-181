"""Stateful flow and task values"""
from dataclasses import dataclass, field
from typing import Any, Optional

from prefect.context import FlowRunContext, TaskRunContext, get_run_context
from prefect_kv import KVStore

__all__ = ["StatefulValue", "stateful_value"]


@dataclass
class StatefulValue:
    """Stateful value - persist values across task/flow runs"""

    name: str

    _value: Any = field(init=False, default=None)
    _store: Optional[KVStore] = field(init=False, repr=False, default=None)

    def __post_init__(self):
        self._store = KVStore(self._get_qualified_prefix())
        self.update()

    def _get_qualified_prefix(self) -> str:
        context = get_run_context()
        if isinstance(context, TaskRunContext):
            ret = "task-{}".format(context.task.name)
        elif isinstance(context, FlowRunContext):
            ret = "flow-{}".format(context.flow.name)
        else:
            raise ValueError("Invalid run context: %s", type(context).__name__)

        return ret.replace("_", "-").lower()

    @property
    def value(self) -> Any:
        """Retrieve the stateful value

        Returns:
            Value within `StatefulValue` instance
        """
        return self._value

    @value.setter
    def value(self, value: Any):
        """Set the stateful value. Value will be persisted.

        In order to not persist the value, use the `set_value`-method instead

        Args:
            value: Value to be set.
        """
        self.set_value(value, persist=True)

    def set_value(self, value: Any, persist: bool = True):
        """Set the stateful value. Optionally disable persistence. Value can be
        manually persisted later using the `persist`-method.

        Args:
            value: Value to be set
            persist: Set to `False` to not persist the value.
        """

        self._value = value
        if persist:
            self.persist()

    def get_value(self, default=None) -> Any:
        """Retrieve the stateful value, optionally return a default value

        Returns:
            Value within `StatefulValue` instance or the supplied `default`
        """
        if self._value is None:
            return default
        return self._value

    def persist(self):
        """Persist the value to the backend `KVStore`."""
        self._store.set(self.name, self._value)

    def update(self):
        """Updated the value by reading it from the backend `KVStore`"""
        self._value = self._store.get(self.name)


def stateful_value(name: str, instance_ref: Optional[str] = None) -> StatefulValue:
    """Create a stateful value instance

    Args:
        name: Name of stateful value
        instance_ref: Optional reference to instance of stateful value

    Returns:
        Stateful value instance

    Example:

        Example task implementation using stateful values::

        ```python
        @task()
        def process_file(fname: str, f_last_updated: datetime):

            last_processed: datetime = stateful_value("last_updated", fname)

            if last_processed.value and f_last_updated > last_processed:
                ... # process file

                # Remember to update task state with new timestamp
                last_processed.value = f_last_updated
        ```
    """
    if instance_ref:
        name = f"{name}__{instance_ref[:64]}"

    return StatefulValue(name)
