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
