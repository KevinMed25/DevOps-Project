from flask import Blueprint, jsonify
from http import HTTPStatus
import logging
from utils.auth_middleware import admin_required
from services.dashboard_service import DashboardService

logger = logging.getLogger(__name__)
dashboard_blueprint = Blueprint('dashboard', __name__)

@dashboard_blueprint.route('/', methods=['GET'])
@admin_required()
def getDashboardCounts():
    logger.info("Request for dashboard counts received.")
    try:
        dashboardService = DashboardService()
        dashboardCounts = dashboardService.getCounts()
        logger.info(f"Dashboard counts retrieved successfully: {dashboardCounts}")
        return dashboardCounts, HTTPStatus.OK
    except Exception as e:
        logger.exception(f"Error retrieving dashboard counts: {e}")
        return jsonify({'error': 'Error interno del servidor al obtener los conteos del dashboard'}), HTTPStatus.INTERNAL_SERVER_ERROR