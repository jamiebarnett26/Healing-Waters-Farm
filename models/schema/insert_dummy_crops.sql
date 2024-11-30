BEGIN;

-- Insert Family 1
INSERT INTO family (family_name) VALUES ('Peppers, Hot');

-- Insert Species 1
INSERT INTO species (family_id, latin_name, species_name) VALUES (1, 'Capsicum baccatum', 'Baccatum');

-- Insert Variety 1
INSERT INTO variety (species_id, variety_name) VALUES (1, 'Aji Amarillo');

-- Insert Crop_Info 1
INSERT INTO crop_infos 
(variety_id, crop_type, template, days_to_maturity, plant_spacing_harvest, plant_spacing_seed, row_spacing_harvest, row_spacing_seed, days_to_maturity_harvest, days_to_maturity_seed, days_to_transplantation, days_to_direct_sow, days_to_harvest, days_to_seed_harvest, frost_sensitivity_rating) 
VALUES (1, NULL, true, 20, NULL, NULL, NULL, NULL, 20, 20, 20, 20, 20, 20, 2);

-- Insert Species 2
INSERT INTO species (family_id, latin_name, species_name) VALUES (1, 'Capsicum Annum', 'Annum');

-- Insert Variety 2
INSERT INTO variety (species_id, variety_name) VALUES (2, 'Fish Peppers');

-- Insert Crop_Info 2
INSERT INTO crop_infos 
(variety_id, crop_type, template, days_to_maturity, plant_spacing_harvest, plant_spacing_seed, row_spacing_harvest, row_spacing_seed, days_to_maturity_harvest, days_to_maturity_seed, days_to_transplantation, days_to_direct_sow, days_to_harvest, days_to_seed_harvest, frost_sensitivity_rating) 
VALUES (2, NULL, true, 20, NULL, NULL, NULL, NULL, 20, 20, 20, 20, 20, 20, 2);

-- Insert Species 3
INSERT INTO species (family_id, latin_name, species_name) VALUES (1, 'Capsicum Chinense', 'Chinense');

-- Insert Variety 3
INSERT INTO variety (species_id, variety_name) VALUES (3, 'Red Scotch Bonnet');

-- Insert Crop_Info 3
INSERT INTO crop_infos 
(variety_id, crop_type, template, days_to_maturity, plant_spacing_harvest, plant_spacing_seed, row_spacing_harvest, row_spacing_seed, days_to_maturity_harvest, days_to_maturity_seed, days_to_transplantation, days_to_direct_sow, days_to_harvest, days_to_seed_harvest, frost_sensitivity_rating) 
VALUES (3, NULL, true, 20, NULL, NULL, NULL, NULL, 20, 20, 20, 20, 20, 20, 2);

-- Insert Family 2
INSERT INTO family (family_name) VALUES ('Beans');

-- Insert Species 4
INSERT INTO species (family_id, latin_name, species_name) VALUES (2, 'Phaseolus vulgaris', 'Vulgaris');

-- Insert Variety 4
INSERT INTO variety (species_id, variety_name) VALUES (4, 'Mbombo Beans');

-- Insert Crop_Info 4
INSERT INTO crop_infos 
(variety_id, crop_type, template, days_to_maturity, plant_spacing_harvest, plant_spacing_seed, row_spacing_harvest, row_spacing_seed, days_to_maturity_harvest, days_to_maturity_seed, days_to_transplantation, days_to_direct_sow, days_to_harvest, days_to_seed_harvest, frost_sensitivity_rating) 
VALUES (4, NULL, true, 20, NULL, NULL, NULL, NULL, 20, 20, 20, 20, 20, 20, 2);

COMMIT;
