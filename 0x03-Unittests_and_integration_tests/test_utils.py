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
from unittest.mock import patch, Mock
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """Unit tests for access_nested_map function."""

    @parameterized.expand([
        ("single_key", {"a": 1}, ("a",), 1),
        ("nested_key", {"a": {"b": 2}}, ("a",), {"b": 2}),
        ("deep_nested_key", {"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, name, nested_map, path, expected):
        """Test access_nested_map with various inputs."""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ("empty_map", {}, ("a",)),
        ("missing_nested_key", {"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, name, nested_map, path):
        """Test access_nested_map raises KeyError with expected message."""
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)
        # The exception message should match the last part of the path
        self.assertEqual(str(cm.exception).strip("'"), str(path[-1]))


class TestGetJson(unittest.TestCase):
    """Unit tests for get_json function."""

    @parameterized.expand([
        ("example_com", "http://example.com", {"payload": True}),
        ("holberton_io", "http://holberton.io", {"payload": False}),
    ])
    @patch("utils.requests.get")
    def test_get_json(self, name, test_url, test_payload, mock_get):
        """Test get_json returns expected output and calls requests.get once."""
        
        # Create a mock response object
        mock_response = Mock()
        # Mock the .json() method to return the test_payload
        mock_response.json.return_value = test_payload
        # Set the mock get function to return the mock_response
        mock_get.return_value = mock_response

        # Call the get_json function
        result = get_json(test_url)

        # Verify that the requests.get was called once with the test_url
        mock_get.assert_called_once_with(test_url)
        
        # Verify that the result of get_json matches the test_payload
        self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """Unit tests for memoize decorator."""

    def test_memoize(self):
        """Test that memoize caches the result of a_property."""
        class TestClass:
            """Test class to validate memoize behavior."""

            def a_method(self):
                """A sample method that returns a constant value."""
                return 42

            @memoize
            def a_property(self):
                """A property to be memoized."""
                return self.a_method()

        with patch.object(TestClass, "a_method", return_value=42) as mock_method:
            test_instance = TestClass()
            self.assertEqual(test_instance.a_property, 42)
            self.assertEqual(test_instance.a_property, 42)  # Second call should be cached
            mock_method.assert_called_once()  # Ensure a_method was called once


if __name__ == "__main__":
    unittest.main()
