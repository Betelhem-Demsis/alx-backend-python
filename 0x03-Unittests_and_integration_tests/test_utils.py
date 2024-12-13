#!/usr/bin/env python3
"""
Unit tests for the utility functions in the 'utils' module.

This file contains test cases for functions such as:
- access_nested_map
- get_json
- memoize

Each test case is designed to verify the correct behavior of the respective function.
"""
import unittest
from unittest.mock import patch
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize


# Task 0: Test access_nested_map
class TestAccessNestedMap(unittest.TestCase):
    """
    Test cases for the access_nested_map function.
    """
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test the access_nested_map function for valid inputs."""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),  # Test empty map with invalid path
        ({"a": 1}, ("a", "b"))  # Test missing key 'b' in nested dictionary
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """Test that a KeyError is raised for invalid paths."""
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)

        # Check if the exception message contains the last key in the path
        self.assertEqual(str(context.exception), f"KeyError: {path[-1]}")


# Task 2: Test get_json with mock HTTP calls
class TestGetJson(unittest.TestCase):
    """
    Test cases for the get_json function with mock HTTP calls.
    """
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])
    @patch("requests.get")
    def test_get_json(self, test_url, test_payload, mock_get):
        """
        Test that get_json returns the expected result while mocking HTTP calls.
        """
        mock_get.return_value.json.return_value = test_payload
        result = get_json(test_url)

        # Ensure the mock HTTP request was called exactly once
        mock_get.assert_called_once_with(test_url)

        # Ensure the result matches the expected test payload
        self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """
    Test cases for the memoize decorator.
    """
    def test_memoize(self):
        """
        Test that memoize caches results properly.
        """
        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        test_class = TestClass()

        with patch.object(test_class, 'a_method', return_value=42) as mock_method:
            # First call to a_property should invoke a_method
            self.assertEqual(test_class.a_property, 42)

            # Second call to a_property should use the cached value
            self.assertEqual(test_class.a_property, 42)

            # Ensure a_method was called only once
            mock_method.assert_called_once()


if __name__ == "__main__":
    unittest.main()
