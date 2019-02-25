from PiezoWebApp.src.models.spark_job_argument_classification import ArgumentClassification


def create_object_schema_from_validation_rules(rules_dict):
    all_properties = [
        key for key, rule in rules_dict.items()
        if rule.classification is not ArgumentClassification.Fixed
    ]
    required_properties = [
        key for key, rule in rules_dict.items()
        if rule.classification is ArgumentClassification.Required
    ]
    return create_object_schema_with_string_properties(all_properties, required=required_properties)


def create_object_schema_with_string_properties(list_of_properties, required=None):
    if not list_of_properties:
        raise ValueError("No properties provided for the schema")
    schema = {"type": "object",
              "properties":
                  {property: {"type": "string"} for property in list_of_properties},
              }
    if required:
        schema["required"] = required
    return schema
