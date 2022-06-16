import typing
import gino
from gino.api import Gino
from app.store.database.gino import db
from sqlalchemy.engine.url import URL

if typing.TYPE_CHECKING:
    from app.web.app import Application


class Database:
    db: Gino

    def __init__(self, app: "Application"):
        self.app = app
        self.db: Optional[Gino] = None

    async def connect(self, app: "Application", *_, **kw):
        self._engine = await gino.create_engine(
            URL(
                drivername="asyncpg",
                host=app.config.database.host,
                database=app.config.database.database,
                username=app.config.database.user,
                password=app.config.database.password,
                port=app.config.database.port,
            ),
            min_size=1,
            max_size=1,
        )
        db.bind = self._engine
        self.db = db
        await db.gino.create_all()

    async def disconnect(self, *_, **kw):
        self.app = None
        if self.db.bind.current_connection:
            engine, db.bind = db.bind, None
            await engine.close()
