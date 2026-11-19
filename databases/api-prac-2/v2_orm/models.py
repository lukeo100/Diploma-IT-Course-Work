"""ORM models: Python classes that map to the existing tables.
These do NOT create tables. The tables already exist in Supabase (see sql/schema.sql),
so we never call Base.metadata.create_all()."""
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

# The tables live in their own schema, not "public"
SCHEMA = "fastapi_practice"


class Base(DeclarativeBase):
    """Every ORM class inherits from this so SQLAlchemy can track them."""


class Course(Base):
    __tablename__ = "courses"
    __table_args__ = {"schema": SCHEMA}

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))  # Mapped[str] (not Optional) = NOT NULL

    # The "one" side: course.students is a list of Student objects.
    # back_populates links this to Student.course so both sides stay in sync.
    students: Mapped[list["Student"]] = relationship(back_populates="course")


class Student(Base):
    __tablename__ = "students"
    __table_args__ = {"schema": SCHEMA}

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    # The foreign key column that actually exists in the table
    course_id: Mapped[int] = mapped_column(ForeignKey(f"{SCHEMA}.courses.id"))

    # The "many" side: student.course is ONE Course object.
    # Use student.course.name to read the course name. SQLAlchemy runs the JOIN/lookup for us.
    course: Mapped["Course"] = relationship(back_populates="students")
