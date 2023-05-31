from django.db import transaction
from django.db.models import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, filters
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.request import Request
from rest_framework.response import Response

from todolist.goals.filters import GoalDateFilter
from todolist.goals.models.goal import Goal
from todolist.goals.permissions import GoalPermissions
from todolist.goals.serializers.goal import GoalCreateSerializer, GoalSerializer


class GoalCreateView(generics.CreateAPIView):
    model = Goal
    permission_classes: list = [permissions.IsAuthenticated]
    serializer_class = GoalCreateSerializer

    def post(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        return super().post(request, *args, **kwargs)


class GoalListView(generics.ListAPIView):
    permission_classes: list = [permissions.IsAuthenticated, GoalPermissions]
    serializer_class = GoalSerializer
    pagination_class = LimitOffsetPagination
    filter_backends: tuple = (
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    )
    filterset_fields: tuple = ('category__board', 'category')
    filterset_class = GoalDateFilter
    ordering_fields: tuple = ('priority', 'due_date')
    ordering: tuple = ('title',)
    search_fields: tuple = ('title',)

    def get_queryset(self) -> QuerySet[Goal]:
        return Goal.objects.select_related('category').filter(
            category__board__participants__user=self.request.user,
            category__board__is_deleted=False,
            category__is_deleted=False
        ).exclude(status=Goal.Status.archived)

    def get(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        return super().get(request, *args, **kwargs)


class GoalDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GoalSerializer
    permission_classes: list = [permissions.IsAuthenticated, GoalPermissions]

    def get_queryset(self) -> QuerySet[Goal]:
        return Goal.objects.select_related('category').filter(
            category__board__participants__user=self.request.user,
            category__board__is_deleted=False,
            category__is_deleted=False
        ).exclude(status=Goal.Status.archived)

    def perform_destroy(self, entity: Goal) -> None:
        with transaction.atomic():
            entity.status = Goal.Status.archived
            entity.save(update_fields=('status',))
            for comment in entity.comment_set.all():
                comment.delete()

    def get(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        return super().get(request, *args, **kwargs)

    def put(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        return super().put(request, *args, **kwargs)

    def patch(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        return super().patch(request, *args, **kwargs)

    def delete(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        return super().delete(request, *args, **kwargs)