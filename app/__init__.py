from flask import Flask


def create_app():
    app = Flask(__name__)

    from .routes.students import students_bp
    from .error_handlers import errors_bp

    app.register_blueprint(students_bp)
    app.register_blueprint(errors_bp)

    return app
