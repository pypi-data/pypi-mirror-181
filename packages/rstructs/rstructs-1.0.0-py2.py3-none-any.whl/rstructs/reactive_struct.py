from abc import ABC, abstractmethod
from functools import wraps
from typing import Any, Self, TypeVar, Generic, Iterable, MutableSequence

from eventsystem import EventDispatcher, event, EventEmitter

T = TypeVar('T')


class ElementError(KeyError):
	"""Can be risen by reactive structures to signal key, index or item error."""
	pass


class IReactiveStructure(Generic[T], ABC, EventDispatcher):
	"""
	Base class for reactive structures. Provides predefined events and abstract methods to implement.

	Derived classes can also override __contains__, __len__ and __iter__ special methods.
	"""

	def __init__(self, constructor: T, initial_data=None, emitter: EventEmitter | None = None, **kwargs):
		super().__init__(emitter=emitter)
		self.data: T = constructor(initial_data, **kwargs)
		self.constructed.trigger(initial_data)

	@event
	def constructed(self, initial_data) -> None:
		"""
		The structure was constructed and initialized.
		:param initial_data: Initial data.
		"""
		...

	def __contains__(self, key_or_item) -> bool:
		"""Checks whether key or item is contained by data."""
		return key_or_item in self.data

	def __len__(self) -> int:
		"""Returns data length."""
		return len(self.data)

	def __iter__(self):
		"""Returns data iterator if available."""
		return iter(self.data)

	def __getitem__(self, key_or_item):
		return self.get(key_or_item)

	def __setitem__(self, key, value):
		return self.update(key, value)

	def __delitem__(self, key):
		return self.remove_key(key)

	def __str__(self):
		return str(self.data)

	def __repr__(self):
		return repr(self.data)

	@property
	def empty(self) -> bool:
		"""Whether the structure has no items."""
		return not len(self)

	@event
	def added(self, key, item) -> None:
		"""Added new item into the structure."""
		...

	@event
	def before_added(self, key_or_item) -> None:
		"""Just before added new item into the structure."""
		...

	@event
	def filled(self, key, item) -> None:
		"""The first item was added to the empty structure."""
		...

	@event
	def before_filled(self, key_or_item) -> None:
		"""Just before the first item was added to the empty structure."""
		...

	def add(self, key_or_item, item=None) -> tuple[Any, Any]:
		"""
		Add new item into the structure.

		Returns key, item pair.
		"""
		was_empty = self.empty
		if was_empty:
			self.before_filled.trigger(key_or_item)
		self.before_added.trigger(key_or_item)
		key, item = self._add(key_or_item, item)
		self.added.trigger(key, item)
		if was_empty:
			self.filled.trigger(key, item)
		return key, item

	@abstractmethod
	def _add(self, key_or_item, item=None) -> tuple[Any, Any]:
		"""
		Add new item into the structure. Must return key, item pair.

		Can accept sequence of key, item or just new item.

		Derived classes should perform validation and optionally rise ElementError.
		"""
		...

	@event
	def changed(self, key, item) -> None:
		"""Changed existing item."""
		...

	@event
	def before_changed(self, key, item) -> None:
		"""Just before changed existing item."""
		...

	def change(self, key, item) -> None:
		"""Change existing item."""
		self.before_changed.trigger(key, item)
		self._change(key, item)
		self.changed.trigger(key, item)

	@abstractmethod
	def _change(self, key, item) -> None:
		"""
		Change existing item in the structure.

		Derived classes should perform validation and optionally rise ElementError.
		"""
		...

	@event
	def updated(self, key, item) -> None:
		"""Added new item or changed existing one in the structure."""
		...

	@event
	def before_updated(self, key_or_item) -> None:
		"""Just before added new item or changed existing one in the structure."""
		...

	def update(self, key_or_item, item=None) -> None:
		"""
		Add new item or change existing one in the structure.

		Firstly tries to change item and in case of ElementError adds as a new one.
		"""
		self.before_updated.trigger(key_or_item)
		try:
			self.change(key_or_item, item)
		except ElementError:
			key_or_item, item = self.add(key_or_item, item)
		self.updated.trigger(key_or_item, item)

	@event
	def removed(self, key, item) -> None:
		"""Removed existing item."""
		...

	@event
	def before_removed(self, key_or_item) -> None:
		"""Just before removed existing item."""
		...

	@event
	def emptied(self) -> None:
		"""The last item was removed from the structure."""
		...

	@event
	def before_emptied(self) -> None:
		"""Just before the last item was removed from the structure."""
		...

	def remove_key(self, key) -> tuple[Any, Any]:
		"""
		Remove existing item.

		Returns key, item pair.
		"""
		return self.__remove(key, True)

	def remove_item(self, item) -> tuple[Any, Any]:
		"""
		Remove existing item.

		Returns key, item pair.
		"""
		return self.__remove(item, False)

	def __remove(self, key_or_item, by_key: bool) -> tuple[Any, Any]:
		if len(self) == 1:
			self.before_emptied.trigger()
		self.before_removed.trigger(key_or_item)
		if by_key:
			key, item = self._remove_key(key_or_item)
		else:
			key, item = self._remove_item(key_or_item)
		self.removed.trigger(key, item)
		if self.empty:
			self.emptied.trigger()
		return key, item

	@abstractmethod
	def _remove_key(self, key) -> tuple[Any, Any]:
		"""
		Remove existing item from the structure by key.

		Must return key, item pair of removed item.

		Derived classes should perform validation and optionally rise ElementError.
		"""
		...

	def _remove_item(self, item) -> tuple[Any, Any]:
		"""
		Remove existing item from the structure by item value.

		Must return key, item pair of removed item.

		Derived classes should perform validation and optionally rise ElementError.

		By default, uses index method to find key of the item.
		"""
		return self._remove_key(self.index(item))

	def get(self, key_or_item, default=None) -> Any:
		"""
		Get existing item.

		If default value is defined return it when ElementError occurs.
		"""
		try:
			return self._get(key_or_item)
		except ElementError:
			if default is not None:
				return default
			raise

	@abstractmethod
	def clear(self) -> None:
		"""
		Remove all items from the structure.

		Derived classes should use remove methods per each item.
		"""
		...

	@abstractmethod
	def _get(self, key_or_item) -> Any:
		"""
		Get existing item.

		Derived classes should perform validation and optionally rise ElementError.
		"""
		...

	def index(self, item) -> Any:
		"""
		Try to get key of item or rise ElementError.
		"""
		try:
			return self.data.index(item)
		except AttributeError:
			try:
				return self.__get_key_of_mapping_item(item)
			except ElementError:
				try:
					return self.__get_key_of_sequence_item(item)
				except ElementError:
					pass
				except Exception as e:
					raise ElementError() from e
			except Exception as e:
				raise ElementError() from e
		except Exception as e:
			raise ElementError() from e

	def __get_key_of_mapping_item(self, item) -> Any:
		try:
			it = iter(self)
		except TypeError:
			raise ElementError()
		else:
			for key in it:
				if self.get(key) is item:
					return key

	def __get_key_of_sequence_item(self, item) -> Any:
		for index in range(len(self)):
			if self.get(index) is item:
				return index
		raise ElementError()
