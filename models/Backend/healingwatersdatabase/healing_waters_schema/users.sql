create table users
(
    user_id         serial
        primary key,
    plot_id         integer
        constraint "users_plots(plot_id)"
            references plots,
    role            varchar(50),
    username        varchar(100) not null
        unique,
    email           varchar(255) not null
        unique,
    hashed_password varchar(255) not null,
    first_name      varchar(100),
    last_name       varchar(100)
);

