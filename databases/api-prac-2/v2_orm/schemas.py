"""Pydantic schemas: describe the JSON that goes IN and OUT of the API.
They are separate from the ORM models in models.py, which describe database tables."""
from pydantic import BaseModel, ConfigDict


class StudentCreate(BaseModel):
    """Request body for POST and PUT /students."""
    name: str
    course_id: int


class CourseOut(BaseModel):
    id: int
    name: str
    # Lets Pydantic read attributes straight from an ORM object (course.id, course.name)
    model_config = ConfigDict(from_attributes=True)


class StudentOut(BaseModel):
    """A student as stored in the table (used by POST, PUT, DELETE)."""
    id: int
    name: str
    course_id: int
    model_config = ConfigDict(from_attributes=True)


class StudentWithCourse(BaseModel):
    """A student with the course NAME instead of course_id (used by the GET endpoints).
    Same shape as v1, so both versions return identical JSON."""
    id: int
    name: str
    course: str
