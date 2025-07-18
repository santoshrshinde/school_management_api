from flask import Flask
from config import SQLALCHEMY_DATABASE_URI
from extensions import db

def create_app():
    app = Flask(__name__)
    app.config.from_object('config')

    db.init_app(app)

    with app.app_context():
        # Import models to register them with SQLAlchemy
        from models import Student, Teacher, Course  # Add others as needed

        # Import blueprints
        from routes import student, teacher, course
        app.register_blueprint(student.bp)
        app.register_blueprint(teacher.bp)
        app.register_blueprint(course.bp)

        # Optional: only if you're creating tables (be careful with existing db)
        # db.create_all()

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
