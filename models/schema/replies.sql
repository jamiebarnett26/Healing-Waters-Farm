DROP TABLE IF EXISTS replies;

create table replies
(
    reply_id          serial primary key,
    user_id              integer,
    user_name     varchar(255) not null,
    question_id              integer,
    text          text not null,
    created_at           timestamp default current_timestamp,
    updated_at           timestamp default current_timestamp
);
