from django.core.exceptions import ValidationError


def validate_require(field_name, val):
    if val is None or len(val) == 0:
        params = {}
        params[field_name] = f"{field_name} is empty or None"
        raise ValidationError("%(field)s is required", params=params)
