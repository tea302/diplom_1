from django.contrib.auth.models import AbstractUser
from django.db.models import TextChoices, CharField


class User(AbstractUser):
    class Sex(TextChoices):
        MALE = "male", "Мужской"
        FEMALE = "female", "Женский"

    sex = CharField(max_length=7, choices=Sex.choices, null=True)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
