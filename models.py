from extensions import db

class Student(db.Model):
    __tablename__ = 'Stds'
    StudentID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.String(100), unique=True, nullable=False)
    DateOfBirth = db.Column(db.Date, nullable=False)
    Address = db.Column(db.Text, nullable=True)

class Teacher(db.Model):
    __tablename__ = 'Teacher'
    TeacherID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.String(100), nullable=False)
    Subject = db.Column(db.String(100))
    Contact = db.Column(db.String(15))

class Course(db.Model):
    __tablename__ = 'Course'
    CourseID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    CourseName = db.Column(db.String(100), nullable=False)

class SchoolBus(db.Model):
    __tablename__ = 'SchoolBus'
    BusID = db.Column(db.Integer, primary_key=True)
    BusNumber = db.Column(db.String(20), nullable=False)
    Driver = db.Column(db.String(100), nullable=False)

class Library(db.Model):
    __tablename__ = 'Library'
    BookID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    BookName = db.Column(db.String(100))
    Author = db.Column(db.String(100))
    Publisher = db.Column(db.String(100))
    TotalQuantity = db.Column(db.Integer)
    AvailableQuantity = db.Column(db.Integer)

class Admission(db.Model):
    __tablename__ = 'Admission'
    AdmissionID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    StudentID = db.Column(db.Integer, db.ForeignKey('Stds.StudentID'), nullable=False)
    AdmissionDate = db.Column(db.Date, nullable=False)
    Status = db.Column(db.String(50), nullable=False)
    CourseID = db.Column(db.Integer, db.ForeignKey('Course.CourseID'), nullable=False)

    student = db.relationship("Student", backref="admissions")
    course = db.relationship("Course", backref="admissions")

from extensions import db

class Attendance(db.Model):
    __tablename__ = 'Attendance'
    AttendanceID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    StudentID = db.Column(db.Integer, db.ForeignKey('Stds.StudentID'))
    Date = db.Column(db.Date)
    Status = db.Column(db.String(10))
    
    # ✅ New CourseID column
    CourseID = db.Column(db.Integer, db.ForeignKey('Course.CourseID'))
    
    # Optional: relationship
    student = db.relationship('Student', backref='attendances')
    course = db.relationship('Course', backref='attendances')


class Fees(db.Model):
    __tablename__ = 'Fees'
    FeeID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    StudentID = db.Column(db.Integer, db.ForeignKey('Stds.StudentID'), nullable=False)
    Amount = db.Column(db.Numeric(10, 2), nullable=False)
    DueDate = db.Column(db.Date, nullable=False)
    PaidAmount = db.Column(db.Numeric(10, 2), nullable=False)
    TotalFee = db.Column(db.Numeric(10, 2), nullable=False)

    student = db.relationship("Student", backref="fees")

class StudentBus(db.Model):
    __tablename__ = 'StudentBus' 
    StudentBusID = db.Column(db.Integer, primary_key=True)
    StudentID = db.Column(db.Integer, db.ForeignKey('Stds.StudentID'))
    BusID = db.Column(db.Integer, db.ForeignKey('SchoolBus.BusID'))

class BookIssue(db.Model):
    __tablename__ = 'BookIssue'
    IssueID = db.Column(db.Integer, primary_key=True)
    StudentID = db.Column(db.Integer, db.ForeignKey('Stds.StudentID'))
    BookID = db.Column(db.Integer, db.ForeignKey('Library.BookID'))
    IssueDate = db.Column(db.Date)
    ReturnDate = db.Column(db.Date)
    Status = db.Column(db.String(20))

class Timetable(db.Model):
    __tablename__ = 'Timetable'
    TimetableID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    CourseID = db.Column(db.Integer, db.ForeignKey('Course.CourseID'))
    Day = db.Column(db.String(20))
    TimeSlot = db.Column(db.String(50))
    Subject = db.Column(db.String(100))
    TeacherID = db.Column(db.Integer, db.ForeignKey('Teacher.TeacherID'))

    course = db.relationship('Course', backref=db.backref('timetables', lazy=True))
    teacher = db.relationship('Teacher', backref=db.backref('timetables', lazy=True))

class Exam(db.Model):
    __tablename__ = 'Exam'
    ExamID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    CourseID = db.Column(db.Integer, db.ForeignKey('Course.CourseID'), nullable=False)
    Subject = db.Column(db.String(100), nullable=False)
    ExamDate = db.Column(db.Date, nullable=False)
    TotalMarks = db.Column(db.Integer, nullable=False)

    course = db.relationship('Course', backref=db.backref('exams', lazy=True))

class Result(db.Model):
    __tablename__ = 'Result'
    ResultID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    StudentID = db.Column(db.Integer, db.ForeignKey('Stds.StudentID'), nullable=False)
    ExamID = db.Column(db.Integer, db.ForeignKey('Exam.ExamID'), nullable=False)
    MarksObtained = db.Column(db.Integer, nullable=False)
    Grade = db.Column(db.String(10), nullable=False)

    student = db.relationship('Student', backref='results')
    exam = db.relationship('Exam', backref='results')
