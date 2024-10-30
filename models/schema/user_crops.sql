DROP TABLE IF EXISTS user_crops;

CREATE TABLE user_crops
(
    user_crop_id                   serial
        primary key,
    user_id                   integer,
    crop_info_id              integer,
    indoor_seed_starting_date date,
    transplanting_date        date,
    direct_sow_date           date,
    harvest_date              date,
    seed_harvest_date         date
);

