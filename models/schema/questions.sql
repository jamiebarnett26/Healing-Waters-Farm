DROP TABLE IF EXISTS questions;

create table questions
(
    question_id          serial primary key,
    user_id              integer,
    title         varchar(255) not null,
    text          text not null,
    status        varchar(50) not null,
    created_at           timestamp default current_timestamp,
    updated_at           timestamp default current_timestamp
);
