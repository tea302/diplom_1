from typing import Any

from todolist.bot.tg.bot_dao import BotDAO
from todolist.bot.tg.bot_state import BotState1
from todolist.bot.tg.client import TgClient
from todolist.settings import TG_BOT_KEY


class BotSession:
    _state = None
    client: TgClient = TgClient(TG_BOT_KEY)
    dao: BotDAO = BotDAO()

    def __init__(self) -> None:
        self.setState(BotState1(client=self.client, botSession=self))

    def setState(self, state) -> None:
        self._state = state
        self._state.botSession = self

    def doSomething(self, **kwargs) -> Any:
        return self._state.doSomething(**kwargs)  # type: ignore

    def run_bot(self) -> None:
        update_id: int = 0
        while True:
            print(self._state.__doc__)
            updates = self.client.get_updates(update_id)
            if updates.result:
                for item in updates.result:
                    update_id = item.update_id + 1
                    self.doSomething(item=item)