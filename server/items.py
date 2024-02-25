#!/usr/bin/env python3

class Item(object):
    def __init__(self, name, **kwargs):
        self._param_list = ['name']
        self.name = name
        for key, value in kwargs.items():
            setattr(self, key, value)
            self._param_list.append(key)

    def serialize(self):
        params = {}
        for key in self._param_list:
            params[key] = getattr(self, key)
        return params

    def contains(self, **kwargs):
        params_left = len(kwargs.keys())
        if params_left > 0:
            for key, value in kwargs.items():
                if getattr(self, key, None) == value:
                    params_left -= 1
            return not bool(params_left)
        return True


class ItemStore(object):
    _items = []

    def _exists(self, name, ret_item=False):
        for index, item in enumerate(self._items):
            if item.name == name:
                if ret_item:
                    return True, item
                return True, index
        return False, -1

    def _filter(self, **kwargs):
        filtered = []
        for item in self._items:
            if item.contains(**kwargs):
                filtered.append(item)
        return filtered

    def list_items(self, **kwargs):
        return self._filter(**kwargs)

    def add_item(self, **kwargs):
        name = kwargs.pop('name', None)
        if not name:
            return False, {'error': 'Name required!'}
        exists, index = self._exists(name)
        if exists:
            return False, {'error': f'Duplicate name: {name}'}
        item = Item(name, **kwargs)
        self._items.append(item)
        return True, item.serialize()

    def del_item(self, name):
        exists, index = self._exists(name)
        if not exists:
            return False, {'error': f'Item not found: {name}'}
        self._items.pop(index)
        return True, {}

    def get_item(self, name):
        exists, item = self._exists(name, ret_item=True)
        if not exists:
            return False, {'error': f'Item not found: {name}'}
        return True, item.serialize()


def initialize_store():
    print('Initializing item store...')
    store = ItemStore()
    for i in range(5):
        print(store.add_item(name=f'item_{i}'))
    return store
