from django.urls import path

from todolist.goals.views.board import BoardCreateView, BoardListView, BoardDetailView
from todolist.goals.views.category import CategoryCreateView, CategoryListView, CategoryDetailView
from todolist.goals.views.comment import CommentCreateView, CommentListView, CommentDetailView
from todolist.goals.views.goal import GoalCreateView, GoalListView, GoalDetailView

urlpatterns = [
    path('board/create', BoardCreateView.as_view(), name='board-create'),
    path('board/list', BoardListView.as_view(), name='board-list'),
    path('board/<int:pk>', BoardDetailView.as_view(), name='board-detail'),

    path("goal_category/create", CategoryCreateView.as_view(), name="category-create"),
    path("goal_category/list", CategoryListView.as_view(), name="category-list"),
    path("goal_category/<int:pk>", CategoryDetailView.as_view(), name="category-detail"),

    path('goal/create', GoalCreateView.as_view(), name="goal-create"),
    path('goal/list', GoalListView.as_view(), name='goal-list'),
    path('goal/<int:pk>', GoalDetailView.as_view(), name='goal-detail'),

    path('goal_comment/create', CommentCreateView.as_view(), name='comment-create'),
    path('goal_comment/list', CommentListView.as_view(), name='comment-list'),
    path('goal_comment/<int:pk>', CommentDetailView.as_view(), name='comment-detail'),
]