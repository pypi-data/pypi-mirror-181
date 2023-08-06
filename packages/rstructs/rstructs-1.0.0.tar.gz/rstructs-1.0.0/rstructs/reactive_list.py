from typing import Any, Iterable

from eventsystem import event

from .reactive_struct import ElementError, EventEmitter, IReactiveStructure


class rlist(IReactiveStructure[list]):
	"""
	List with callback events.

	Provides unordinary methods for items manipulation.
	"""

	def clear(self) -> None:
		while not self.empty:
			self.remove_key(0)

	def _add(self, key_or_item, item=None) -> tuple[Any, Any]:
		index = len(self.data)
		self.data.append(key_or_item)
		return index, key_or_item

	def _change(self, key, item) -> None:
		try:
			self.data[key] = item
		except IndexError as e:
			raise ElementError from e

	def _remove_key(self, key) -> tuple[Any, Any]:
		try:
			item = self.data[key]
			del self.data[key]
			return key, item
		except IndexError as e:
			raise ElementError from e

	def _get(self, key_or_item) -> Any:
		try:
			return self.data[key_or_item]
		except IndexError as e:
			raise ElementError from e

	def __init__(self, items: Iterable = None, emitter: EventEmitter | None = None):
		if items is None:
			items = []
		super().__init__(list, items, emitter)

	@event
	def sorted(self) -> None:
		"""
		The list sorted inplace.
		"""
		...

	@event
	def before_sorted(self) -> None:
		"""
		Just before the list sorted inplace.
		"""
		...

	def sort(self, *, key=None, reverse=False) -> None:
		"""
		This method sorts the list in place, using only < comparisons between items. Exceptions are not suppressed - if any comparison operations fail, the entire sort operation will fail (and the list will likely be left in a partially modified state).

		:param key: specifies a function of one argument that is used to extract a comparison key from each list element (for example, key=str.lower). The key corresponding to each item in the list is calculated once and then used for the entire sorting process. The default value of None means that list items are sorted directly without calculating a separate key value.
		:param reverse: is a boolean value. If set to True, then the list elements are sorted as if each comparison were reversed.
		"""
		self.before_sorted.trigger()
		self.data.sort(key=key, reverse=reverse)
		self.sorted.trigger()

	def __setitem__(self, key, value):
		return self.change(key, value)
