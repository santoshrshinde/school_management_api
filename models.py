# from app import db

# class Student(db.Model):
#     __tablename__ = 'student'
#     StudentID = db.Column(db.Integer, primary_key=True)
#     Name = db.Column(db.String(100))
#     DateOfBirth = db.Column(db.Date)
#     Address = db.Column(db.Text)

# class Teacher(db.Model):
#     __tablename__ = 'teacher'
#     TeacherID = db.Column(db.Integer, primary_key=True)
#     Name = db.Column(db.String(100))
#     Subject = db.Column(db.String(100))
#     Contact = db.Column(db.String(15))

# class Course(db.Model):
#     __tablename__ = 'course'
#     CourseID = db.Column(db.Integer, primary_key=True)
#     CourseName = db.Column(db.String(100))

from extensions import db

class Student(db.Model):
    __tablename__ = 'student'
    StudentID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100))
    DateOfBirth = db.Column(db.Date)
    Address = db.Column(db.Text)

class Teacher(db.Model):
    __tablename__ = 'teacher'
    TeacherID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100))
    Subject = db.Column(db.String(100))
    Contact = db.Column(db.String(15))

class Course(db.Model):
    __tablename__ = 'course'
    CourseID = db.Column(db.Integer, primary_key=True)
    CourseName = db.Column(db.String(100))
