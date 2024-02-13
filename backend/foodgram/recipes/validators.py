from django.core.exceptions import ValidationError


def cooking_time_validator(time):
    if time < 1:
        raise ValidationError("Время готовки должно быть больше 0.")
