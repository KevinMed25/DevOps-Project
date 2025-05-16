from utils.db import get_db
from models.routes import Route, RouteSchema
from models.drivers import Driver
from models.vehicle import Vehicle

class RouteService:
    
    def get_route_by_id(self, route_id: int):
        db = next(get_db())
        route = db.query(Route).filter(Route.id == route_id).first()
        if not route:
            raise ValueError("Ruta no encontrada")
        return route
    
    def get_all_routes(self):
        db = next(get_db())
        return db.query(Route).all()
    
    def create_route(self, route: RouteSchema):
        db = next(get_db())
        
        vehicle = db.query(Vehicle).filter(Vehicle.id == route.vehicle_id).first()
        driver = db.query(Driver).filter(Driver.id == route.driver_id).first()
        
        if not vehicle or not driver:
            raise ValueError("El vehículo o conductor no existen")
        
        # Validar que no haya otra ruta ese día para el vehículo 
        existing_route = db.query(Route).filter(
            Route.vehicle_id == route.vehicle_id,
            Route.date == route.date
        ).first()
        
        if existing_route:
            raise ValueError("El vehículo ya tiene una ruta programada para esta fecha")
        
        new_route = Route(
            name=route.name,
            date=route.date,
            origin_lat=route.origin_lat,
            origin_lng=route.origin_lng,
            destination_lat=route.destination_lat,
            destination_lng=route.destination_lng,
            vehicle_id=route.vehicle_id,
            driver_id=route.driver_id,
            status="pending"
        )
        
        db.add(new_route)
        db.commit()
        db.refresh(new_route)
        return new_route.id

    def update_route(self, route_id: int, route_data: RouteSchema):
        db = next(get_db())
        
        route = db.query(Route).filter(Route.id == route_id).first()
        if not route:
            raise ValueError("Ruta no encontrada")
        
        # Validar cambios en fecha/vehículo
        if route_data.date != route.date or route_data.vehicle_id != route.vehicle_id:
            existing_route = db.query(Route).filter(
                Route.vehicle_id == route_data.vehicle_id,
                Route.date == route_data.date,
                Route.id != route_id
            ).first()
            
            if existing_route:
                raise ValueError("El vehículo ya tiene otra ruta programada para la nueva fecha")
        
        # Actualizar campos
        route.name = route_data.name
        route.date = route_data.date
        route.origin_lat = route_data.origin_lat
        route.origin_lng = route_data.origin_lng
        route.destination_lat = route_data.destination_lat
        route.destination_lng = route_data.destination_lng
        route.status = route_data.status or route.status
        route.problem_description = route_data.problem_description
        route.comments = route_data.comments
        
        db.commit()
        return route.id
    
