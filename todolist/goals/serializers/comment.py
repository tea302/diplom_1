from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied, ValidationError

from core.serializers import UserDetailSerializer
from todolist.goals.models.board import BoardParticipant
from todolist.goals.models.comment import Comment
from todolist.goals.models.goal import Goal


class CommentCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    def validate_goal(self, entity: Goal) -> Goal:
        current_user = self.context.get('request').user  # type: ignore
        board_participant = BoardParticipant.objects.filter(
            board=entity.category.board,
            user=current_user
        ).first()
        if not board_participant:
            raise PermissionDenied('Board participant not found')
        if board_participant.role == BoardParticipant.Role.reader:
            raise PermissionDenied('You are allowed only to read, not to create')
        if entity.status == Goal.Status.archived:
            raise ValidationError("You can't create comment in archived goal")
        return entity

    class Meta:
        model = Comment
        fields: str = '__all__'
        read_only_fields: tuple = ('id', 'created', 'updated', 'user')


class CommentSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer(read_only=True)
    goal: serializers.PrimaryKeyRelatedField = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields: str = '__all__'
        read_only_fields: tuple = ('id', 'created', 'updated', 'user', 'goal')