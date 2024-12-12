DROP TABLE IF EXISTS family;
DROP TABLE IF EXISTS species;
DROP TABLE IF EXISTS variety;
DROP TABLE IF EXISTS crop_type;
DROP TABLE IF EXISTS crop_infos;

create table family
(
    family_id           serial primary key,
    family_name         varchar(255) not null
);
create table species
(
    species_id           serial primary key,
    family_id            integer,
    latin_name           varchar(255) not null,
    species_name         varchar(255) not null
);
create table variety
(
    variety_id           serial primary key,
    species_id           integer,
    variety_name         varchar(255) not null
);
create table crop_infos
(
    crop_info_id         serial primary key,
    variety_id         integer not null,
    user_id                   integer,
    crop_type                 varchar(255),
    days_to_maturity          integer,
    plant_spacing_harvest     integer,
    plant_spacing_seed        integer,
    row_spacing_harvest       integer,
    row_spacing_seed          integer,
    days_to_maturity_harvest  integer,
    days_to_maturity_seed     integer,
    days_to_transplantation   integer,
    days_to_direct_sow        integer,
    days_to_harvest           integer,
    days_to_seed_harvest      integer,
    frost_sensitivity_rating  integer
);


