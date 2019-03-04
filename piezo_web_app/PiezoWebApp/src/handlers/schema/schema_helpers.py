def create_object_schema_from_validation_ruleset(ruleset):
    property_types = ruleset.get_key_type_pairs_allowed_as_input()
    required_properties = ruleset.get_keys_of_required_inputs()
    schema = {"type": "object",
              "properties":
                  {prop_name: {"type": prop_type} for prop_name, prop_type in property_types.items()},
              }
    if required_properties:
        schema["required"] = required_properties
    return schema


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
