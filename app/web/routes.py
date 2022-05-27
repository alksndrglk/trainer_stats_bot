from aiohttp.web_app import Application


def setup_routes(app: Application):
    from app.results.routes import setup_routes as results_setup_routes

    results_setup_routes(app)
