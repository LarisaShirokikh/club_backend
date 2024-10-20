from flask import Flask
from .models import db
from flask_cors import CORS
import logging

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object('app.config.Config')

    db.init_app(app)

    logging.basicConfig()
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

    with app.app_context():
        db.create_all()  # Создание всех таблиц
        print("Tables created successfully")

    # Импортируем blueprint после инициализации базы данных
    from .views import bp as main_bp
    app.register_blueprint(main_bp)

    return app