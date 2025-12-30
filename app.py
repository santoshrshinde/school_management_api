from flask import Flask
from flask_cors import CORS
from extensions import db
from config import SQLALCHEMY_DATABASE_URI

def create_app():
    app = Flask(__name__)
    app.url_map.strict_slashes = False

    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

    db.init_app(app)

    with app.app_context():

        # Import models
        from models import (
            Student, Teacher, Course, SchoolBus, Library, Admission,
            Attendance, Fees, StudentBus, BookIssue,
            Timetable, Exam, Result
        )

        db.create_all()

        # Import blueprints
        from routes.student import bp as student_bp
        from routes.teacher import bp as teacher_bp
        from routes.course import bp as course_bp
        from routes.schoolbus import bp as schoolbus_bp
        from routes.library import bp as library_bp
        from routes.admission import bp as admission_bp
        from routes.attendance import bp as attendance_bp
        from routes.fees import bp as fees_bp
        from routes.studentbus import bp as studentbus_bp
        from routes.bookissue import bp as bookissue_bp
        from routes.timetable import bp as timetable_bp
        from routes.exam import bp as exam_bp
        from routes.result import bp as result_bp
        from routes.dashboard import dashboard_bp   # ✅ DASHBOARD

        # Register blueprints
        app.register_blueprint(student_bp)
        app.register_blueprint(teacher_bp)
        app.register_blueprint(course_bp)
        app.register_blueprint(schoolbus_bp)
        app.register_blueprint(library_bp)
        app.register_blueprint(admission_bp)
        app.register_blueprint(attendance_bp)
        app.register_blueprint(fees_bp)
        app.register_blueprint(studentbus_bp)
        app.register_blueprint(bookissue_bp)
        app.register_blueprint(timetable_bp)
        app.register_blueprint(exam_bp)
        app.register_blueprint(result_bp)
        app.register_blueprint(dashboard_bp)        # ✅ DASHBOARD

        @app.route('/')
        def home():
            return "✅ 🎇🎉 School Management API is running!"

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
