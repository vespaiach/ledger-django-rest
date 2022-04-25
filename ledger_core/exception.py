from django.core.exceptions import ValidationError


def throw_validation_error(message, params=None):
    raise ValidationError(message, "validation", params)
