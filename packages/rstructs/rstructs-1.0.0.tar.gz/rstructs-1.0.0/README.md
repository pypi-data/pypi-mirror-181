# Reactive structures - data structures with events

Provides several data structures with different events such as reactive list or reactive dict.

**Both ordinary and async functions are supported.**

# Example

```python
from rstructs import rlist

subscriptions = rlist()


@subscriptions.added
def on_user_subscribed(index, user):
	if index == 0:
		print(f'The first user {user} has just subscribed! ')
	else:
		print(f'{user} has just subscribed. ')


subscriptions.add('Bob')
subscriptions.add('Alice')

```

> The first user Bob has just subscribed!
>
> Alice has just subscribed.

# How to subscribe to events?

To subscribe to an event just decorate with it event handler.

```python
@subscriptions.added
def on_user_subscribed(index, user):
	...
```

Moreover, a time to handle parameter can be used.

```python
@subscriptions.added(2) # handle only for the first two times
def on_user_subscribed(index, user):
	...
```

# API

## Common predefined events

`constructed(initial_data)` - The structure was constructed and initialized.

`added(key, item)` - Added new item into the structure.

`before_added(key_or_item)` - Just before added new item into the structure.

`filled(key, item)` - The first item was added to the empty structure.

`before_filled(key_or_item)` - Just before the first item was added to the empty structure.

`changed(key, item)` - Changed existing item.

`before_changed(key, item)` - Just before changed existing item.

`updated(key, item)` - Added new item or changed existing one in the structure.

`before_updated(key_or_item)` - Just before added new item or changed existing one in the structure.

`removed(key, item)` - Removed existing item.

`before_removed(key_or_item)` - Just before removed existing item.

`emptied()` - The last item was removed from the structure.

`before_emptied()` - Just before the last item was removed from the structure.

## Additional predefined rlist events

`sorted()` - The list sorted inplace.

`before_sorted()` - Just before the list sorted inplace.

## Common predefined methods

`key_or_item in ...` - Checks whether key or item is contained by data.

`len(...)` - Returns data length.

`iter(...)` - Returns data iterator if available.

`...[key_or_item]` - alias to `get(key_or_item)`.

`...[key] = value` - alias to `update(key, value)`.

`del ...[key]` - alias to remove_key(key).

`add(key)->key, item` or `add(key, item)->key, item` - Add new item into the structure.

`change(key, item)` - Change existing item.

`update(key)` or `update(key, item)` - Add new item or change existing one in the structure. Firstly tries to change item and in case of ElementError adds as a new one.

`remove_key(key)->key, item` - Remove existing item.

`remove_item(item)->key, item` - Remove existing item.

`get(key_or_item, default=None)` - Get existing item. If default value is defined return it when ElementError occurs.

`clear()` - Remove all items from the structure. Derived classes should use remove methods per each item.

`index(item)->key` - Try to get key of item or rise ElementError.

## Additional predefined rlist methods

`sort(*, key=None, reverse=False)` - This method sorts the list in place, using only < comparisons between items. Exceptions are not suppressed - if any comparison operations fail, the entire sort operation will fail (and the list will likely be left in a partially modified state).

`...[key] = value` - alias to `change(key, value)`.

## Additional predefined rdict methods

`keys()->list[keys]` - get list of keys.

`values()->list[values]` - get list of keys.

`items()->list[tuple[key,value]]` - get list of tuples of keys and values.

# How to create your own reactive structure?

To create new reactive class you need to derive from `IReactiveStructure` and implement abstract methods (and optionally override other predefined methods).

# More details

This library is made on top of [eventsystem](https://pypi.org/project/eventsystem).
