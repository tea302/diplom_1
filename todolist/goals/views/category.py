from django.db import transaction
from django.db.models import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, filters
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.request import Request
from rest_framework.response import Response

from todolist.goals.models.category import GoalCategory
from todolist.goals.models.goal import Goal
from todolist.goals.permissions import CategoryPermissions
from todolist.goals.serializers.category import CategoryCreateSerializer, CategorySerializer


class CategoryCreateView(generics.CreateAPIView):
    model = GoalCategory
    permission_classes: list = [permissions.IsAuthenticated]
    serializer_class = CategoryCreateSerializer

    def post(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        return super().post(request, *args, **kwargs)


class CategoryListView(generics.ListAPIView):
    permission_classes: list = [permissions.IsAuthenticated, CategoryPermissions]
    serializer_class = CategorySerializer
    pagination_class = LimitOffsetPagination
    filter_backends: tuple = (
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    )
    filterset_fields: tuple = ('board',)
    ordering_fields: tuple = ('title', 'created')
    ordering: tuple = ('title',)
    search_fields: tuple = ('title', 'board__title')

    def get_queryset(self) -> QuerySet[GoalCategory]:
        return GoalCategory.objects.select_related('board').filter(
            board__participants__user=self.request.user,
            board__is_deleted=False,
            is_deleted=False
        )

    def get(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        return super().get(request, *args, **kwargs)


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer
    permission_classes: list = [permissions.IsAuthenticated, CategoryPermissions]

    def get_queryset(self) -> QuerySet[GoalCategory]:

        return GoalCategory.objects.select_related('board').filter(
            board__participants__user=self.request.user,
            board__is_deleted=False,
            is_deleted=False
        )

    def perform_destroy(self, entity: GoalCategory) -> None:
        with transaction.atomic():
            entity.is_deleted = True
            entity.save(update_fields=('is_deleted',))
            entity.goal_set.update(status=Goal.Status.archived)

    def get(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        return super().get(request, *args, **kwargs)

    def put(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        return super().put(request, *args, **kwargs)

    def patch(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        return super().patch(request, *args, **kwargs)

    def delete(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        return super().delete(request, *args, **kwargs)