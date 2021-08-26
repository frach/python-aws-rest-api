ITEM_POST_INPUT_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "http://example.com/example.json",
    "type": "object",
    "examples": [{"name": "item_name_1"}],
    "required": ["name"],
    "properties": {
        "name": {
            "$id": "#/properties/name",
            "type": "string",
            "title": "The name of the item",
            "examples": ["item_name_1"],
            "maxLength": 100,
        },
    },
}