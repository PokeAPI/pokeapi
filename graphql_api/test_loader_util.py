import unittest

from .utils import unbatch, create_batches, batch_fetch
from .loader_key import LoaderKey


class TestObject:
    """An object used for mocking models in tests."""
    def __init__(self, id, other_id):
        self.id = id
        self.other_id = other_id
        self.some_map = TestMap()

    def __eq__(self, other):
        return self.id == other.id

class TestMap:
    def all(self):
        return [TestObject(7, 99), TestObject(8, 99), TestObject(9, 99)]


class UtilTestCase(unittest.TestCase):

    def test_loader_key(self):
        key1 = LoaderKey(id=1, arg1="x")
        key2 = LoaderKey(id=1, arg1="x")
        key3 = LoaderKey(id=1, arg1="y")
        key4 = LoaderKey(id=4, arg1="x")

        self.assertEqual(key1, key2, "LoaderKeys with same ids and same args should be equal")
        self.assertNotEqual(key1, key3)
        self.assertNotEqual(key1, key4)
        self.assertNotEqual(key3, key4)

        self.assertEqual(key1.id, 1)
        self.assertEqual(key1.args, ("x",))
        self.assertEqual(key1.args.arg1, "x")

    def test_unbatch(self):
        keys = [1, 2, 1]
        values = [TestObject(1, "x"), TestObject(2, "x"), TestObject(3, "y")]

        actual = unbatch(keys, values, "id")
        should_be = [TestObject(1, "x"), TestObject(2, "x"), TestObject(1, "x")]
        self.assertEqual(actual, should_be)

        empty_list = unbatch([], [], "id")
        self.assertEqual(empty_list, [])

    def test_create_batches (self):
        keys = [
            LoaderKey(id=1, arg1="x"),
            LoaderKey(id=2, arg1="x"),
            LoaderKey(id=3, arg1="z"),
            LoaderKey(id=1, arg1="z"),
        ]
        should_be = {
            ("x", ): [1, 2],
            ("z", ): [3, 1],
        }
        self.assertEqual(create_batches(keys), should_be)

    def test_batch_fetch(self):
        keys = [
            LoaderKey(id=56, qty=3),
            LoaderKey(id=23, qty=1),
            LoaderKey(id=332, qty=0),
        ]
        actual = batch_fetch(keys, UtilTestCase.get_query_set, "other_id")
        should_be = [
            [TestObject(1, 56), TestObject(2, 56), TestObject(3, 56)],
            [TestObject(1, 23)],
            []
        ]

        self.assertEqual(actual, should_be)

    @staticmethod
    def get_query_set(ids, qty):
        results = []
        for id in ids:
            for i in range(qty):
                results.append(TestObject(id=i + 1, other_id=id))
        return results
