from django.db import transaction, IntegrityError
from django.db.models import QuerySet
from rest_framework import serializers

from core.models import User
from todolist.goals.models.board import BoardParticipant, Board


class BoardParticipantSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(
        required=True,
        choices=BoardParticipant.Role.choices[1:]
    )
    user = serializers.SlugRelatedField(
        slug_field="username",
        queryset=User.objects.all()
    )

    class Meta:
        model = BoardParticipant
        fields: str = "__all__"
        read_only_fields: tuple = ("id", "created", "updated", "board")


class BoardListSerializer(serializers.ModelSerializer):
    """
    Board list serializer
    """
    class Meta:
        model = Board
        fields: str = "__all__"


class BoardCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def create(self, validated_data) -> Board:
        user = validated_data.pop("user")
        board = Board.objects.create(**validated_data)
        BoardParticipant.objects.create(
            user=user,
            board=board,
            role=BoardParticipant.Role.owner
        )
        return board

    class Meta:
        model = Board
        read_only_fields: tuple = ("id", "created", "updated")
        fields: str = "__all__"


class BoardSerializer(serializers.ModelSerializer):
    participants = BoardParticipantSerializer(
        many=True
    )
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    def update(self, entity: Board, validated_data) -> Board:
        board_owner = validated_data.pop('user')
        elders: QuerySet = entity.participants.exclude(user=board_owner).select_related('user')
        newbies: dict = {user.get('user').id: user for user in validated_data.pop('participants')}
        with transaction.atomic():
            for old in elders:
                if old.user_id not in newbies:
                    old.delete()
                else:
                    if old.role != newbies[old.user_id]['role']:
                        old.role = newbies[old.user_id]['role']
                        old.save()
                    newbies.pop(old.user_id)
            for newbie in newbies.values():
                if newbie.get('user') == board_owner:
                    raise IntegrityError('You cant add yourself as a participant')
                BoardParticipant.objects.create(
                    board=entity,
                    user=newbie.get('user'),
                    role=newbie.get('role')
                )
        entity.title = validated_data.get('title')
        entity.save()
        return entity

    class Meta:
        model = Board
        fields: str = "__all__"
        read_only_fields: tuple = ("id", "created", "updated")