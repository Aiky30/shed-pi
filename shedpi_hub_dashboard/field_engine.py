import dataclasses

from typing import Optional

"""
Design considerations:
- What about allowing developers to define rules externally?, needs the rule map to be configurable and to allow third party code!
"""


@dataclasses
class FieldError:
    field_name: str
    message: str


@dataclasses
class FieldErrors:
    field_errors: list[FieldError]


class FieldEngineValidator:
    errors: FieldErrors = None
    rules: Optional[dict] = None
    field_rules_map: Optional[dict] = None

    def __init__(self, rules):
        self.rules = rules
        self.errors = FieldErrors()
        self.field_rules_map = {
            "not_null": self.validate_rule_not_null,
            "required": self.validate_rule_required,
            "regex": self.validate_rule_regex,
            #"integer": self._rule_integer,
        }

    def validate_data(self, rules: dict) -> FieldErrors:
        for row in rules:
            self.validate_rule_required(row)
            self.validate_rule_not_null(row)
            self.validate_rule_regex(row)

        return self.errors

    def validate_rule_required(self, fieldname, row):
        if fieldname not in row:
            self.errors.field_errors.append(
                FieldError(
                    fieldname=fieldname,
                    message=f"Field {fieldname} is required but missing"
                )
            )

    def validate_rule_not_null(self, entry):
        pass

    def validate_rule_regex(self, entry):
        pass


class FieldEngine:
    errors: Optional[list] = None
    validator: Optional[FieldEngineValidator] = None

    def __init__(self, rules: dict) -> None:

        # FIXME: Allow the validator to be provided per "model" to allow third parties to provide their own config
        self.validator = FieldEngineValidator(rules)

    def validate(self, data):
        self.validator.validate_data(data)
