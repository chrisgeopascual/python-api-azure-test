from jsonschema import validate, ValidationError

def validate_schema(instance, schema):
    """
    Thin wrapper around jsonschema.validate so tests can assert
    a clean pass/fail instead of catching ValidationError directly.
    Returns True if valid, raises AssertionError with the jsonschema
    error message if not.
    """
    try:
        validate(instance=instance, schema=schema)
        return True
    except ValidationError as e:
        raise AssertionError(f"Schema validation failed: {e.message}")