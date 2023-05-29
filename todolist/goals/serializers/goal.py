from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied, ValidationError

from core.serializers import UserDetailSerializer
from todolist.goals.models.board import BoardParticipant
from todolist.goals.models.category import GoalCategory
from todolist.goals.models.goal import Goal
from todolist.goals.serializers.category import CategorySerializer


class GoalCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    category = serializers.PrimaryKeyRelatedField(
        queryset=GoalCategory.objects.all()
    )

    def validate_category(self, entity: GoalCategory) -> GoalCategory:
        current_user = self.context.get('request').user  # type: ignore
        board_participant = BoardParticipant.objects.filter(
            board=entity.board,
            user=current_user
        ).first()
        if not board_participant:
            raise PermissionDenied('Board participant not found')
        if board_participant.role == BoardParticipant.Role.reader:
            raise PermissionDenied('You are allowed only to read, not to create')
        if entity.is_deleted:
            raise ValidationError("You can't create goal in deleted category")
        return entity

    class Meta:
        model = Goal
        fields: str = '__all__'
        read_only_fields: tuple = ('id', 'created', 'updated', 'user')


class GoalSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer(read_only=True)
    category = CategorySerializer

    class Meta:
        model = Goal
        fields: str = '__all__'
        read_only_fields: tuple = ('id', 'created', 'updated', 'user')