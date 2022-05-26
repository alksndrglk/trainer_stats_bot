import typing

from app.store.database.database import Database

if typing.TYPE_CHECKING:
    from app.web.app import Application


class Store:
    def __init__(self, app: "Application"):
        from app.store.bot.manager import BotManager
        from app.store.client.tg.accessor import TgClientAccessor
        from app.store.results.accessor import ResultsAccessor

        self.results = ResultsAccessor(app)
        self.tg_api = TgClientAccessor(app)
        self.bots_manager = BotManager(app)


def setup_store(app: "Application"):
    app.database = Database(app)
    app.on_startup.append(app.database.connect)
    app.on_shutdown.append(app.database.disconnect)
    app.store = Store(app)
