from django.db import models
from django.db.models import CASCADE

from core.models import User
from todolist.goals.models.category_models import BaseModel
from todolist.goals.models.goal_models import Goal


class GoalComment(BaseModel):
    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    user = models.ForeignKey(User, on_delete=CASCADE, related_name='comments')
    goal = models.ForeignKey(Goal, on_delete=CASCADE, related_name='comments')
    text = models.TextField(verbose_name='Текст', max_length=1000)

    def __str__(self) -> str:
        return self.text
