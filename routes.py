from flask import request, jsonify, Blueprint  
from config import db  
from models import Manager, Employee


my_blueprint = Blueprint('my_blueprint', __name__)

# --------------------------- Home Route --------------------------- #
@my_blueprint.route('/')
def home():
    return "Welcome to the Employee Management System!"

# --------------------------- Manager Routes --------------------------- #

@my_blueprint.route('/managers', methods=['POST'])
def create_manager():
    try:
        data = request.get_json()
        new_manager = Manager(name=data['name'])
        db.session.add(new_manager)
        db.session.commit()
        return jsonify({"message": "Manager created", "id": new_manager.id}), 201
    except Exception as e:
        db.session.rollback()  # Rollback the session on error
        return jsonify({"error": "An error occurred while creating the manager."}), 500

@my_blueprint.route('/managers', methods=['GET'])
def get_managers():
    try:
        managers = Manager.query.all()
        return jsonify([{'id': m.id, 'name': m.name} for m in managers]), 200
    except Exception as e:
        app.logger.error(f"Error retrieving managers: {str(e)}")
        return jsonify({"error": "An error occurred while retrieving managers."}), 500

@my_blueprint.route('/managers/<int:manager_id>', methods=['GET'])
def get_manager(manager_id):
    try:
        manager = Manager.query.get_or_404(manager_id)
        return jsonify({'id': manager.id, 'name': manager.name}), 200
    except Exception as e:
        app.logger.error(f"Error retrieving manager {manager_id}: {str(e)}")
        return jsonify({"error": "An error occurred while retrieving the manager."}), 500

@my_blueprint.route('/managers/<int:manager_id>', methods=['PUT'])
def update_manager(manager_id):
    try:
        manager = Manager.query.get_or_404(manager_id)
        data = request.get_json()
        manager.name = data.get('name', manager.name)
        db.session.commit()
        return jsonify({"message": "Manager updated", "id": manager.id}), 200
    except Exception as e:
        db.session.rollback()  
        app.logger.error(f"Error updating manager {manager_id}: {str(e)}")
        return jsonify({"error": "An error occurred while updating the manager."}), 500

@my_blueprint.route('/managers/<int:manager_id>', methods=['DELETE'])
def delete_manager(manager_id):
    try:
        manager = Manager.query.get_or_404(manager_id)
        db.session.delete(manager)
        db.session.commit()
        return jsonify({"message": "Manager deleted"}), 200
    except Exception as e:
        db.session.rollback()  
        return jsonify({"error": "Integrity error occurred. Please check related employees."}), 400
    except Exception as e:
        db.session.rollback()  
        app.logger.error(f"Error deleting manager {manager_id}: {str(e)}")
        return jsonify({"error": "An error occurred while trying to delete the manager."}), 500

# --------------------------- Employee Routes --------------------------- #

@my_blueprint.route('/employees', methods=['POST'])
def create_employee():
    try:
        data = request.get_json()
        new_employee = Employee(name=data['name'], manager_id=data['manager_id'])
        db.session.add(new_employee)
        db.session.commit()
        return jsonify({"message": "Employee created", "id": new_employee.id}), 201
    except Exception as e:
        db.session.rollback()  
        app.logger.error(f"Error creating employee: {str(e)}")
        return jsonify({"error": "An error occurred while creating the employee."}), 500

@my_blueprint.route('/employees', methods=['GET'])
def get_employees():
    try:
        employees = Employee.query.all()
        return jsonify([{'id': e.id, 'name': e.name, 'manager_id': e.manager_id} for e in employees]), 200
    except Exception as e:
        app.logger.error(f"Error retrieving employees: {str(e)}")
        return jsonify({"error": "An error occurred while retrieving employees."}), 500

@my_blueprint.route('/employees/<int:employee_id>', methods=['GET'])
def get_employee(employee_id):
    try:
        employee = Employee.query.get_or_404(employee_id)
        return jsonify({'id': employee.id, 'name': employee.name, 'manager_id': employee.manager_id}), 200
    except Exception as e:
        app.logger.error(f"Error retrieving employee {employee_id}: {str(e)}")
        return jsonify({"error": "An error occurred while retrieving the employee."}), 500

@my_blueprint.route('/employees/<int:employee_id>', methods=['PUT'])
def update_employee(employee_id):
    try:
        employee = Employee.query.get_or_404(employee_id)
        data = request.get_json()
        employee.name = data.get('name', employee.name)
        employee.manager_id = data.get('manager_id', employee.manager_id)
        db.session.commit()
        return jsonify({"message": "Employee updated", "id": employee.id}), 200
    except Exception as e:
        db.session.rollback()  
        app.logger.error(f"Error updating employee {employee_id}: {str(e)}")
        return jsonify({"error": "An error occurred while updating the employee."}), 500

@my_blueprint.route('/employees/<int:employee_id>', methods=['DELETE'])
def delete_employee(employee_id):
    try:
        employee = Employee.query.get_or_404(employee_id)
        db.session.delete(employee)
        db.session.commit()
        return jsonify({"message": "Employee deleted"}), 200
    except Exception as e:
        db.session.rollback()  
        app.logger.error(f"Error deleting employee {employee_id}: {str(e)}")
        return jsonify({"error": "An error occurred while trying to delete the employee."}), 500
