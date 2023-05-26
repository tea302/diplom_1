from django.db import transaction
from django.db.models import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import LimitOffsetPagination

from todolist.goals.filters import GoalDateFilter
from todolist.goals.models import GoalCategory
from todolist.goals.models import GoalComment

from todolist.goals.models import Goal

from todolist.goals.permissions import GoalCategoryPermission, GoalPermission, GoalCommentPermission

from todolist.goals.serializers import GoalCategoryCreateSerializer, GoalCategorySerializer, GoalCreateSerializer, \
    GoalSerializer, GoalCommentSerializer, GoalCommentCreateSerializer


class GoalCategoryCreateView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCategoryCreateSerializer


class GoalCategoryListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCategorySerializer
    filter_backends = [OrderingFilter, SearchFilter]
    ordering_fields = ('title', 'created')
    ordering = ['title']
    search_fields = ['title']

    def get_queryset(self):
        return GoalCategory.objects.select_related('user').filter(user=self.request.user, is_deleted=False)


class GoalCategoryView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [GoalCategoryPermission]
    serializer_class = GoalCategorySerializer

    def get_queryset(self):
        return GoalCategory.objects.select_related('user').filter(user=self.request.user, is_deleted=False)

    def perform_destroy(self, instance: GoalCategory) -> None:
        with transaction.atomic():
            instance.is_deleted = True
            instance.save(update_fields=('is_deleted',))
            instance.goals.update(status=Goal.Status.archived)


class GoalCreateView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCreateSerializer


class GoalListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCreateSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = GoalDateFilter
    ordering_fields = ('title', 'created')
    ordering = ['title']
    search_fields = ('title', 'description')

    def get_queryset(self) -> QuerySet[Goal]:
        return (
            Goal.objects.select_related('user')
            .filter(user=self.request.user, category__is_deleted=False
            ).exclude(status=Goal.Status.archived)
        )


class GoalView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [GoalPermission]
    serializer_class = GoalSerializer

    def get_queryset(self):
        return Goal.objects.select_related('user').filter(
            user=self.request.user, category__is_deleted=False
        ).exclude(status=Goal.Status.archived)

    def perform_destroy(self, instance: Goal):
        instance.status = Goal.Status.archived
        instance.save(update_fields=('status',))


class GoalCommentCreateView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCommentCreateSerializer


class GoalCommentListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCommentSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    # ordering_fields = ('created', 'updated')
    filterset_fields = ['goal']
    ordering = ['-created']

    def get_queryset(self) -> QuerySet[GoalComment]:
        return GoalComment.objects.filter(
            user_id=self.request.user.id
        ).exclude(goal__status=Goal.Status.archived)


class GoalCommentView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [GoalCommentPermission]
    serializer_class = GoalCommentSerializer
    queryset = GoalComment.objects.select_related('user')

