from typing import Any

import pytest
from rest_framework.exceptions import ErrorDetail
from rest_framework.utils.serializer_helpers import ReturnDict

from core.models import User
from core.serializers import UserDetailSerializer
from todolist.goals.models.board import BoardParticipant
from todolist.goals.models.goal import Goal
from todolist.goals.serializers.comment import CommentSerializer
from todolist.tests.factories import BoardParticipantFactory, BoardFactory, CategoryFactory, GoalFactory, CommentFactory


class TestComment:
    @pytest.mark.django_db
    def test_create_comment(self, client: Any, user_auth: dict[str, Any]) -> None:
        board_participant: Any = BoardParticipantFactory.create(
            board=BoardFactory.create(),
            user=user_auth.get('user')
        )
        category: Any = CategoryFactory.create(board=board_participant.board, user=user_auth.get('user'))
        goal: Any = GoalFactory.create(category=category, user=user_auth.get('user'))
        post_response: Any = client.post(
            '/goals/goal_comment/create',
            data={
                "text": "testComment",
                "goal": goal.id
            },
            content_type='application/json',
        )
        expected_response: dict[str, int | str | None] = {
            "id": 1,
            "created": None,
            "updated": None,
            "text": "testComment",
            "goal": goal.id
        }

        assert post_response.status_code == 201, 'Comment was not created successfully'
        assert post_response.data is not None, 'HttpResponseError'
        assert post_response.data.get('text') == expected_response.get('text'), 'Wrong text data'
        assert post_response.data.get('id') == expected_response.get('id'), 'Wrong id'
        assert post_response.data.get('goal') == expected_response.get('goal'), 'Wrong goal expected'

    @pytest.mark.django_db
    def test_create_comment_403(self, client: Any, user_auth: dict[str, Any]) -> None:
        board_participant: Any = BoardParticipantFactory.create(
            board=BoardFactory.create(),
            user=user_auth.get('user'),
            role=BoardParticipant.Role.reader
        )
        category: Any = CategoryFactory.create(board=board_participant.board, user=user_auth.get('user'))
        goal: Any = GoalFactory.create(category=category, user=user_auth.get('user'))
        post_response: Any = client.post(
            '/goals/goal_comment/create',
            data={
                "text": "testComment",
                "goal": goal.id
            },
            content_type='application/json',
        )
        expected_response: dict[str, str] = {
            'detail': 'You are allowed only to read, not to create'
        }

        assert post_response.status_code == 403, 'Comment was created successfully'
        assert post_response.data is not None, 'HttpResponseError'
        assert post_response.data == expected_response

    @pytest.mark.django_db
    def test_create_comment_400(self, client: Any, user_auth: dict[str, Any]) -> None:
        board_participant: Any = BoardParticipantFactory.create(
            board=BoardFactory.create(),
            user=user_auth.get('user'),
            role=BoardParticipant.Role.writer
        )
        category: Any = CategoryFactory.create(board=board_participant.board, user=user_auth.get('user'))
        goal: Any = GoalFactory.create(category=category, user=user_auth.get('user'))
        goal.status = Goal.Status.archived
        goal.save()
        post_response: Any = client.post(
            '/goals/goal_comment/create',
            data={
                "text": "testComment",
                "goal": goal.id
            },
            content_type='application/json',
        )
        expected_response: dict[str, list[ErrorDetail]] = {
            'goal': [ErrorDetail(string="You can't create comment in archived goal", code='invalid')]
        }

        assert post_response.status_code == 400, 'Comment was created successfully'
        assert post_response.data is not None, 'HttpResponseError'
        assert post_response.data == expected_response

    @pytest.mark.django_db
    def test_retrieve_comment(self, client: Any, user_auth: dict[str, Any]) -> None:
        board_participant: Any = BoardParticipantFactory.create(user=user_auth.get('user'))
        category: Any = CategoryFactory.create(board=board_participant.board, user=user_auth.get('user'))
        goal: Any = GoalFactory.create(category=category, user=user_auth.get('user'))
        comment: Any = CommentFactory.create(user=user_auth.get('user'), goal=goal)
        response: Any = client.get(
            f'/goals/goal_comment/{comment.id}',
        )
        expected_response: dict[str, list[ReturnDict]] = {
            "id": comment.id,
            "user": [
                UserDetailSerializer(user_auth.get('user')).data
            ],
            "created": goal.created,
            "updated": goal.updated,
            "text": comment.text,
            "goal": comment.goal.id
        }

        assert response.status_code == 200, 'Status code error'
        assert response.data is not None, 'HttpResponseError'
        assert response.data.get('id') == expected_response.get('id'), 'Wrong id expected'
        assert response.data.get('text') == expected_response.get('text'), 'Wrong text expected'
        assert response.data.get('goal') == expected_response.get('goal'), 'Wrong goal expected'

    @pytest.mark.django_db
    def test_retrieve_goal_403(self, client: Any, user_not_auth: dict[str, Any]) -> None:
        board_participant: Any = BoardParticipantFactory.create(user=user_not_auth)
        category: Any = CategoryFactory.create(board=board_participant.board, user=user_not_auth)
        goal: Any = GoalFactory.create(category=category, user=user_not_auth)
        comment: Any = CommentFactory.create(user=user_not_auth, goal=goal)
        response: Any = client.get(
            f'/goals/goal_comment/{comment.id}',
        )
        expected_response: dict[str, str] = {
            "detail": 'Authentication credentials were not provided.'
        }

        assert response.status_code == 403, 'Status code error'
        assert response.data is not None, 'HttpResponseError'
        assert response.data == expected_response, 'Wrong data'

    @pytest.mark.django_db
    def test_comment_list(self, client: Any, user_auth: dict[str, Any]) -> None:
        board_participant: Any = BoardParticipantFactory.create(user=user_auth.get('user'))
        category: Any = CategoryFactory.create(board=board_participant.board, user=user_auth.get('user'))
        goal: Any = GoalFactory.create(category=category, user=user_auth.get('user'))
        comment: Any = CommentFactory.create_batch(2, user=user_auth.get('user'), goal=goal)
        expected_response: list[ReturnDict] = [
            CommentSerializer(comment[1]).data,
            CommentSerializer(comment[0]).data,
        ]
        response: Any = client.get('/goals/goal_comment/list')
        assert response.status_code == 200, 'Status code error'
        assert response.data is not None, 'HttpResponseError'
        assert response.data == expected_response, 'Wrong data expected'

    @pytest.mark.django_db
    def test_comment_list_403(self, client: Any, user_not_auth: User) -> None:
        board_participant: Any = BoardParticipantFactory.create(user=user_not_auth)
        category: Any = CategoryFactory.create(board=board_participant.board, user=user_not_auth)
        goal: Any = GoalFactory.create(category=category, user=user_not_auth)
        CommentFactory.create_batch(2, user=user_not_auth, goal=goal)
        expected_response: dict[str, str] = {"detail": 'Authentication credentials were not provided.'}
        response: Any = client.get('/goals/goal_comment/list')

        assert response.status_code == 403, 'Status code error'
        assert response.data is not None, 'HttpResponseError'
        assert response.data == expected_response, 'Wrong data expected'

    @pytest.mark.django_db
    def test_update_comment(self, client: Any, user_auth: dict[str, Any]) -> None:
        board_participant: Any = BoardParticipantFactory.create(user=user_auth.get('user'))
        category: Any = CategoryFactory.create(board=board_participant.board, user=user_auth.get('user'))
        goal: Any = GoalFactory.create(category=category, user=user_auth.get('user'))
        comment: Any = CommentFactory.create(user=user_auth.get('user'), goal=goal)
        expected_response: dict[str, str | list[ReturnDict]] = {
            "id": comment.id,
            "user": [UserDetailSerializer(user_auth.get('user')).data],
            "created": comment.goal.created,
            "updated": comment.goal.updated,
            "text": "testComment_edited",
            "goal": comment.goal.id
        }
        put_response: Any = client.put(
            f'/goals/goal_comment/{comment.id}',
            data={
                'text': 'testComment_edited',
            },
            content_type='application/json',
        )

        assert put_response.status_code == 200, 'Goal was not updated successfully'
        assert put_response.data is not None, 'HttpResponseError'
        assert put_response.data.get('text') == expected_response.get('text'), 'Wrong text data'
        assert put_response.data.get('id') == expected_response.get('id'), 'Wrong id'
        assert put_response.data.get('goal') == expected_response.get('goal'), 'Wrong goal expected'

    @pytest.mark.django_db
    def test_update_comment_403(self, client: Any, user_auth: dict[str, Any]) -> None:
        board_participant: Any = BoardParticipantFactory.create(
            user=user_auth.get('user'),
            role=BoardParticipant.Role.reader
        )
        category: Any = CategoryFactory.create(board=board_participant.board, user=user_auth.get('user'))
        goal: Any = GoalFactory.create(category=category, user=user_auth.get('user'))
        comment: Any = CommentFactory.create(user=user_auth.get('user'), goal=goal)
        expected_response: dict[str, str] = {
            'detail': 'You do not have permission to perform this action.'
        }
        put_response: Any = client.put(
            f'/goals/goal_comment/{comment.id}',
            data={
                'text': 'testComment_edited',
            },
            content_type='application/json',
        )

        assert put_response.status_code == 403, 'Board was edited successfully'
        assert put_response.data is not None, 'HttpResponseError'
        assert put_response.data == expected_response, 'Wrong data'

    @pytest.mark.django_db
    def test_delete_comment(self, client: Any, user_auth: dict[str, Any]) -> None:
        board_participant: Any = BoardParticipantFactory.create(user=user_auth.get('user'))
        category: Any = CategoryFactory.create(board=board_participant.board, user=user_auth.get('user'))
        goal: Any = GoalFactory.create(category=category, user=user_auth.get('user'))
        comment: Any = CommentFactory.create(user=user_auth.get('user'), goal=goal)
        delete_response: Any = client.delete(
            f'/goals/goal_comment/{comment.id}',
        )

        assert delete_response.status_code == 204, 'Goal was not deleted successfully'
        assert delete_response.data is None, 'HttpResponseError'

    @pytest.mark.django_db
    def test_delete_comment_403(self, client: Any, user_auth: dict[str, Any]) -> None:
        board_participant: Any = BoardParticipantFactory.create(
            user=user_auth.get('user'),
            role=BoardParticipant.Role.reader
        )
        category: Any = CategoryFactory.create(board=board_participant.board, user=user_auth.get('user'))
        goal: Any = GoalFactory.create(category=category, user=user_auth.get('user'))
        comment: Any = CommentFactory.create(user=user_auth.get('user'), goal=goal)
        expected_response: dict[str, str] = {
            'detail': 'You do not have permission to perform this action.'
        }
        delete_response: Any = client.delete(
            f'/goals/goal_comment/{comment.id}',
        )

        assert delete_response.status_code == 403, 'Category was deleted successfully'
        assert delete_response.data is not None, 'HttpResponseError'
        assert delete_response.data == expected_response, 'Wrong data'
