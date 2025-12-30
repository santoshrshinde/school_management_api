CREATE DATABASE IF NOT EXISTS student_db;
USE student_db;

-- 1. Stds Table (formerly Student)
CREATE TABLE Stds (
    StudentID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(100) UNIQUE,
    DateOfBirth DATE,
    Address TEXT
);

-- 2. Course Table
CREATE TABLE Course (
    CourseID INT PRIMARY KEY AUTO_INCREMENT,
    CourseName VARCHAR(100)
);

-- 3. Admission Table
CREATE TABLE Admission (
    AdmissionID INT PRIMARY KEY AUTO_INCREMENT,
    StudentID INT,
    AdmissionDate DATE,
    Status VARCHAR(50),
    CourseID INT,
    FOREIGN KEY (StudentID) REFERENCES Stds(StudentID),
    FOREIGN KEY (CourseID) REFERENCES Course(CourseID)
);

-- 4. Attendance Table
CREATE TABLE Attendance (
    AttendanceID INT PRIMARY KEY AUTO_INCREMENT,
    StudentID INT,
    Date DATE,
    Status VARCHAR(10),
    FOREIGN KEY (StudentID) REFERENCES Stds(StudentID)
);

-- 5. Fees Table
CREATE TABLE Fees (
    FeeID INT PRIMARY KEY AUTO_INCREMENT,
    StudentID INT,
    Amount DECIMAL(10,2),
    DueDate DATE,
    PaidAmount DECIMAL(10,2),
    TotalFee DECIMAL(10,2),
    FOREIGN KEY (StudentID) REFERENCES Stds(StudentID)
);

-- 6. SchoolBus Table
CREATE TABLE SchoolBus (
    BusID INT PRIMARY KEY AUTO_INCREMENT,
    BusNumber VARCHAR(20),
    Driver VARCHAR(100)
);

-- 7. StudentBus Table
CREATE TABLE StudentBus (
    StudentBusID INT PRIMARY KEY AUTO_INCREMENT,
    StudentID INT,
    BusID INT,
    FOREIGN KEY (StudentID) REFERENCES Stds(StudentID),
    FOREIGN KEY (BusID) REFERENCES SchoolBus(BusID)
);

-- 8. Library Table
CREATE TABLE Library (
    BookID INT PRIMARY KEY AUTO_INCREMENT,
    BookName VARCHAR(100),
    Author VARCHAR(100),
    Publisher VARCHAR(100),
    TotalQuantity INT,
    AvailableQuantity INT
);

-- 9. BookIssue Table
CREATE TABLE BookIssue (
    IssueID INT PRIMARY KEY AUTO_INCREMENT,
    StudentID INT,
    BookID INT,
    IssueDate DATE,
    ReturnDate DATE,
    Status VARCHAR(20),
    FOREIGN KEY (StudentID) REFERENCES Stds(StudentID),
    FOREIGN KEY (BookID) REFERENCES Library(BookID)
);

-- 10. Teacher Table
CREATE TABLE Teacher (
    TeacherID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(100),
    Subject VARCHAR(100),
    Contact VARCHAR(15)
);

-- 11. Timetable Table
CREATE TABLE Timetable (
    TimetableID INT PRIMARY KEY AUTO_INCREMENT,
    CourseID INT,
    Day VARCHAR(20),
    TimeSlot VARCHAR(50),
    Subject VARCHAR(100),
    TeacherID INT,
    FOREIGN KEY (CourseID) REFERENCES Course(CourseID),
    FOREIGN KEY (TeacherID) REFERENCES Teacher(TeacherID)
);

-- 12. Exam Table
CREATE TABLE Exam (
    ExamID INT PRIMARY KEY AUTO_INCREMENT,
    CourseID INT,
    Subject VARCHAR(100),
    ExamDate DATE,
    TotalMarks INT,
    FOREIGN KEY (CourseID) REFERENCES Course(CourseID)
);

-- 13. Result Table
CREATE TABLE Result (
    ResultID INT PRIMARY KEY AUTO_INCREMENT,
    StudentID INT,
    ExamID INT,
    MarksObtained INT,
    Grade VARCHAR(10),
    FOREIGN KEY (StudentID) REFERENCES Stds(StudentID),
    FOREIGN KEY (ExamID) REFERENCES Exam(ExamID)
);

-- 1. Stds (Student)
INSERT INTO Stds (Name, DateOfBirth, Address)
VALUES ('Atharv Shinde', '2006-04-15', 'Pune');
SELECT * FROM Stds;

-- 2. Course
INSERT INTO Course (CourseName)
VALUES ('BSc Computer Science');
SELECT * FROM Course;

-- 3. Admission
INSERT INTO Admission (StudentID, AdmissionDate, Status, CourseID)
VALUES (1, '2023-06-01', 'Active', 1);
SELECT * FROM Admission;

-- 4. Attendance
INSERT INTO Attendance (StudentID, Date, Status)
VALUES (1, '2024-07-08', 'Present');
SELECT * FROM Attendance;

-- 5. Fees
INSERT INTO Fees (StudentID, Amount, DueDate, PaidAmount, TotalFee)
VALUES (1, 5000.00, '2024-08-01', 3000.00, 5000.00);
SELECT * FROM Fees;

-- 6. SchoolBus
INSERT INTO SchoolBus (BusNumber, Driver)
VALUES ('MH12AB1234', 'Ramesh Patil');
SELECT * FROM SchoolBus;

-- 7. StudentBus
INSERT INTO StudentBus (StudentID, BusID)
VALUES (1, 1);
SELECT * FROM StudentBus;

-- 8. Library
INSERT INTO Library (BookName, Author, Publisher, TotalQuantity, AvailableQuantity)
VALUES ('Python Programming', 'Guido van Rossum', 'OReilly', 10, 9);
SELECT * FROM Library;

-- 9. BookIssue
INSERT INTO BookIssue (StudentID, BookID, IssueDate, ReturnDate, Status)
VALUES (1, 1, '2024-07-01', NULL, 'Issued');
SELECT * FROM BookIssue;

-- 10. Teacher
INSERT INTO Teacher (Name, Subject, Contact)
VALUES ('Dr. Rane', 'Computer Science', '9876543210');
SELECT * FROM Teacher;

-- 11. Timetable
INSERT INTO Timetable (CourseID, Day, TimeSlot, Subject, TeacherID)
VALUES (1, 'Monday', '10:00-11:00', 'Computer Science', 1);
SELECT * FROM Timetable;

-- 12. Exam
INSERT INTO Exam (CourseID, Subject, ExamDate, TotalMarks)
VALUES (1, 'Computer Science', '2024-07-15', 100);
SELECT * FROM Exam;

-- 13. Result
INSERT INTO Result (StudentID, ExamID, MarksObtained, Grade)
VALUES (1, 1, 88, 'A');
SELECT * FROM Result;

SELECT * FROM Stds;
SELECT * FROM Course;


INSERT INTO Stds (Name, DateOfBirth, Address)
VALUES 
('Atharv', '2005-08-15', 'Pune'),
('Prasad', '2004-12-01', 'Nashik');
 select * from Course;
 select * from Stds;
 
ALTER TABLE Attendance
ADD COLUMN CourseID INT;

ALTER TABLE Attendance
ADD CONSTRAINT fk_att_course
FOREIGN KEY (CourseID) REFERENCES Course(CourseID);

SHOW TABLES;

select * from Attendance;

