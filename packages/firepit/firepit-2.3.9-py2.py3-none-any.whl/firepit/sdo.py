IDENTITY_SCHEMA = {
    "id": "TEXT UNIQUE",
    "identity_class": "TEXT",
    "name": "TEXT",
    "created": "TEXT",
    "modified": "TEXT"
}

OBSERVED_DATA_SCHEMA = {
    "id": "TEXT UNIQUE",
    "created_by_ref": "TEXT",
    "created": "TEXT",
    "modified": "TEXT",
    "first_observed": "TEXT",
    "last_observed": "TEXT",
    "number_observed": "INTEGER"
}
