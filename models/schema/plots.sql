DROP TABLE IF EXISTS crop_information;

create table plots
(
    plot_id             serial
        primary key,
    garden_zone         varchar(5) not null,
    average_first_frost date,
    average_last_frost  date
);

