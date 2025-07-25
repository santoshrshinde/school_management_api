from extensions import db

class Student(db.Model):
    __tablename__ = 'Stds'
    StudentID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100), unique=True)
    DateOfBirth = db.Column(db.Date)
    Address = db.Column(db.Text)

class Teacher(db.Model):
    __tablename__ = 'Teacher'
    TeacherID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100))
    Subject = db.Column(db.String(100))
    Contact = db.Column(db.String(15))

class Course(db.Model):
    __tablename__ = 'Course'
    CourseID = db.Column(db.Integer, primary_key=True)
    CourseName = db.Column(db.String(100))

