from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Configuración de la base de datos
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Cambia según tu base de datos
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = '140603'

    # Inicialización de la base de datos
    db.init_app(app)

    # Registra los blueprints y realiza otras configuraciones
    with app.app_context():
        from . import routes  # Importa tus rutas aquí
        app.register_blueprint(routes.main)

    return app