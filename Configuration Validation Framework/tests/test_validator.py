import unittest

from validators import (
    ConfigValidator,
    RequiredRule,
    DataTypeRule,
    EmailRule,
    IPAddressRule,
    PortRangeRule,
    StringLengthRule,
    AllowedValuesRule
)


class TestConfigValidator(unittest.TestCase):

    def setUp(self):
        self.validator = ConfigValidator()

        self.validator.add_rules(
            "username",
            RequiredRule(),
            DataTypeRule(str),
            StringLengthRule(3, 20)
        )

        self.validator.add_rules(
            "email",
            RequiredRule(),
            DataTypeRule(str),
            EmailRule()
        )

        self.validator.add_rules(
            "host",
            RequiredRule(),
            DataTypeRule(str),
            IPAddressRule()
        )

        self.validator.add_rules(
            "port",
            RequiredRule(),
            DataTypeRule(int),
            PortRangeRule()
        )

        self.validator.add_rules(
            "timeout",
            RequiredRule(),
            DataTypeRule(int),
            AllowedValuesRule([10, 20, 30, 60])
        )

    def test_valid_configuration(self):
        config = {
            "username": "admin",
            "email": "admin@example.com",
            "host": "192.168.1.1",
            "port": 8080,
            "timeout": 30
        }

        self.assertTrue(self.validator.is_valid(config))

    def test_required_field(self):
        config = {
            "email": "admin@example.com",
            "host": "192.168.1.1",
            "port": 8080,
            "timeout": 30
        }

        errors = self.validator.validate(config)

        self.assertIn("username", errors)

    def test_invalid_email(self):
        config = {
            "username": "admin",
            "email": "invalid",
            "host": "192.168.1.1",
            "port": 8080,
            "timeout": 30
        }

        errors = self.validator.validate(config)

        self.assertIn("email", errors)

    def test_invalid_ip(self):
        config = {
            "username": "admin",
            "email": "admin@example.com",
            "host": "999.999.999.999",
            "port": 8080,
            "timeout": 30
        }

        errors = self.validator.validate(config)

        self.assertIn("host", errors)

    def test_invalid_port(self):
        config = {
            "username": "admin",
            "email": "admin@example.com",
            "host": "192.168.1.1",
            "port": 70000,
            "timeout": 30
        }

        errors = self.validator.validate(config)

        self.assertIn("port", errors)

    def test_invalid_timeout(self):
        config = {
            "username": "admin",
            "email": "admin@example.com",
            "host": "192.168.1.1",
            "port": 8080,
            "timeout": 100
        }

        errors = self.validator.validate(config)

        self.assertIn("timeout", errors)


if __name__ == "__main__":
    unittest.main()