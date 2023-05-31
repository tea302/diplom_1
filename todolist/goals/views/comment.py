from django.db.models import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, filters
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.request import Request
from rest_framework.response import Response

from todolist.goals.models.comment import Comment
from todolist.goals.models.goal import Goal
from todolist.goals.permissions import CommentPermissions
from todolist.goals.serializers.comment import CommentCreateSerializer, CommentSerializer


class CommentCreateView(generics.CreateAPIView):

    model = Comment
    permission_classes: list = [permissions.IsAuthenticated]
    serializer_class = CommentCreateSerializer

    def post(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        return super().post(request, *args, **kwargs)


class CommentListView(generics.ListAPIView):

    permission_classes: list = [permissions.IsAuthenticated, CommentPermissions]
    serializer_class = CommentSerializer
    pagination_class = LimitOffsetPagination
    filter_backends: tuple = (
        DjangoFilterBackend,
        filters.OrderingFilter,
    )
    filterset_fields: tuple = ('goal__category__board', 'goal')
    ordering_fields: tuple = ('created', 'updated')
    ordering: tuple = ('-created',)

    def get_queryset(self) -> QuerySet[Comment]:

        return Comment.objects.select_related('goal').filter(
            goal__category__board__participants__user=self.request.user,
            goal__category__board__is_deleted=False,
            goal__category__is_deleted=False,
        ).exclude(goal__status=Goal.Status.archived)

    def get(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        return super().get(request, *args, **kwargs)


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes: list = [permissions.IsAuthenticated, CommentPermissions]

    def get_queryset(self) -> QuerySet[Comment]:
        return Comment.objects.select_related('goal').filter(
            goal__category__board__participants__user=self.request.user,
            goal__category__board__is_deleted=False,
            goal__category__is_deleted=False,
        ).exclude(goal__status=Goal.Status.archived)

    def get(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        return super().get(request, *args, **kwargs)

    def put(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        return super().put(request, *args, **kwargs)

    def patch(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        return super().patch(request, *args, **kwargs)

    def delete(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        return super().delete(request, *args, **kwargs)