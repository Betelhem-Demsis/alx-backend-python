#!/usr/bin/env python3
import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient."""

    @parameterized.expand([
        ("google", "google"),
        ("abc", "abc"),
    ])
    @patch("client.get_json")
    def test_org(self, name, org_name, mock_get_json):
        """Test GithubOrgClient.org returns the correct value."""
        mock_get_json.return_value = {"payload": True}
        client = GithubOrgClient(org_name)
        result = client.org
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")
        self.assertEqual(result, {"payload": True})

    @patch("client.GithubOrgClient.org", new_callable=PropertyMock)
    def test_public_repos_url(self, mock_org):
        """Test GithubOrgClient._public_repos_url property."""
        mock_org.return_value = {"repos_url": "https://api.github.com/orgs/test/repos"}
        client = GithubOrgClient("test")
        result = client._public_repos_url
        self.assertEqual(result, "https://api.github.com/orgs/test/repos")

    @patch("client.get_json")
    @patch("client.GithubOrgClient._public_repos_url", new_callable=PropertyMock)
    def test_public_repos(self, mock_repos_url, mock_get_json):
        """Test GithubOrgClient.public_repos method."""
        mock_repos_url.return_value = "https://api.github.com/orgs/test/repos"
        mock_get_json.return_value = [{"name": "repo1"}, {"name": "repo2"}]

        client = GithubOrgClient("test")
        result = client.public_repos

        self.assertEqual(result, ["repo1", "repo2"])
        mock_repos_url.assert_called_once()
        mock_get_json.assert_called_once_with("https://api.github.com/orgs/test/repos")

    @parameterized.expand([
        ("repo_with_license", {"license": {"key": "my_license"}}, "my_license", True),
        ("repo_without_license", {"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, name, repo, license_key, expected):
        """Test GithubOrgClient.has_license method."""
        client = GithubOrgClient("test")
        result = client.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized_class([
    {
        "org_payload": TEST_PAYLOAD,
        "repos_payload": TEST_PAYLOAD,
        "expected_repos": TEST_PAYLOAD,
        "apache2_repos": TEST_PAYLOAD,
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient."""

    @classmethod
    def setUpClass(cls):
        """Set up class for integration tests."""
        cls.get_patcher = patch("requests.get")
        mock_get = cls.get_patcher.start()
        mock_get.side_effect = lambda url: Mock(
            **{"json.return_value": cls.org_payload if "orgs" in url else cls.repos_payload}
        )

    @classmethod
    def tearDownClass(cls):
        """Tear down class after integration tests."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos method with integration."""
        client = GithubOrgClient("test")
        self.assertEqual(client.public_repos, self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos method filtering by license."""
        client = GithubOrgClient("test")
        self.assertEqual(
            client.public_repos(license_key="apache-2.0"), self.apache2_repos
        )


if __name__ == "__main__":
    unittest.main()