DROP TABLE IF EXISTS announcements;

create table announcements
(
    announcement_id          serial primary key,
    user_id              integer,
    user_name     varchar(255) not null,
    title         varchar(255) not null,
    text          text not null,
    created_at           timestamp default current_timestamp,
    updated_at           timestamp default current_timestamp
);
