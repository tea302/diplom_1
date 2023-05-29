from typing import Tuple

from django.db.models import QuerySet

from todolist.bot.models import TgUser
from todolist.goals.models.board import BoardParticipant
from todolist.goals.models.category import GoalCategory
from todolist.goals.models.goal import Goal


class BotDAO:
    @staticmethod
    def get_or_create_user(message) -> Tuple[TgUser, bool]:
        tg_user, created = TgUser.objects.get_or_create(
            tg_user_id=message.from_.id,
            tg_chat_id=message.chat.id
        )
        return tg_user, created

    @staticmethod
    def get_user_or_exception(message) -> TgUser:
        tg_user: TgUser = TgUser.objects.get(tg_user_id=message.from_.id)
        return tg_user

    @staticmethod
    def get_goals(tg_user) -> QuerySet[Goal]:
        goals: QuerySet[Goal] = Goal.objects.select_related('category').filter(
            category__board__participants__user=tg_user.user,
            category__board__is_deleted=False,
            category__is_deleted=False
        ).exclude(status=Goal.Status.archived)
        return goals

    @staticmethod
    def get_categories(tg_user) -> QuerySet[GoalCategory]:
        categories: QuerySet[GoalCategory] = GoalCategory.objects.select_related('board').filter(
            board__participants__role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer],
            board__participants__user=tg_user.user,
            board__is_deleted=False,
            is_deleted=False
        )
        return categories

    @staticmethod
    def set_category(tg_user, category) -> None:
        category_: GoalCategory = GoalCategory.objects.select_related('board').get(
            board__participants__user=tg_user.user,
            board__is_deleted=False,
            is_deleted=False,
            title__iexact=category
        )
        tg_user.selected_category = category_
        tg_user.save()

    @staticmethod
    def create_goal(tg_user, item) -> tuple[int, int, int]:
        new_goal: Goal = Goal.objects.create(
            user=tg_user.user,
            category=tg_user.selected_category,
            title=item.message.text
        )
        return new_goal.category.board.id, new_goal.category.id, new_goal.id
    