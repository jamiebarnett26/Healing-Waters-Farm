DROP TABLE IF EXISTS admin;

create table admin
(
    admin_id           serial primary key,
    user_id            integer
);

INSERT INTO admin (user_id) VALUES (1);
INSERT INTO admin (user_id) VALUES (2);
INSERT INTO admin (user_id) VALUES (3);
INSERT INTO admin (user_id) VALUES (4);
INSERT INTO admin (user_id) VALUES (5);
INSERT INTO admin (user_id) VALUES (6);
INSERT INTO admin (user_id) VALUES (7);
INSERT INTO admin (user_id) VALUES (8);
INSERT INTO admin (user_id) VALUES (9);
INSERT INTO admin (user_id) VALUES (10);
INSERT INTO admin (user_id) VALUES (11);
INSERT INTO admin (user_id) VALUES (12);