# goal model
from django.db import models

from todolist.goals.models.category import GoalCategory
from todolist.goals.models.dates_model_mixin import DatesModelMixin


class Goal(DatesModelMixin):
    class Status(models.IntegerChoices):
        to_do = 1, "К выполнению"
        in_progress = 2, "В процессе"
        done = 3, "Выполнено"
        archived = 4, "Архив"

    class Priority(models.IntegerChoices):
        low = 1, "Низкий"
        medium = 2, "Средний"
        high = 3, "Высокий"
        critical = 4, "Критический"

    user = models.ForeignKey(
        'core.User',
        verbose_name='Автор',
        on_delete=models.PROTECT
    )
    category = models.ForeignKey(
        GoalCategory,
        verbose_name='Категория',
        on_delete=models.PROTECT
    )
    title = models.CharField(
        verbose_name='Название',
        max_length=500
    )
    description = models.TextField(
        verbose_name='Описание',
        max_length=2000,
        blank=True
    )
    status = models.PositiveSmallIntegerField(
        verbose_name='Статус',
        choices=Status.choices,
        default=Status.to_do
    )
    priority = models.PositiveSmallIntegerField(
        verbose_name='Приоритет',
        choices=Priority.choices,
        default=Priority.medium
    )
    due_date = models.DateTimeField(
        verbose_name='Дедлайн',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Цель'
        verbose_name_plural = 'Цели'
