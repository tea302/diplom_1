from typing import Type

import factory

from core.models import User
from todolist.goals.models.board import Board, BoardParticipant
from todolist.goals.models.category import GoalCategory
from todolist.goals.models.comment import Comment
from todolist.goals.models.goal import Goal


class AbstractFactory(factory.django.DjangoModelFactory):
    title: factory.Sequence = factory.Sequence(lambda x: f"board_{x}")


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model: Type[User] = User

    username: factory.Faker = factory.Faker('user_name')
    password: factory.Faker = factory.Faker('password')


class BoardFactory(AbstractFactory):
    class Meta:
        model: Type[Board] = Board


class BoardParticipantFactory(factory.django.DjangoModelFactory):
    class Meta:
        model: Type[BoardParticipant] = BoardParticipant

    board: factory.SubFactory = factory.SubFactory(BoardFactory)


class CategoryFactory(AbstractFactory):
    class Meta:
        model: Type[GoalCategory] = GoalCategory

    board: factory.SubFactory = factory.SubFactory(BoardFactory)


class GoalFactory(AbstractFactory):
    class Meta:
        model: Type[Goal] = Goal

    category: factory.SubFactory = factory.SubFactory(CategoryFactory)


class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model: Type[Comment] = Comment

    text: factory.Sequence = factory.Sequence(lambda x: f"testComment_{x}")
    goal: factory.SubFactory = factory.SubFactory(GoalFactory)
