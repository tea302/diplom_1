from typing import Any

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseBase
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from core.models import User
from core.serializers import UserRegistrationSerializer, UserDetailSerializer, UserChangePasswordSerializer


class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

    def post(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        return super().post(request, *args, **kwargs)


class UserLoginView(CreateAPIView):
    def post(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        user: Any = authenticate(
            username=request.data.get('username'),
            password=request.data.get('password')
        )
        if user:
            login(request, user)
            return Response('Successful login', status=status.HTTP_201_CREATED)
        raise AuthenticationFailed('Invalid username or password')


class UserDetailUpdateLogoutView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserDetailSerializer
    permission_classes: list = [IsAuthenticated]

    @method_decorator(ensure_csrf_cookie)
    def dispatch(self, *args, **kwargs) -> HttpResponseBase:
        return super().dispatch(*args, **kwargs)

    def get_object(self) -> Any:
        return self.request.user

    def destroy(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        logout(request)
        return Response('Successful logout', status=status.HTTP_204_NO_CONTENT)

    def get(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        return super().get(request, *args, **kwargs)

    def put(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        return super().put(request, *args, **kwargs)

    def patch(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        return super().patch(request, *args, **kwargs)

    def delete(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        return super().delete(request, *args, **kwargs)


class UserUpdatePasswordView(UpdateAPIView):
    serializer_class = UserChangePasswordSerializer
    permission_classes: list = [IsAuthenticated]

    def get_object(self) -> Any:
        return self.request.user

    def put(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        return super().put(request, *args, **kwargs)

    def patch(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        return super().patch(request, *args, **kwargs)