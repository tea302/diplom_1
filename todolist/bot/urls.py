from django.urls import path

from todolist.bot.views import TgUserUpdateView

urlpatterns = [
    path('verify', TgUserUpdateView.as_view(), name='tg_user-update'),
]