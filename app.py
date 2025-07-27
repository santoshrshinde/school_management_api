from flask import Flask
from extensions import db
from config import SQLALCHEMY_DATABASE_URI
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 🔥 Wide-open CORS for debugging — DON'T use in production
    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

    db.init_app(app)

    with app.app_context():
        from models import Student, Teacher, Course
        db.create_all()

        from routes.student import bp as student_bp
        from routes.teacher import bp as teacher_bp
        from routes.course import bp as course_bp

        app.register_blueprint(student_bp)
        app.register_blueprint(teacher_bp)
        app.register_blueprint(course_bp)

        @app.route('/')
        def home():
            return "✅ School Management API is running!"

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
