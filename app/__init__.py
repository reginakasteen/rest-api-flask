from flask import Flask, jsonify
import os

def create_app():
    print("Starting app creation...")
    app = Flask(__name__, instance_relative_config=True)
    config_type = os.getenv("CONFIG_TYPE", default="app.config.Config")
    app.config.from_object(config_type)
    print("App created successfully!")

    @app.route('/')
    def home():
        """
        Welcome page
        ---
        tags:
            - homepage
        produces:
            - application/json
        responses:
            200:
                description: Welcome
                schema:
                    $ref: '#/definitions/Hello'
        """
        return  jsonify(message='Hi')

    @app.errorhandler(404)
    def handle_404(exeption):
        return jsonify(error="No items found"), 404

    
    from app.swagger_bp import swagger_ui_blueprint, SWAGGER_API_URL
    from app.swagger_utils import build_swagger
    @app.route(SWAGGER_API_URL)
    def spec():
        return jsonify(build_swagger(app))

    from app.db import db
    from app.migrate import migrate
    from app.jwt import jwt


    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    with app.app_context():
        db.create_all()

    from app import expense
    from app import user
    app.register_blueprint(expense.bp)
    app.register_blueprint(user.bp)
    app.register_blueprint(swagger_ui_blueprint)

    return app