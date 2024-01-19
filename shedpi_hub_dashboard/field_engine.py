import dataclasses

from typing import Optional, Callable, Any

"""
Design considerations:
- What about allowing developers to define rules externally?, needs the rule map to be configurable and to allow third party code!
"""


@dataclasses.dataclass
class FieldError:
    field_name: str
    message: str


@dataclasses.dataclass
class ValidationErrors:
    field_errors: list[FieldError]


@dataclasses.dataclass
class FieldEngineValidator:
    errors: Optional[ValidationErrors] = None
    specification: Optional[dict] = None
    field_rules_map: Optional[dict] = None

    def __init__(self, specification):
        self.specification = specification
        #self.errors: FieldErrors = {}
        self.errors = ValidationErrors(
            field_errors=[]
        )
        self.field_rules_map: dict[str, Callable] = {
            "not_null": self.validate_rule_not_null,
            "regex": self.validate_rule_regex,
            #"integer": self._rule_integer,
        }
        # self.default_field_checks_map: dict[str, Callable] = {
        #     "required": self.validate_required,
        #     "type": self.validate_type,
        # }
        # self.dataset_rules_map: dict[str, Callable] = {
        #     "required": self.validate_rule_required,
        # }

        self.required_fields: list = [key for key, field in self.specification["fields"].items() if field.get("required")]

    def process_field_rules(self, field_name: str, field_value: Any):
        """

        :param field_name:
        :param field_value:
        :return:
        """
        rules = self.specification["fields"][field_name].get("rules")

        if not rules:
            return

        for rule in rules:
            rule_type = rule["type"]
            if rule_type in self.field_rules_map:
                self.process_field_rule(rule_type, field_name, field_value)

    def process_field_rule(self, rule_type: str, field_name: str, field_value: Any):
        """

        :param rule_type:
        :param field_name:
        :param field_value:
        :return:
        """
        # TODO: Provide rule config
        if not self.field_rules_map[rule_type](field_value):
            self.errors.field_errors.append(f"Field {field_name} failed rule: {rule_type}")

    def validate_required(self, fields) -> bool:
        """
        Ensure that fields tht are required are present in the dataset

        :param fields:
        :return:
        """
        missing_fields = list[set(self.required_fields) - set(fields)]

        if missing_fields:
            self.errors.field_errors.append(f"Fields {missing_fields} are missing")
            return True
        return False

    def validate_data(self, data: dict) -> None:
        """

        :param data:
        :return:
        """

        for row in data:
            fields: list = row.keys()

            # Row rules
            self.validate_required(fields)

            for field_name in fields:

                # TODO: Field Type checks!

                # Field rules
                if field_name in self.specification["fields"]:
                    self.process_field_rules(field_name=field_name, field_value=row[field_name])

    def validate_rule_required(self, row):
        """
        Takes a dict, neends ot map the field to the ict

        Potentially want to compile rules per field, then for each field found run checks

        :param row:
        :return:
        """
        pass
        # if rule not in row:
        #     error = FieldError(
        #             fieldname=fieldname,
        #             message=f"Field {fieldname} is required but missing"
        #         )
        #     self.errors.field_errors.append(
        #         error
        #     )

    def validate_rule_not_null(self, field_value) -> bool:
        return bool(field_value)

    def validate_rule_regex(self, entry):
        pass


class FieldEngine:
    validator: Optional[FieldEngineValidator] = None

    def __init__(self, specifiction: dict) -> None:

        # FIXME: Allow the validator to be provided per "model" to allow third parties to provide their own config
        self.validator = FieldEngineValidator(specifiction)

    def validate(self, data):
        self.validator.validate_data(data)
