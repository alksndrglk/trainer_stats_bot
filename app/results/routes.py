import typing
from ..results.views import AddResultView, UserResultsView


if typing.TYPE_CHECKING:
    from app.web.app import Application


def setup_routes(app: "Application"):
    app.router.add_view("/result/{user_name}", UserResultsView)
    app.router.add_view("/result", AddResultView)
