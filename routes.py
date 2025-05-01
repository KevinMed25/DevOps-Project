from controllers import drivers
from controllers import drivers, routes_controller, vehicle_controller, assignment_controller

def register_routes(app):
    app.register_blueprint(drivers.drivers_blueprint, url_prefix='/drivers')
    app.register_blueprint(vehicle_controller.vehicle_blueprint, url_prefix='/vehicle')
    app.register_blueprint(vehicle_controller.vehicle_blueprint, url_prefix='/assignments')
    app.register_blueprint(admin_controller.admin_blueprint, url_prefix='/admin')