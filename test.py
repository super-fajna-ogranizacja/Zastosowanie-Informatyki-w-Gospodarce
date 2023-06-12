"""  File contains testing data and methods for discussion.py file
"""

import unittest

import discussion


class PrepareTestJSON:
    """Returns different json for testing purposes"""

    @staticmethod
    def get_correct_json():
        """Returns correct discussion dict

        Returns
        -------
        dict
            Correct dictionary
        """
        return {
            "title": "TinyNvidiaUpdateChecker",
            "body": "### Description\n\ncheck for NVIDIA GPU driver updates\n\n### URLs\n\nhttps://github.com/ElPumpo/TinyNvidiaUpdateChecker\n\n### Types\n\n- [ ] CLI\n- [ ] TUI\n- [X] GUI\n- [ ] webapp\n- [ ] library\n- [ ] framework\n\n### Platforms\n\n- [ ] Linux\n- [X] Windows\n- [ ] MacOS\n- [ ] iOS\n- [ ] Android\n- [ ] Web\n\n### Categories\n\nUsing now and then\n\n### \n---\n\nUsed once, I think and looked OK. Lists [EnvyUpdate](https://github.com/fyr77/EnvyUpdate) and [nvidia-update](https://github.com/ZenitH-AT/nvidia-update) as alternatives",  # noqa E501
            "author": {"login": "XYZ"},
            "number": 22,
        }

    @staticmethod
    def get_incorrect_body_json():
        """Returns JSON with incorrect body

        Returns
        -------
        str
            Incorrect JSON
        """
        return {
            "title": "TinyNvidiaUpdateChecker",
            "body": "### Types\n\n- [ ] CLI",
            "author": {"login": "XYZ"},
            "number": 22,
        }

    @staticmethod
    def get_missing_title_json():
        """Returns JSON without title

        Returns
        -------
        str
            Incorrect JSON
        """
        return {
            "body": "### Description\n\ncheck for NVIDIA GPU driver updates\n\n### URLs\n\nhttps://github.com/ElPumpo/TinyNvidiaUpdateChecker\n\n### Types\n\n- [ ] CLI\n- [ ] TUI\n- [X] GUI\n- [ ] webapp\n- [ ] library\n- [ ] framework\n\n### Platforms\n\n- [ ] Linux\n- [X] Windows\n- [ ] MacOS\n- [ ] iOS\n- [ ] Android\n- [ ] Web\n\n### Categories\n\nUsing now and then\n\n### \n---\n\nUsed once, I think and looked OK. Lists [EnvyUpdate](https://github.com/fyr77/EnvyUpdate) and [nvidia-update](https://github.com/ZenitH-AT/nvidia-update) as alternatives",  # noqa E501
            "author": {"login": "XYZ"},
            "number": 22,
        }

    @staticmethod
    def get_missing_desc_json():
        """Returns JSON without description

        Returns
        -------
        str
            Incorrect JSON
        """
        return {
            "title": "TinyNvidiaUpdateChecker",
            "body": "### URLs\n\nhttps://github.com/ElPumpo/TinyNvidiaUpdateChecker\n\n### Types\n\n- [ ] CLI\n- [ ] TUI\n- [X] GUI\n- [ ] webapp\n- [ ] library\n- [ ] framework\n\n### Platforms\n\n- [ ] Linux\n- [X] Windows\n- [ ] MacOS\n- [ ] iOS\n- [ ] Android\n- [ ] Web\n\n### Categories\n\nUsing now and then\n\n### \n---\n\nUsed once, I think and looked OK. Lists [EnvyUpdate](https://github.com/fyr77/EnvyUpdate) and [nvidia-update](https://github.com/ZenitH-AT/nvidia-update) as alternatives",  # noqa E501
            "author": {"login": "XYZ"},
            "number": 22,
        }

    @staticmethod
    def get_missing_categories_json():
        """Returns JSON without categories info

        Returns
        -------
        str
            Incorrect JSON
        """
        return {
            "title": "TinyNvidiaUpdateChecker",
            "body": "### Description\n\ncheck for NVIDIA GPU driver updates\n\n### URLs\n\nhttps://github.com/ElPumpo/TinyNvidiaUpdateChecker\n\n### Types\n\n- [ ] CLI\n- [ ] TUI\n- [X] GUI\n- [ ] webapp\n- [ ] library\n- [ ] framework\n\n",  # noqa E501
            "author": {"login": "XYZ"},
            "number": 22,
        }

    @staticmethod
    def get_missing_types_json():
        """Returns JSON without types info

        Returns
        -------
        str
            Incorrect JSON
        """
        return {
            "title": "TinyNvidiaUpdateChecker",
            "body": "### Description\n\ncheck for NVIDIA GPU driver updates\n\n### URLs\n\nhttps://github.com/ElPumpo/TinyNvidiaUpdateChecker\n\n### Platforms\n\n- [ ] Linux\n- [X] Windows\n- [ ] MacOS\n- [ ] iOS\n- [ ] Android\n- [ ] Web\n\n### Categories\n\nUsing now and then\n\n### \n---\n\nUsed once, I think and looked OK. Lists [EnvyUpdate](https://github.com/fyr77/EnvyUpdate) and [nvidia-update](https://github.com/ZenitH-AT/nvidia-update) as alternatives",  # noqa E501
            "author": {"login": "XYZ"},
            "number": 22,
        }

    @staticmethod
    def get_missing_platforms_json():
        """Returns JSON without platfrom info

        Returns
        -------
        str
            Incorrect JSON
        """
        return {
            "title": "TinyNvidiaUpdateChecker",
            "body": "### Description\n\ncheck for NVIDIA GPU driver updates\n\n### URLs\n\nhttps://github.com/ElPumpo/TinyNvidiaUpdateChecker\n\n### Types\n\n- [ ] CLI\n- [ ] TUI\n- [X] GUI\n- [ ] webapp\n- [ ] library\n- [ ] framework\n\n### Platforms\n\n- [ ] Linux\n- [X] Windows\n- [ ] MacOS\n- [ ] iOS\n- [ ] Android\n- [ ] Web\n\n### \n---\n\nUsed once, I think and looked OK. Lists [EnvyUpdate](https://github.com/fyr77/EnvyUpdate) and [nvidia-update](https://github.com/ZenitH-AT/nvidia-update) as alternatives",  # noqa E501
            "author": {"login": "XYZ"},
            "number": 22,
        }

    @staticmethod
    def get_missing_comment_json():
        """Returns JSON without comment

        Returns
        -------
        str
            Incorrect JSON
        """
        return {
            "title": "TinyNvidiaUpdateChecker",
            "body": "### Description\n\ncheck for NVIDIA GPU driver updates\n\n### URLs\n\nhttps://github.com/ElPumpo/TinyNvidiaUpdateChecker\n\n### Types\n\n- [ ] CLI\n- [ ] TUI\n- [X] GUI\n- [ ] webapp\n- [ ] library\n- [ ] framework\n\n### Platforms\n\n- [ ] Linux\n- [X] Windows\n- [ ] MacOS\n- [ ] iOS\n- [ ] Android\n- [ ] Web\n\n### Categories\n\nUsing now and then\n\n### \n",  # noqa E501
            "author": {"login": "XYZ"},
            "number": 22,
        }

    @staticmethod
    def get_incorrect_json():
        """Returns incorrect JSON

        Returns
        -------
        str
            Incorrect JSON
        """
        return r"""
        data:
            "repository":
            "discussions":
                "nodes":
                    "title": "TinyNvidiaUpdateChecker",
                    "body": "### Description\n\ncheck for NVIDIA GPU driver updates\n\n### URLs\n\nhttps://github.com/ElPumpo/TinyNvidiaUpdateChecker\n\n### Types\n\n- [ ] CLI\n- [ ] TUI\n- [X] GUI\n- [ ] webapp\n- [ ] library\n- [ ] framework\n\n### Platforms\n\n- [ ] Linux\n- [X] Windows\n- [ ] MacOS\n- [ ] iOS\n- [ ] Android\n- [ ] Web\n\n### Categories\n\nUsing now and then\n\n### \n", # noqa E501
                    "author":
                    "login": "XYZ"
                "totalCount": 1
        """


class TestDiscussion(unittest.TestCase):
    """Class containing testing methods"""

    def test_correct_json(self):
        """Tests if correct json contains right informations"""
        apps = discussion.parse_discussions([PrepareTestJSON.get_correct_json()])
        self.assertEqual(apps[0].name, "TinyNvidiaUpdateChecker")
        self.assertEqual(apps[0].description, "check for NVIDIA GPU driver updates")
        self.assertEqual(
            apps[0].urls,
            ["https://github.com/ElPumpo/TinyNvidiaUpdateChecker"],
        )
        self.assertEqual(apps[0].types, ["GUI"])
        self.assertEqual(apps[0].platforms, ["Windows"])
        self.assertEqual(apps[0].categories, "Using now and then")
        self.assertEqual(
            apps[0].comments,
            # pylint: disable=C0301
            "Used once, I think and looked OK. Lists [EnvyUpdate](https://github.com/fyr77/EnvyUpdate) and [nvidia-update](https://github.com/ZenitH-AT/nvidia-update) as alternatives",  # noqa E501
            # pylint: enable=C0301
        )

    def test_wrong_body_json(self):
        """Tests if incorrect json results in not creating any objects"""
        apps = discussion.parse_discussions([PrepareTestJSON.get_incorrect_body_json()])
        self.assertEqual(apps, [])

    def test_missing_title_json(self):
        """Tests if incorrect json results in not creating any objects"""
        self.assertRaises(
            KeyError,
            lambda: discussion.parse_discussions(
                [PrepareTestJSON.get_missing_title_json()]
            ),
        )

    def test_missing_categories_json(self):
        """Tests if incorrect json results in not creating any objects"""
        apps = discussion.parse_discussions(
            [PrepareTestJSON.get_missing_categories_json()]
        )
        self.assertEqual(apps, [])

    def test_missing_platforms_json(self):
        """Tests if incorrect json results in not creating any objects"""
        apps = discussion.parse_discussions(
            [PrepareTestJSON.get_missing_platforms_json()]
        )
        self.assertEqual(apps, [])

    def test_missing_types_json(self):
        """Tests if incorrect json results in not creating any objects"""
        apps = discussion.parse_discussions([PrepareTestJSON.get_missing_types_json()])
        self.assertEqual(apps, [])

    def test_missing_desc_json(self):
        """Tests if incorrect json results in not creating any objects"""
        apps = discussion.parse_discussions([PrepareTestJSON.get_missing_desc_json()])
        self.assertEqual(apps, [])

    def test_empty_json(self):
        """Tests if empty serwer response results in throwing an exception"""
        self.assertRaises(Exception, lambda: discussion.parse_discussions([""]))

    def test_incorrect_json(self):
        """Tests if incorrectly formated JSON results in throwing an exception"""
        self.assertRaises(
            Exception,
            lambda: discussion.parse_discussions(
                [PrepareTestJSON.get_incorrect_json()]
            ),
        )


if __name__ == "__main__":
    unittest.main()
