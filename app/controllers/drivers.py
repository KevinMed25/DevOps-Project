from flask import Blueprint, jsonify

drivers_blueprint = Blueprint('drivers', __name__)
@drivers_blueprint.route('/drivers', methods=['GET'])
def get_drivers():
    pass