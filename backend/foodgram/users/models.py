from django.contrib.auth.models import AbstractUser
from django.db import models

from users.constants_users import (
    MAX_LEN_NICKNAME,
    MAX_LEN_EMAIL,
    MAX_LEN_NAME,
    MAX_LEN_SURNAME,
)
from users.validators import user_validator


class User(AbstractUser):
    """
    Модель пользователя.
    """

    nickname = models.CharField(
        'Логин',
        max_length=MAX_LEN_NICKNAME,
        unique=True,
        validators=(user_validator,)
    )

    email = models.EmailField(
        'Электронная почта',
        max_length=MAX_LEN_EMAIL,
        unique=True
    )

    name = models.CharField(
        'Имя пользователя',
        max_length=MAX_LEN_NAME,
    )

    surname = models.CharField(
        'Фамилия пользователя',
        max_length=MAX_LEN_SURNAME,
    )

    class Meta:
        ordering = ('nickname',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.nickname


# from django.core.validators import validate_slug
# from django.core.exceptions import ValidationError
#     nickname = models.CharField(
#         'Логин',
#         max_length=constants_users.MAX_LEN_NICKNAME,
#         unique=True,
#     )

#     def clean(self):
#         super().clean()
#         try:
#             validate_slug(self.nickname)
#         except ValidationError:
#             raise ValidationError({'nickname': 'Логин содержит недопустимые символы'})
