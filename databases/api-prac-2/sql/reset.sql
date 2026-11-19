-- Puts the data back to the seed state WITHOUT dropping the tables.
-- The tests run this before and after every test.
-- RESTART IDENTITY makes ids start at 1 again, so seed ids are always 1 to 4 / 1 to 8.
truncate fastapi_practice.students, fastapi_practice.courses restart identity;

insert into fastapi_practice.courses (name) values
    ('Programming'), ('Networking'), ('Cyber Security'), ('Web Development');

insert into fastapi_practice.students (name, course_id) values
    ('Alice Chen', 1), ('Ben Carter', 1), ('Chloe Nguyen', 2), ('Daniel Smith', 2),
    ('Emma Wilson', 3), ('Farid Khan', 3), ('Grace Lee', 4), ('Harry Brown', 4);
