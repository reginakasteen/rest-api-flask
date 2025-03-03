from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from app.db import db
from app.jwt import jwt
from app.user import bp as user_bp
from app.expense import bp as expense_bp


def create_app():
    app = Flask(__name__)
    
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = "secret_key"
    
    db.init_app(app)
    jwt.init_app(app)
    migrate = Migrate(app, db)
    
    app.register_blueprint(user_bp)
    app.register_blueprint(expense_bp)
    print("Registered routes:")
    for rule in app.url_map.iter_rules():
        print(rule)

    with app.app_context():
            db.create_all()
    
    @app.route("/")
    def home():
        return {"message": "Welcome to the Flask API"}, 200
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)