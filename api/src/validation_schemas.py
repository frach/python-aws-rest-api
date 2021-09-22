ITEM_POST_INPUT_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "http://example.com/example.json",
    "type": "object",
    "additionalProperties": False,
    "required": ["name"],
    "properties": {
        "name": {
            "$id": "#/properties/name",
            "type": "string",
            "title": "The human-friendly name of the item.",
            "pattern": "^[A-Za-z\\s]*$",
            "minLength": 1,
            "maxLength": 30,
        },
        "optional_attr": {
            "$id": "#/properties/optional_attr",
            "type": "string",
            "title": "Some optional string parameter",
            "examples": ["optional_value"],
            "minLength": 0,
            "maxLength": 100,
        }
    },
}

ITEM_PUT_INPUT_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "http://example.com/example.json",
    "type": "object",
    "additionalProperties": False,
    "required": [],
    "properties": {
        "optional_attr": {
            "$id": "#/properties/optional_attr",
            "type": "string",
            "title": "Some optional parameter",
            "minLength": 0,
            "maxLength": 100,
        }
    },
}
