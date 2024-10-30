/* Family 1 Peppers, Hot */
INSERT INTO family (family_name) VALUES ('Peppers, Hot');

/* Species 1, Capsicum Baccatum, Peppers Hot */
INSERT INTO species (family_id, latin_name, species_name) VALUES (1, 'Capsicum baccatum', 'Baccatum');

/* Variety 1, Aji Amarillo, Capsicum Baccatum */
INSERT INTO variety (species_id, variety_name) VALUES (1, 'Aji Amarillo');

/* Crop_Info 1, Aji Amarillo */
INSERT INTO crop_infos 
(variety_id, crop_type, template, days_to_maturity, plant_spacing_harvest, plant_spacing_seed, row_spacing_harvest, row_spacing_seed, days_to_maturity_harvest, days_to_maturity_seed, days_to_transplantation, days_to_direct_sow, days_to_harvest, days_to_seed_harvest, frost_sensitivity_rating) 
VALUES (1, NULL, true, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);

/* Species 2, Capsicum Annum, Peppers Hot */
INSERT INTO species (family_id, latin_name, species_name) VALUES (1, 'Capsicum Annum', 'Annum');

/* Variety 2, Fish Peppers, Capsicum Annum */
INSERT INTO variety (species_id, variety_name) VALUES (2, 'Fish Peppers');

/* Crop_Info 2, Fish Peppers */
INSERT INTO crop_infos 
(variety_id, crop_type, template, days_to_maturity, plant_spacing_harvest, plant_spacing_seed, row_spacing_harvest, row_spacing_seed, days_to_maturity_harvest, days_to_maturity_seed, days_to_transplantation, days_to_direct_sow, days_to_harvest, days_to_seed_harvest, frost_sensitivity_rating) 
VALUES (2, NULL, true, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);

/* Species 3, Capsicum Chinense, Peppers Hot */
INSERT INTO species (family_id, latin_name, species_name) VALUES (1, 'Capsicum Chinense', 'Chinense');

/* Variety 3, Red Scotch Bonnet, Capsicum Chinense */
INSERT INTO variety (species_id, variety_name) VALUES (3, 'Red Scotch Bonnet');

/* Crop_Info 3, Red Scotch Bonnet */
INSERT INTO crop_infos 
(variety_id, crop_type, template, days_to_maturity, plant_spacing_harvest, plant_spacing_seed, row_spacing_harvest, row_spacing_seed, days_to_maturity_harvest, days_to_maturity_seed, days_to_transplantation, days_to_direct_sow, days_to_harvest, days_to_seed_harvest, frost_sensitivity_rating) 
VALUES (3, NULL, true, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);

/* Family 2 Beans */
INSERT INTO family (family_name) VALUES ('Beans');

/* Species 4, Phaseolus vulgaris, Beans */
INSERT INTO species (family_id, latin_name, species_name) VALUES (2, 'Phaseolus vulgaris', 'Vulgaris');

/* Variety 4, Mbombo Beans, Phaseolus Vulgaris */
INSERT INTO variety (species_id, variety_name) VALUES (4, 'Mbombo Beans');

/* Crop_Info 4, Mbombo Beans */
INSERT INTO crop_infos 
(variety_id, crop_type, template, days_to_maturity, plant_spacing_harvest, plant_spacing_seed, row_spacing_harvest, row_spacing_seed, days_to_maturity_harvest, days_to_maturity_seed, days_to_transplantation, days_to_direct_sow, days_to_harvest, days_to_seed_harvest, frost_sensitivity_rating) 
VALUES (4, NULL, true, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);
