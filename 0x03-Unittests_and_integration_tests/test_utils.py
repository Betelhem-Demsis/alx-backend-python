#!/usr/bin/env python3
"""
Unit tests for the utility functions in the 'utils' module.

"""

from utils import (access_nested_map, get_json, memoize)
import requests
from parameterized import parameterized
import unittest
from unittest.mock import patch


class TestMemoize(unittest.TestCase):
    """ Class Tests Memoize """

    def test_memoize(self):
        """ test momorize func"""

        class TestClass:
            """wrapps with momorize """

            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with patch.object(TestClass, 'a_method') as mock:
            test_class = TestClass()
            test_class.a_property()

            test_class.a_property()
            mock.assert_called_once()


class TestAccessNestedMap(unittest.TestCase):
    """ For testing access nested map """

    @parameterized.expand([
        ({"a": 1}, ("a",), 1), ({"a": {"b": 2}}, ("a",), {'b': 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """ tests nested map """
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), 'a'), ({"a": 1}, ("a", "b"), 'b')
    ])
    def test_access_nested_map_exception(self, nested_map, path, expected):
        """ raises key error"""
        with self.assertRaises(KeyError) as e:
            access_nested_map(nested_map, path)
        self.assertEqual(f"KeyError('{expected}')", repr(e.exception))


class TestGetJson(unittest.TestCase):
    """ for testing get json """

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])
    def test_get_json(self, test_url, test_payload):
        """ tests get json"""
        config = {'return_value.json.return_value': test_payload}
        patcher = patch('requests.get', **config)
        mock = patcher.start()

        self.assertEqual(get_json(test_url), test_payload)
        mock.assert_called_once()
        patcher.stop()
        