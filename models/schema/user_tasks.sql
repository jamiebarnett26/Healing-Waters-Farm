-- DROP TABLE IF EXISTS users;

-- CREATE TABLE users
-- (
--     user_id    serial
--         primary key,
--     first_name varchar(50)  not null,
--     last_name  varchar(50)  not null,
--     email      varchar(100) not null
--         unique
-- );

DROP TABLE IF EXISTS tasks;

CREATE TABLE tasks
(
    task_id      serial
        primary key,
    user_crop_id integer,
    user_id      integer,
    task_name    varchar(255),
    task_date    date,
    completed    boolean
);
