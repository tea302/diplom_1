from django.urls import path

from core.views import UserCreateView, UserLoginView, UserDetailUpdateLogoutView, UserUpdatePasswordView

urlpatterns = [
    path('signup', UserCreateView.as_view()),
    path('login', UserLoginView.as_view()),
    path('profile', UserDetailUpdateLogoutView.as_view(), name='user-retrieve-update-destroy'),
    path('update_password', UserUpdatePasswordView.as_view())
]