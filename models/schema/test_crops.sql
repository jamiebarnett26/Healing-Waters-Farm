INSERT INTO crop_information (
    latin_name, family, species, type, variety, template, seed_spacing_inches, row_spacing_inches, 
    seed_spacing_harvest, row_spacing_harvest, days_to_maturity, 
    days_to_seed_maturity, days_to_transplantation, days_to_direct_sow, 
    days_to_harvest, days_to_seed_harvest, indoor_seed_starting_date, 
    transplanting_date, direct_sow_date, harvest_date, seed_harvest_date, 
    frost_sensitivity_rating
) VALUES 
(
    'Solanum lycopersicum', 'Tomato Family', 'Tomato Species', 'Tomato', 'Beefsteak', True, 18, 24, 12, 36, 70, 
    80, 0, 0, 80, 0, '2024-02-15', '2024-05-01', NULL, '2024-07-15', NULL, 3
),
(
    'Daucus carota', 'Carrot Family', 'Carrot Species', 'Carrot', 'Imperator', True, 2, 12, 2, 12, 70, 
    70, 0, 0, 70, 0, NULL, NULL, '2024-03-15', '2024-07-01', NULL, 2
);