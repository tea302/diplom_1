from rest_framework import serializers

from todolist.bot.models import TgUser


class TgUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = TgUser
        fields: str = '__all__'
        read_only_fields: tuple[str, str, str] = ('id', 'tg_user_id', 'tg_chat_id')