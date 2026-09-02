from examples.validators import ( 
    ConfigValidator,
    RequiredRule,
    DataTypeRule,
    EmailRule,
    IPAddressRule,
    PortRangeRule,
    StringLengthRule,
    AllowedValuesRule,
    NestedConfigRule
)


database_validator = ConfigValidator()

database_validator.add_rules(
    "host",
    RequiredRule(),
    DataTypeRule(str),
    IPAddressRule()
)

database_validator.add_rules(
    "port",
    RequiredRule(),
    DataTypeRule(int),
    PortRangeRule()
)


config_validator = ConfigValidator()

config_validator.add_rules(
    "username",
    RequiredRule(),
    DataTypeRule(str),
    StringLengthRule(minimum=3, maximum=20)
)

config_validator.add_rules(
    "email",
    RequiredRule(),
    DataTypeRule(str),
    EmailRule()
)

config_validator.add_rules(
    "host",
    RequiredRule(),
    DataTypeRule(str),
    IPAddressRule()
)

config_validator.add_rules(
    "port",
    RequiredRule(),
    DataTypeRule(int),
    PortRangeRule()
)

config_validator.add_rules(
    "timeout",
    RequiredRule(),
    DataTypeRule(int),
    AllowedValuesRule([10, 20, 30, 60])
)

config_validator.add_rules(
    "database",
    RequiredRule(),
    NestedConfigRule(database_validator)
)


config = {
    "username": 123,
    "email": "giteshpawar3516@gmail.com",
    "host": "192.168.1.10",
    "port": 8080,
    "timeout": 30,
    "database": {
        "host": "192.168.1.20",
        "port": 5432
    }
}


errors = config_validator.validate(config)

if errors:
    print("Configuration is INVALID")
    print("Errors:")

    for field, error in errors.items():
        print(f"{field}: {error}")
else:
    print("Configuration is VALID")