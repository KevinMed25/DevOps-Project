from controllers import routes_controller, vehicle_controller,assignment_controller, admin_controller, dashboard_controller, drivers_controller

def register_routes(app):
    app.register_blueprint(drivers_controller.drivers_blueprint, url_prefix='/drivers')
    app.register_blueprint(vehicle_controller.vehicle_blueprint, url_prefix='/vehicle')
    app.register_blueprint(assignment_controller.assignment_blueprint, url_prefix='/assignments')
    app.register_blueprint(admin_controller.admin_blueprint, url_prefix='/admin')
    app.register_blueprint(routes_controller.rutas_blueprint, url_prefix='/routes')
    app.register_blueprint(dashboard_controller.dashboard_blueprint, url_prefix='/dashboard')