# comment model
from django.db import models
from django.db.models import CASCADE

from todolist.goals.models.dates_model_mixin import DatesModelMixin
from todolist.goals.models.goal import Goal


class Comment(DatesModelMixin):
    goal = models.ForeignKey(
        Goal,
        verbose_name='Цель',
        on_delete=CASCADE
    )
    user = models.ForeignKey(
        'core.User',
        verbose_name='Автор',
        on_delete=models.CASCADE
    )
    text = models.TextField(
        verbose_name='Текст',
        max_length=1000
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'