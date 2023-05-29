from django.db.models import QuerySet
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from todolist.bot.models import TgUser
from todolist.bot.serializers import TgUserSerializer


class TgUserUpdateView(generics.GenericAPIView):
    queryset: QuerySet[TgUser] = TgUser.objects.all()
    serializer_class = TgUserSerializer
    permission_classes: list = [IsAuthenticated]

    def patch(self, request: Request, *args: tuple, **kwargs: dict) -> Response:

        return self.update(request, *args, **kwargs)

    def update(self, request: Request, *args: tuple, **kwargs: dict) -> Response:

        current_user = request.user
        tg_user = TgUser.objects.filter(
            verification_code=request.data.get('verification_code')
        ).first()
        if not tg_user:
            return Response('Invalid verification code', status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(tg_user, data=request.data)
        serializer.is_valid(raise_exception=True)
        tg_user.user = current_user  # type: ignore
        tg_user.status = TgUser.Status.verified
        tg_user.save()

        return Response('Success verification', status=status.HTTP_200_OK)
