from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from typing import List


class CacheRouter:
    """

    description: A client to control all database cache CRUD operations
    references: https://docs.djangoproject.com/en/3.2/topics/cache/

    """

    def __init__(self):
        self.connection = cache

    def find_one(self, key):
        """All cache read operations go to the replica"""
        value = self.connection.get(key)

        print(f'Value for {key} is {value}')
        return value

    def find_or_create(self, key: str, default: [dict, str, list] = 'Blank') -> str:
        """All cache read operations go to the replica"""
        return self.connection.get_or_set(key, default, timeout=DEFAULT_TIMEOUT)

    def create(self, key, value):
        """All cache write operations go to primary"""
        return self.connection.set(key, value)

    def create_many(self, key_array: dict) -> dict:
        """All cache write operations go to primary"""
        return self.connection.set_many(key_array)

    def find_many(self, key_array: list) -> dict:
        """All cache write operations go to primary"""
        return self.connection.get_many(key_array)
