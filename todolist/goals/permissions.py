from typing import Any

from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import APIView

from todolist.goals.models.board import BoardParticipant
from todolist.goals.models.category import GoalCategory
from todolist.goals.models.comment import Comment
from todolist.goals.models.goal import Goal


class BoardPermissions(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: APIView, obj: Any) -> bool:
        if not request.user.is_authenticated:
            return False
        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(
                user=request.user, board=obj
            ).exists()
        return BoardParticipant.objects.filter(
            user=request.user, board=obj, role=BoardParticipant.Role.owner
        ).exists()


class CategoryPermissions(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: APIView, obj: Any) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return GoalCategory.objects.select_related('board').filter(
                board__participants__user=request.user,
                board=obj.board
            ).exists()
        else:
            return GoalCategory.objects.select_related('board').filter(
                board__participants__user=request.user,
                board=obj.board,
                board__participants__role__in=[
                    BoardParticipant.Role.owner,
                    BoardParticipant.Role.writer
                ]
            ).exists()


class GoalPermissions(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: APIView, obj: Any) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return Goal.objects.select_related('category').filter(
                category__board__participants__user=request.user,
                category__board=obj.category.board
            ).exists()
        else:
            return Goal.objects.select_related('category').filter(
                category__board__participants__user=request.user,
                category__board=obj.category.board,
                category__board__participants__role__in=[
                    BoardParticipant.Role.owner,
                    BoardParticipant.Role.writer
                ]
            ).exists()


class CommentPermissions(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: APIView, obj: Any) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return Comment.objects.select_related('goal').filter(
                goal__category__board__participants__user=request.user,
                goal__category__board=obj.goal.category.board
            ).exists()
        else:
            return Comment.objects.select_related('goal').filter(
                goal__category__board__participants__user=request.user,
                goal__category__board=obj.goal.category.board,
                goal__category__board__participants__role__in=[
                    BoardParticipant.Role.owner,
                    BoardParticipant.Role.writer
                ]
            ).exists()