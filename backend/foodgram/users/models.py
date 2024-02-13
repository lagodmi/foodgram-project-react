from django.contrib.auth.models import AbstractUser
from django.db import models

from .config import (
    MAX_LEN_NICKNAME,
    MAX_LEN_EMAIL,
    MAX_LEN_NAME,
    MAX_LEN_SURNAME,
    MAX_LEN_PASSWORD,
)
from .validators import user_validator


class User(AbstractUser):
    """
    Модель пользователя.
    """

    username = models.CharField(
        "Логин",
        max_length=MAX_LEN_NICKNAME,
        unique=True,
        validators=(user_validator,)
    )

    email = models.EmailField(
        verbose_name="Электронная почта", max_length=MAX_LEN_EMAIL, unique=True
    )

    first_name = models.CharField(
        verbose_name="Имя пользователя",
        max_length=MAX_LEN_NAME,
    )

    last_name = models.CharField(
        verbose_name="Фамилия пользователя",
        max_length=MAX_LEN_SURNAME,
    )

    password = models.CharField(
        verbose_name="Пароль",
        max_length=MAX_LEN_PASSWORD,
    )

    class Meta:
        ordering = ("username",)
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username


class Follower(models.Model):
    """
    Модель подписки
    """

    user = models.ForeignKey(
        User,
        verbose_name="Пользователь",
        related_name="owner",
        on_delete=models.CASCADE,
    )

    subscriber = models.ForeignKey(
        User,
        verbose_name="Подписчик",
        related_name="subscribers",
        on_delete=models.CASCADE,
    )

    class Meta:
        unique_together = ("user", "subscriber")
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"

    def __str__(self):
        return f"{self.subscriber} подписан на {self.user}"
