from django.db import IntegrityError, transaction
from django.db.models import QuerySet
from rest_framework import generics, permissions, status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.request import Request
from rest_framework.response import Response

from todolist.goals.models.board import Board
from todolist.goals.models.goal import Goal
from todolist.goals.permissions import BoardPermissions
from todolist.goals.serializers.board import BoardCreateSerializer, BoardListSerializer, BoardSerializer


class BoardCreateView(generics.CreateAPIView):
    model = Board
    permission_classes: list = [permissions.IsAuthenticated]
    serializer_class = BoardCreateSerializer

    def post(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        return super().post(request, *args, **kwargs)


class BoardListView(generics.ListAPIView):
    permission_classes: list = [permissions.IsAuthenticated]
    serializer_class = BoardListSerializer
    pagination_class = LimitOffsetPagination
    ordering: tuple = ('title',)

    def get_queryset(self) -> QuerySet[Board]:
        return Board.objects.filter(
            participants__user=self.request.user,  # type: ignore
            is_deleted=False
        )

    def get(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        return super().get(request, *args, **kwargs)


class BoardDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes: tuple = (permissions.IsAuthenticated, BoardPermissions)
    serializer_class = BoardSerializer

    def get_queryset(self) -> QuerySet[Board]:
        return Board.objects.filter(
            participants__user=self.request.user,  # type: ignore
            is_deleted=False
        )

    def update(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        try:
            return super().update(request, *args, **kwargs)
        except IntegrityError as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    def perform_destroy(self, entity: Board) -> None:
        with transaction.atomic():
            entity.is_deleted = True
            entity.save()
            entity.categories.update(is_deleted=True)
            Goal.objects.filter(category__board=entity).update(
                status=Goal.Status.archived
            )

    def get(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        return super().get(request, *args, **kwargs)

    def put(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        return super().put(request, *args, **kwargs)

    def patch(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        return super().patch(request, *args, **kwargs)

    def delete(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        return super().delete(request, *args, **kwargs)