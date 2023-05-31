from pytest_factoryboy import register

from todolist.tests.factories import *

pytest_plugins = 'tests.fixtures'


register(UserFactory)
register(BoardFactory)
register(BoardParticipantFactory)
register(CategoryFactory)
register(GoalFactory)
register(CommentFactory)