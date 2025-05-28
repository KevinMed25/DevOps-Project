from flask import Blueprint
from http import HTTPStatus
from utils.auth_middleware import admin_required
from services.dashboard_service import DashboardService

dashboard_blueprint = Blueprint('dashboard', __name__)

@dashboard_blueprint.route('/', methods=['GET'])
@admin_required()
def getDashboardCounts():
    dashboardService = DashboardService()
    dashboardCounts = dashboardService.getCounts()
    return dashboardCounts, HTTPStatus.OK
