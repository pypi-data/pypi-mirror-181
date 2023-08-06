from typing import Any, Iterable, Mapping

from .reactive_struct import ElementError, EventEmitter, IReactiveStructure


class rdict(IReactiveStructure[dict]):
	"""
	Dictionary with callback events.

	Provides unordinary methods for items manipulation.
	"""

	def clear(self) -> None:
		for key in self.keys():
			self.remove_key(key)

	def _add(self, key_or_item, item=None) -> tuple[Any, Any]:
		if key_or_item in self.data:
			raise ElementError()
		self.data[key_or_item] = item
		return key_or_item, item

	def _change(self, key, item) -> None:
		if key not in self.data:
			raise ElementError()
		self.data[key] = item

	def _remove_key(self, key) -> tuple[Any, Any]:
		if key not in self.data:
			raise ElementError()
		item = self.data[key]
		del self.data[key]
		return key, item

	def _get(self, key_or_item) -> Any:
		if key_or_item not in self.data:
			raise ElementError()
		return self.data[key_or_item]

	def __init__(self, items: Mapping | Iterable = None, emitter: EventEmitter | None = None):
		if items is None:
			items = {}
		super().__init__(dict, items, emitter)

	def keys(self) -> list:
		return list(self.data.keys())

	def values(self) -> list:
		return list(self.data.values())

	def items(self) -> list:
		return list(self.data.items())
