import unittest
from utils import msg_parse


class TestMsgParse(unittest.TestCase):

    def setUp(self):
        self.monikers_flat = ["coffee", "coffees", 7]

    def test_mixedOrder(self):
        # Test that mixed order keywords get assigned properly
        message = "/tip hey can u send 1 coffee across to my boy @username please :)"
        parsedMessage = msg_parse(message, self.monikers_flat)
        self.assertEqual(parsedMessage, [
            "/tip",  # bot call
            "username",  # username
            "1",  # amount
            "coffee",  # moniker
            ""  # address
        ])

    def test_numberPlacement(self):
        # Test that function can find the moniker when
        #  it does not come after the digit
        message = "/tip hey can u send some coffee across to my boy @username... 2 cups please :)"
        parsedMessage = msg_parse(message, self.monikers_flat)
        self.assertEqual(parsedMessage, [
            "/tip",  # bot call
            "username",  # username
            "2",  # amount
            "coffee",  # moniker
            ""  # address
        ])

        # Test that function can parse a rounded down
        # integer when a floating point number is passed
        message = "/tip hey can u send some coffee across to my boy @username... 2.99 cups please :)"
        parsedMessage = msg_parse(message, self.monikers_flat)
        self.assertEqual(parsedMessage, [
            "/tip",  # bot call
            "username",  # username
            "2",  # amount
            "coffee",  # moniker
            ""  # address
        ])

    def test_amountSingle(self):
        # Test that function can assign an amount '1' when
        # no amount is specified but moniker present
        message = "/tip yo send coffee to @username"
        parsedMessage = msg_parse(message, self.monikers_flat)
        self.assertEqual(parsedMessage, [
            "/tip",  # bot call
            "username",  # username
            "1",  # amount
            "coffee",  # moniker
            ""  # address
        ])

        # Test that function can assign an amount '1' when
        #  'a or an' amount classifier is used and moniker present
        message = "/tip yo send a cup of coffee to @username"
        parsedMessage = msg_parse(message, self.monikers_flat)
        self.assertEqual(parsedMessage, [
            "/tip",  # bot call
            "username",  # username
            "1",  # amount
            "coffee",  # moniker
            ""  # address
        ])
