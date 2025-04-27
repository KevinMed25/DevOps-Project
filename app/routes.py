def register_routes(app):
    from app.controllers import drivers
    app.register_blueprint(drivers.drivers_blueprint, url_prefix='/drivers')