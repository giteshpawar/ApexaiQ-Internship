from abc import ABC, abstractmethod
import re
import ipaddress


class ValidationRule(ABC):

    @abstractmethod
    def validate(self, field, value, config):
        pass


class RequiredRule(ValidationRule):

    def validate(self, field, value, config):
        if value is None or value == "":
            return f"{field} is required"
        return None


class DataTypeRule(ValidationRule):

    def __init__(self, expected_type):
        self.expected_type = expected_type

    def validate(self, field, value, config):
        if value is None:
            return None

        if not isinstance(value, self.expected_type):
            return f"{field} must be of type {self.expected_type.__name__}"

        return None


class EmailRule(ValidationRule):

    def validate(self, field, value, config):
        if value is None or value == "":
            return None

        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

        if not re.match(pattern, value):
            return f"{field} must be a valid email address"

        return None


class IPAddressRule(ValidationRule):

    def validate(self, field, value, config):
        if value is None or value == "":
            return None

        try:
            ipaddress.ip_address(value)
        except ValueError:
            return f"{field} must be a valid IP address"

        return None


class PortRangeRule(ValidationRule):

    def __init__(self, minimum=1, maximum=65535):
        self.minimum = minimum
        self.maximum = maximum

    def validate(self, field, value, config):
        if value is None:
            return None

        if not isinstance(value, int) or isinstance(value, bool):
            return f"{field} must be an integer"

        if not self.minimum <= value <= self.maximum:
            return f"{field} must be between {self.minimum} and {self.maximum}"

        return None


class StringLengthRule(ValidationRule):

    def __init__(self, minimum=None, maximum=None):
        self.minimum = minimum
        self.maximum = maximum

    def validate(self, field, value, config):
        if value is None:
            return None

        if not isinstance(value, str):
            return f"{field} must be a string"

        if self.minimum is not None and len(value) < self.minimum:
            return f"{field} must contain at least {self.minimum} characters"

        if self.maximum is not None and len(value) > self.maximum:
            return f"{field} must contain at most {self.maximum} characters"

        return None


class AllowedValuesRule(ValidationRule):

    def __init__(self, allowed_values):
        self.allowed_values = allowed_values

    def validate(self, field, value, config):
        if value is None:
            return None

        if value not in self.allowed_values:
            return f"{field} must be one of {self.allowed_values}"

        return None


class NestedConfigRule(ValidationRule):

    def __init__(self, validator):
        self.validator = validator

    def validate(self, field, value, config):
        if value is None:
            return None

        if not isinstance(value, dict):
            return f"{field} must be a dictionary"

        errors = self.validator.validate(value)

        if errors:
            return errors

        return None


class ConfigValidator:

    def __init__(self):
        self.rules = {}

    def add_rule(self, field, rule):
        if field not in self.rules:
            self.rules[field] = []

        self.rules[field].append(rule)

    def add_rules(self, field, *rules):
        for rule in rules:
            self.add_rule(field, rule)

    def validate(self, config):
        errors = {}

        for field, rules in self.rules.items():
            value = config.get(field)

            for rule in rules:
                error = rule.validate(field, value, config)

                if error is not None:
                    errors[field] = error
                    break

        return errors

    def is_valid(self, config):
        return len(self.validate(config)) == 0