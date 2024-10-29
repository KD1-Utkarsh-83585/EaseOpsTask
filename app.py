from flask import Flask
from flask_migrate import Migrate

from config import db 
from models import Manager, Employee  
from routes import my_blueprint  
from swagger import swaggerui_blueprint  


app = Flask(__name__)

# Configuring MySQL database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:manager@localhost/employeedb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)


migrate = Migrate(app, db)


app.register_blueprint(swaggerui_blueprint)


app.register_blueprint(my_blueprint)  


with app.app_context():
    db.create_all()  

if __name__ == '__main__':
    app.run(debug=True)  
