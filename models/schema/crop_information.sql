DROP TABLE IF EXISTS crop_information;

CREATE TABLE crop_information
(
    crop_id                   serial
        primary key,
    latin_name                varchar(255),
    variety                   varchar(255),
    type                      varchar(100),
    template                  boolean,
    seed_spacing_inches       integer,
    row_spacing_inches        integer,
    seed_spacing_harvest      integer,
    row_spacing_harvest       integer,
    days_to_maturity          integer,
    days_to_seed_maturity     integer,
    days_to_transplantation   integer,
    days_to_direct_sow        integer,
    days_to_harvest           integer,
    days_to_seed_harvest      integer,
    indoor_seed_starting_date date,
    transplanting_date        date,
    direct_sow_date           date,
    harvest_date              date,
    seed_harvest_date         date,
    frost_sensitivity_rating  integer
);

