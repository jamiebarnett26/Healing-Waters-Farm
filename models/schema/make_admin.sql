DROP TABLE IF EXISTS admin;

create table admin
(
    admin_id           serial primary key,
    user_id            integer
);

INSERT INTO admin (user_id) VALUES (1);
INSERT INTO admin (user_id) VALUES (2);