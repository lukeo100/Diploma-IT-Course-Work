"""
Version 2: FastAPI + SQLAlchemy ORM (Psycopg 3 is the driver underneath).

Run from the project root:
    fastapi dev v2_orm/main.py
Swagger UI: http://127.0.0.1:8000/docs
"""
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from .database import get_db
from .models import Course, Student
from .schemas import CourseOut, StudentCreate, StudentOut, StudentWithCourse

app = FastAPI(title="Students API (v2: SQLAlchemy ORM)")


def with_course(student: Student) -> StudentWithCourse:
    """Build the response for GET. student.course is the relationship:
    reading .name from it needs no hand-written JOIN."""
    return StudentWithCourse(id=student.id, name=student.name, course=student.course.name)


def get_student_or_404(db: Session, student_id: int) -> Student:
    """db.get() looks a row up by primary key. It returns None when there is no match."""
    student = db.get(Student, student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


def check_course_exists(db: Session, course_id: int) -> None:
    """Friendly 400 instead of a database foreign key error."""
    if db.get(Course, course_id) is None:
        raise HTTPException(status_code=400, detail="course_id does not exist")


@app.get("/courses", response_model=list[CourseOut])
def list_courses(db: Session = Depends(get_db)):
    """All courses, ordered by id. select(Course) builds "SELECT ... FROM courses"."""
    # db.scalars() returns the Course objects themselves (not rows of columns)
    return db.scalars(select(Course).order_by(Course.id)).all()


@app.get("/students", response_model=list[StudentWithCourse])
def list_students(db: Session = Depends(get_db)):
    """All students with their course name."""
    # selectinload fetches every needed Course in ONE extra query up front.
    # Without it, reading student.course for 8 students would fire 8 separate queries
    # ("lazy loading", the N+1 problem). The result is the same, it is just faster.
    students = db.scalars(
        select(Student).options(selectinload(Student.course)).order_by(Student.id)
    ).all()
    return [with_course(s) for s in students]


@app.get("/students/{student_id}", response_model=StudentWithCourse)
def get_student(student_id: int, db: Session = Depends(get_db)):
    """One student. Here student.course is lazy loaded the first time it is read."""
    return with_course(get_student_or_404(db, student_id))


@app.post("/students", response_model=StudentOut, status_code=201)
def create_student(data: StudentCreate, db: Session = Depends(get_db)):
    """Create a student. The JSON body is validated against StudentCreate first."""
    check_course_exists(db, data.course_id)
    student = Student(name=data.name, course_id=data.course_id)  # a plain Python object so far
    db.add(student)      # stage it in the session (nothing sent to the database yet)
    db.commit()          # run the INSERT and make it permanent
    db.refresh(student)  # reload from the database so student.id (generated there) is filled in
    return student


@app.put("/students/{student_id}", response_model=StudentOut)
def update_student(student_id: int, data: StudentCreate, db: Session = Depends(get_db)):
    """Replace a student's name and course."""
    student = get_student_or_404(db, student_id)
    check_course_exists(db, data.course_id)
    # Just change the attributes. The session notices the change and
    # writes an UPDATE when we commit.
    student.name = data.name
    student.course_id = data.course_id
    db.commit()
    db.refresh(student)
    return student


@app.delete("/students/{student_id}", response_model=StudentOut)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    """Delete a student and return the deleted record."""
    student = get_student_or_404(db, student_id)
    # Copy the data BEFORE deleting: after the commit the object no longer
    # has a row behind it, so reading its attributes would fail.
    deleted = StudentOut.model_validate(student)
    db.delete(student)
    db.commit()
    return deleted
