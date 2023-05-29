from django.core.management import BaseCommand

from todolist.bot.tg.bot_session import BotSession


class Command(BaseCommand):
    help = 'Run telegram bot'

    def handle(self, *args, **options) -> None:
        """Create session with bot and start bot"""
        bot = BotSession()
        bot.run_bot()