from utils.db import get_db
from models.routes import Route, RouteSchema
from models.drivers import Driver
from models.vehicle import Vehicle
from models.assignment import Assignment
from sqlalchemy.orm import joinedload
from typing import Dict, Tuple, List, Optional
from http import HTTPStatus

class RouteService:
    VALID_STATUSES = {"completed", "failed", "in_progress", "pending"}

    def is_vehicle_assigned_to_driver(self, vehicle_id: int, driver_id: int) -> bool:
        """Verifica si un vehículo está asignado a un conductor."""
        db = next(get_db())
        assignment = db.query(Assignment).filter(
            Assignment.vehicle_id == vehicle_id,
            Assignment.driver_id == driver_id
        ).first()
        return assignment is not None

    def _validate_route_status(self, status: Optional[str]) -> str:
        """Valida y establece un estado por defecto para la ruta."""
        if status is None:
            return "pending"
        if status not in self.VALID_STATUSES:
            raise ValueError(f"Estado inválido. Los estados permitidos son: {self.VALID_STATUSES}")
        return status

    def _build_route_data(self, route: Route) -> Dict:
        """Construye el diccionario de datos de la ruta."""
        return {
            "id": route.id,
            "name": route.name,
            "date": route.date.isoformat() if route.date else None,
            "origin_lat": route.origin_lat,
            "origin_lng": route.origin_lng,
            "destination_lat": route.destination_lat,
            "destination_lng": route.destination_lng,
            "vehicle_id": route.vehicle_id,
            "driver_id": route.driver_id,
            "status": route.status,
            "problem_description": route.problem_description,
            "comments": route.comments,
            "vehicle_info": {
                "brand": route.vehicle.brand if route.vehicle else None,
                "model": route.vehicle.model if route.vehicle else None,
                "license_plate": route.vehicle.license_plate if route.vehicle else None,
                "vin": route.vehicle.vin if route.vehicle else None
            },
            "driver_info": {
                "name": route.driver.name if route.driver else None,
                "license": route.driver.license_number if route.driver else None,
                "curp": route.driver.curp if route.driver else None
            }
        }

    def create_route(self, route: RouteSchema) -> Tuple[int, str]:
        """Crea una nueva ruta."""
        db = next(get_db())
        
        try:
            # Verificar existencia del vehículo
            vehicle = db.query(Vehicle).filter(Vehicle.id == route.vehicle_id).first()
            if not vehicle:
                raise ValueError(f"El vehículo con ID {route.vehicle_id} no existe")

            # Verificar existencia del conductor
            driver = db.query(Driver).filter(Driver.id == route.driver_id).first()
            if not driver:
                raise ValueError(f"El conductor con ID {route.driver_id} no existe")

            # Verificar asignación vehículo-conductor
            assignment = db.query(Assignment).filter(
                Assignment.vehicle_id == route.vehicle_id,
                Assignment.driver_id == route.driver_id
            ).first()
            
            if not assignment:
                raise ValueError(f"El vehículo {route.vehicle_id} no está asignado al conductor {route.driver_id}")

            # Verificar ruta duplicada para el mismo vehículo y fecha
            existing_route = db.query(Route).filter(
                Route.vehicle_id == route.vehicle_id,
                Route.date == route.date
            ).first()
            
            if existing_route:
                raise ValueError(f"El vehículo {route.vehicle_id} ya tiene una ruta programada para esta fecha")

            # Validar y establecer estado
            validated_status = self._validate_route_status(getattr(route, 'status', None))

            new_route = Route(
                name=route.name,
                date=route.date,
                origin_lat=route.origin_lat,
                origin_lng=route.origin_lng,
                destination_lat=route.destination_lat,
                destination_lng=route.destination_lng,
                vehicle_id=route.vehicle_id,
                driver_id=route.driver_id,
                status=validated_status,
                problem_description=route.problem_description,
                comments=route.comments
            )

            db.add(new_route)
            db.commit()
            db.refresh(new_route)
            return new_route.id, "Ruta creada exitosamente"

        except ValueError as e:
            db.rollback()
            raise e
        except Exception as e:
            db.rollback()
            raise Exception(f"Error al crear la ruta: {str(e)}")

    def get_all_routes(self) -> Tuple[List[Dict], str]:
        """Obtiene todas las rutas."""
        try:
            db = next(get_db())
            routes = db.query(Route).options(
                joinedload(Route.vehicle),
                joinedload(Route.driver)
            ).all()
            
            if not routes:
                return [], "No se encontraron rutas registradas"
                
            routes_data = [self._build_route_data(route) for route in routes]
            return routes_data, "Rutas obtenidas exitosamente"
            
        except Exception as e:
            raise Exception(f"Error al obtener las rutas: {str(e)}")

    def get_route_by_id(self, route_id: int) -> Tuple[Optional[Dict], str]:
        """Obtiene una ruta por su ID."""
        try:
            db = next(get_db())
            route = db.query(Route).options(
                joinedload(Route.vehicle),
                joinedload(Route.driver)
            ).filter(Route.id == route_id).first()
            
            if not route:
                return None, f"No se encontró la ruta con ID {route_id}"
                
            route_data = self._build_route_data(route)
            return route_data, "Ruta obtenida exitosamente"
            
        except Exception as e:
            raise Exception(f"Error al obtener la ruta: {str(e)}")

    def update_route(self, route_id: int, route_data: RouteSchema) -> Tuple[Optional[Dict], str]:
        """Actualiza una ruta existente con validación completa."""
        db = next(get_db())
        
        try:
            route = db.query(Route).filter(Route.id == route_id).first()
            if not route:
                return None, f"No se encontró la ruta con ID {route_id}"

            # Obtener IDs actuales o nuevos
            vehicle_id = getattr(route_data, 'vehicle_id', route.vehicle_id)
            driver_id = getattr(route_data, 'driver_id', route.driver_id)

            # Verificar existencia del vehículo si se está actualizando
            if hasattr(route_data, 'vehicle_id'):
                vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
                if not vehicle:
                    raise ValueError(f"El vehículo con ID {vehicle_id} no existe")

            # Verificar existencia del conductor si se está actualizando
            if hasattr(route_data, 'driver_id'):
                driver = db.query(Driver).filter(Driver.id == driver_id).first()
                if not driver:
                    raise ValueError(f"El conductor con ID {driver_id} no existe")

            # Verificar asignación vehículo-conductor si se están actualizando
            if hasattr(route_data, 'vehicle_id') or hasattr(route_data, 'driver_id'):
                assignment = db.query(Assignment).filter(
                    Assignment.vehicle_id == vehicle_id,
                    Assignment.driver_id == driver_id
                ).first()
                
                if not assignment:
                    raise ValueError(f"El vehículo {vehicle_id} no está asignado al conductor {driver_id}")

            # Validar estado si se está actualizando
            if hasattr(route_data, 'status'):
                validated_status = self._validate_route_status(route_data.status)
                setattr(route, 'status', validated_status)

            # Actualizar campos
            for field in ['name', 'date', 'origin_lat', 'origin_lng', 
                        'destination_lat', 'destination_lng',
                        'problem_description', 'comments', 'vehicle_id', 'driver_id']:
                if hasattr(route_data, field):
                    setattr(route, field, getattr(route_data, field))

            db.commit()
            
            # Obtener la ruta actualizada
            updated_route = self._build_route_data(route)
            return updated_route, "Ruta actualizada exitosamente"
            
        except ValueError as e:
            db.rollback()
            raise e
        except Exception as e:
            db.rollback()
            raise Exception(f"Error al actualizar la ruta: {str(e)}")

    def delete_route(self, route_id: int) -> Tuple[bool, str]:
        """Elimina una ruta."""
        db = next(get_db())
        
        try:
            route = db.query(Route).filter(Route.id == route_id).first()
            if not route:
                return False, f"No se encontró la ruta con ID {route_id}"
                
            db.delete(route)
            db.commit()
            return True, f"Ruta con ID {route_id} eliminada exitosamente"
            
        except Exception as e:
            db.rollback()
            raise Exception(f"Error al eliminar la ruta: {str(e)}")