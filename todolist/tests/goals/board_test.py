from typing import Any

import pytest
from rest_framework.utils.serializer_helpers import ReturnDict

from todolist.goals.models.board import BoardParticipant
from todolist.goals.models.goal import Goal
from todolist.goals.serializers.board import BoardParticipantSerializer, BoardListSerializer
from todolist.tests.factories import BoardParticipantFactory, UserFactory, CategoryFactory, GoalFactory


class TestBoard:
    @pytest.mark.django_db
    def test_create_board(self, client: Any, user_auth: dict[str, Any]) -> None:
        expected_response: dict[str, str | int] = {
            'id': 1,
            'title': 'testBoard',
        }

        post_response: Any = client.post(
            '/goals/board/create',
            data={'title': 'testBoard'},
            content_type='application/json',
        )

        assert post_response.status_code == 201, 'Board was not created successfully'
        assert post_response.data is not None, 'HttpResponseError'
        assert post_response.data.get('title') == expected_response.get('title'), 'Wrong title data'
        assert post_response.data.get('id') == expected_response.get('id'), 'Wrong id'
        assert post_response.data.get('is_deleted') is False, 'Wrong is_deleted status'

    @pytest.mark.django_db
    def test_create_board_403(self, client: Any, user_not_auth: User) -> None:
        expected_response: dict[str, str] = {
            'detail': 'Authentication credentials were not provided.'
        }

        post_response: Any = client.post(
            '/goals/board/create',
            data={'title': 'testBoard'},
            content_type='application/json',

        )

        assert post_response.status_code == 403, 'Status code error'
        assert post_response.data is not None, 'HttpResponseError'
        assert post_response.data == expected_response

    @pytest.mark.django_db
    def test_retrieve_board(self, client: Any, user_auth: dict[str, Any]) -> None:
        board_participant: Any = BoardParticipantFactory.create(user=user_auth.get('user'))

        response: Any = client.get(
            f'/goals/board/{board_participant.board.id}',
        )
        expected_response: dict[str, list[ReturnDict]] = {
            "id": response.data.get('id'),
            "participants": [
                BoardParticipantSerializer(board_participant).data
            ],
            "created": board_participant.board.created,
            "updated": board_participant.board.updated,
            "title": board_participant.board.title,
            "is_deleted": board_participant.board.is_deleted
        }

        assert response.status_code == 200, 'Status code error'
        assert response.data is not None, 'HttpResponseError'
        assert response.data.get('id') == expected_response.get('id'), 'Wrong id expected'
        assert response.data.get('title') == expected_response.get('title'), 'Wrong title expected'
        assert response.data.get('is_deleted') == expected_response.get('is_deleted'), 'Wrong is_deleted expected'
        assert response.data.get('participants') == expected_response.get('participants'), 'Wrong participants expected'

    @pytest.mark.django_db
    def test_retrieve_board_403(self, client: Any, user_not_auth: User) -> None:
        board_participant: Any = BoardParticipantFactory.create(user=user_not_auth)

        response: Any = client.get(
            f'/goals/board/{board_participant.board.id}',
        )
        expected_response: dict[str, str] = {
            "detail": 'Authentication credentials were not provided.'

        }

        assert response.status_code == 403, 'Status code error'
        assert response.data is not None, 'HttpResponseError'
        assert response.data == expected_response, 'Wrong data'

    @pytest.mark.django_db
    def test_retrieve_board_404(self, client: Any, user_auth: dict[str, Any]) -> None:
        board_participant: Any = BoardParticipantFactory.create(user=user_auth.get('user'))
        board_participant.board.is_deleted = True
        board_participant.board.save()

        response: Any = client.get(
            f'/goals/board/{board_participant.board.id}',
        )
        not_expected_response: dict[str, bool | list[ReturnDict]] = {
            "id": response.data.get('id'),
            "participants": [
                BoardParticipantSerializer(board_participant).data
            ],
            "created": board_participant.board.created,
            "updated": board_participant.board.updated,
            "title": board_participant.board.title,
            "is_deleted": board_participant.board.is_deleted
        }

        assert response.status_code == 404, 'Status code error'
        assert response.data is not None, 'HttpResponseError'
        assert response.data != not_expected_response, 'Wrong data expected'

    @pytest.mark.django_db
    def test_board_list(self, client: Any, user_auth: dict[str, Any]) -> None:
        board_participants: Any = BoardParticipantFactory.create_batch(2, user=user_auth.get('user'))
        expected_response: list[ReturnDict] = [
            BoardListSerializer(board_participants[0].board).data,
            BoardListSerializer(board_participants[1].board).data,
        ]
        response = client.get('/goals/board/list')

        assert response.status_code == 200, 'Status code error'
        assert response.data is not None, 'HttpResponseError'
        assert response.data == expected_response, 'Wrong data expected'

    @pytest.mark.django_db
    def test_board_list_deleted(self, client: Any, user_auth: dict[str, Any]) -> None:
        board_participants: Any = BoardParticipantFactory.create_batch(2, user=user_auth.get('user'))
        board_participants[0].board.is_deleted = True
        board_participants[0].board.save()
        expected_response: list[ReturnDict] = [
            BoardListSerializer(board_participants[1].board).data,
        ]
        response = client.get('/goals/board/list')

        assert response.status_code == 200, 'Status code error'
        assert response.data is not None, 'HttpResponseError'
        assert response.data == expected_response, 'Wrong data expected'

    @pytest.mark.django_db
    def test_board_list_403(self, client: Any, user_not_auth: User) -> None:
        BoardParticipantFactory.create_batch(2, user=user_not_auth)
        expected_response: dict[str, str] = {"detail": 'Authentication credentials were not provided.'}
        response: Any = client.get('/goals/board/list')

        assert response.status_code == 403, 'Status code error'
        assert response.data is not None, 'HttpResponseError'
        assert response.data == expected_response, 'Wrong data expected'

    @pytest.mark.django_db
    def test_update_board(self, client: Any, user_auth: dict[str, Any]) -> None:
        board_participant_1: Any = BoardParticipantFactory.create(user=user_auth.get('user'))
        board_participant_2: Any = BoardParticipantFactory.create(
            user=UserFactory.create(),
            board=board_participant_1.board,
            role=BoardParticipant.Role.reader
        )
        board_participant_3: Any = BoardParticipantFactory.create(
            user=UserFactory.create(),
            board=board_participant_1.board,
            role=BoardParticipant.Role.writer
        )
        expected_response: dict[str, str | list] = {
            'title': 'testBoard_edited',
            'participants': [
                BoardParticipantSerializer(board_participant_1).data,
                BoardParticipantSerializer(board_participant_2).data
            ]
        }
        put_response_1: Any = client.put(
            f'/goals/board/{board_participant_1.board.id}',
            data={
                'title': 'testBoard_edited',
                'participants': [
                    BoardParticipantSerializer(board_participant_2).data
                ]
            },
            content_type='application/json',
        )

        board_participant_2.role = BoardParticipant.Role.writer
        board_participant_2.save()

        # add new participant, change old participant's role
        put_response_2: Any = client.put(
            f'/goals/board/{board_participant_1.board.id}',
            data={
                'title': 'testBoard_edited',
                'participants': [
                    BoardParticipantSerializer(board_participant_2).data,
                    BoardParticipantSerializer(board_participant_3).data
                ]
            },
            content_type='application/json',
        )

        # delete one old participant
        put_response_3: Any = client.put(
            f'/goals/board/{board_participant_1.board.id}',
            data={
                'title': 'testBoard_edited',
                'participants': [
                    BoardParticipantSerializer(board_participant_2).data,
                ]
            },
            content_type='application/json',
        )

        assert put_response_1.status_code == 200, 'Board was not edited successfully'
        assert put_response_1.data is not None, 'HttpResponseError'
        assert put_response_1.data.get('title') == expected_response.get('title'), 'Wrong title data'
        assert len(put_response_3.data.get('participants')) == 2, 'Wrong count of participants'
        assert put_response_1.data.get('participants')[0]['user'] == board_participant_1.user.username, \
            'Wrong username_1 data'
        assert put_response_1.data.get('participants')[1]['user'] == board_participant_2.user.username, \
            'Wrong username_2 data'
        assert put_response_1.data.get('participants')[0]['board'] == board_participant_1.board.id, \
            'Wrong board_1 data'
        assert put_response_1.data.get('participants')[1]['board'] == board_participant_2.board.id, \
            'Wrong board_2 data'
        # ----------------------------------------------------------------
        assert len(put_response_2.data.get('participants')) == 3, 'Wrong count of participants'
        assert put_response_2.data.get('participants')[1]['user'] == board_participant_2.user.username, \
            'Wrong username_2 data'
        assert put_response_2.data.get('participants')[2]['user'] == board_participant_3.user.username, \
            'Wrong username_3 data'
        assert put_response_2.data.get('participants')[1]['role'] == board_participant_2.role, \
            'Wrong role_2 data'
        assert put_response_2.data.get('participants')[2]['role'] == board_participant_3.role, \
            'Wrong role_3 data'
        assert put_response_2.data.get('participants')[1]['board'] == board_participant_2.board.id, \
            'Wrong board_2 data'
        assert put_response_2.data.get('participants')[2]['board'] == board_participant_3.board.id, \
            'Wrong board_3 data'
        # ----------------------------------------------------------------
        assert len(put_response_3.data.get('participants')) == 2, 'Wrong count of participants'
        assert put_response_3.data.get('participants')[1]['user'] == board_participant_2.user.username, \
            'Wrong username_2 data'
        assert put_response_2.data.get('participants')[1]['role'] == board_participant_2.role, \
            'Wrong role_2 data'
        assert put_response_2.data.get('participants')[1]['board'] == board_participant_2.board.id, \
            'Wrong board_2 data'

    @pytest.mark.django_db
    def test_update_board_403(self, client: Any, user_auth: dict[str, Any]) -> None:
        board_participant: Any = BoardParticipantFactory.create(
            user=user_auth.get('user'),
            role=BoardParticipant.Role.reader
        )
        expected_response: dict[str, str] = {
            'detail': 'You do not have permission to perform this action.'
        }
        put_response: Any = client.put(
            f'/goals/board/{board_participant.board.id}',
            data={
                'title': 'testBoard_edited',
                'participants': []
            },
            content_type='application/json',
        )

        assert put_response.status_code == 403, 'Board was edited successfully'
        assert put_response.data is not None, 'HttpResponseError'
        assert put_response.data == expected_response, 'Wrong data'

    @pytest.mark.django_db
    def test_update_board_404(self, client: Any, user_auth: dict[str, Any]) -> None:
        board_participant: Any = BoardParticipantFactory.create(
            user=user_auth.get('user'),
            role=BoardParticipant.Role.reader
        )
        board_participant.board.is_deleted = True
        board_participant.board.save()
        not_expected_response: dict[str, str | list] = {
            'title': 'testBoard_edited',
            'participants': []
        }
        put_response: Any = client.put(
            f'/goals/board/{board_participant.board.id}',
            data={
                'title': 'testBoard_edited',
                'participants': []
            },
            content_type='application/json',
        )

        assert put_response.status_code == 404, 'Status code error'
        assert put_response.data is not None, 'HttpResponseError'
        assert put_response.data != not_expected_response, 'Wrong data expected'

    @pytest.mark.django_db
    def test_delete_board(self, client: Any, user_auth: dict[str, Any]) -> None:
        board_participant: Any = BoardParticipantFactory.create(user=user_auth.get('user'))
        delete_response: Any = client.delete(
            f'/goals/board/{board_participant.board.id}',
        )

        assert delete_response.status_code == 204, 'Board was not deleted successfully'
        assert delete_response.data is None, 'HttpResponseError'

    @pytest.mark.django_db
    def test_delete_board_403(self, client: Any, user_auth: dict[str, Any]) -> None:
        board_participant: Any = BoardParticipantFactory.create(
            user=user_auth.get('user'),
            role=BoardParticipant.Role.reader
        )
        expected_response: dict[str, str] = {
            'detail': 'You do not have permission to perform this action.'
        }
        delete_response: Any = client.delete(
            f'/goals/board/{board_participant.board.id}',
        )

        assert delete_response.status_code == 403, 'Board was deleted successfully'
        assert delete_response.data is not None, 'HttpResponseError'
        assert delete_response.data == expected_response, 'Wrong data'

    @pytest.mark.django_db
    def test_entities_change_status(self, client: Any, user_auth: dict[str, Any]) -> None:
        board_participant: Any = BoardParticipantFactory.create(user=user_auth.get('user'))
        category: Any = CategoryFactory.create(board=board_participant.board, user=user_auth.get('user'))
        goal: Any = GoalFactory.create(category=category, user=user_auth.get('user'))
        delete_response: Any = client.delete(
            f'/goals/board/{board_participant.board.id}',
        )
        category.refresh_from_db()
        goal.refresh_from_db()

        assert delete_response.status_code == 204, 'Wrong'
        assert category.is_deleted is True, 'Category was not deleted successfully'
        assert goal.status == Goal.Status.archived, 'Wrong status expected'
