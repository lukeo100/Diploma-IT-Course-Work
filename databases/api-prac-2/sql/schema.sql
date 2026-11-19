-- Full setup script for the FastAPI practice schema.
-- Already applied to the Supabase "Learning" project as the migration
-- "fastapi_practice_schema". Safe to re-run: it drops and recreates both tables.
-- Uses its own schema so the shared "public" schema is not touched.

create schema if not exists fastapi_practice;

-- Drop the child table first because students depends on courses
drop table if exists fastapi_practice.students;
drop table if exists fastapi_practice.courses;

create table fastapi_practice.courses (
    id   integer generated always as identity primary key,
    name varchar(100) not null
);

-- One course has many students (one-to-many via the foreign key)
create table fastapi_practice.students (
    id        integer generated always as identity primary key,
    name      varchar(100) not null,
    course_id integer not null references fastapi_practice.courses (id)
);

insert into fastapi_practice.courses (name) values
    ('Programming'), ('Networking'), ('Cyber Security'), ('Web Development');

insert into fastapi_practice.students (name, course_id) values
    ('Alice Chen', 1), ('Ben Carter', 1), ('Chloe Nguyen', 2), ('Daniel Smith', 2),
    ('Emma Wilson', 3), ('Farid Khan', 3), ('Grace Lee', 4), ('Harry Brown', 4);

-- Direct Postgres connections bypass RLS; this only blocks the public Data API
alter table fastapi_practice.courses  enable row level security;
alter table fastapi_practice.students enable row level security;
