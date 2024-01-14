from django.core.validators import RegexValidator

user_validator = RegexValidator(
    r'^[\w.@+-]+\Z',
    'Поле username не соответствует формату.'
)
