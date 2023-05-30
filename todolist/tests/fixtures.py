from typing import Any

import pytest

from core.models import User
from todolist.tests.factories import UserFactory


@pytest.fixture
def user_auth(client) -> dict[str, Any]:

    user_factory: Any = UserFactory.build()
    client.post(
        '/core/signup',
        {
            'username': user_factory.username,
            'password': user_factory.password,
            'password_repeat': user_factory.password
        }
    )
    user_db: User = User.objects.get(username=user_factory.username)
    response_auth: Any = client.post(
        '/core/login',
        {
            'username': user_factory.username,
            'password': user_factory.password,
        },
        format='json'
    )
    return {
        'user': user_db,
        'auth': response_auth
    }


# ----------------------------------------------------------------
@pytest.fixture
def user_not_auth(client: Any) -> User:

    user_factory: Any = UserFactory.build()
    client.post(
        '/core/signup',
        {
            'username': user_factory.username,
            'password': user_factory.password,
            'password_repeat': user_factory.password
        }
    )
    user_db: User = User.objects.get(username=user_factory.username)
    return user_db
