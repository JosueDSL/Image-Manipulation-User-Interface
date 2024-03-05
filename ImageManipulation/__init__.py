from flask import Flask
from flask_jwt_extended import JWTManager
from datetime import timedelta

def create_app():
    # Creating the Flask app
    app = Flask(__name__)
    app.config['JWT_SECRET_KEY'] = '03UVDeJ5V8mxXpC'
    
    # Initializing the JWTManager
    jwt = JWTManager(app)

    # Configuring the upload folder
    UPLOAD_FOLDER = 'uploads'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=8)
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)

    # Registering the blueprints
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    
    return app