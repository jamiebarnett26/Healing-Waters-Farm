BEGIN;

-- Families
INSERT INTO family (family_name) VALUES ('African Pea');
INSERT INTO family (family_name) VALUES ('Beans');
INSERT INTO family (family_name) VALUES ('Beets');
INSERT INTO family (family_name) VALUES ('Collards');
INSERT INTO family (family_name) VALUES ('Okra');
INSERT INTO family (family_name) VALUES ('Peppers, Hot');
INSERT INTO family (family_name) VALUES ('Radish');
INSERT INTO family (family_name) VALUES ('Sorghum');
INSERT INTO family (family_name) VALUES ('Squash');
INSERT INTO family (family_name) VALUES ('Tomatos');

-- Species

INSERT INTO species (family_id, latin_name, species_name)
VALUES ((SELECT family_id FROM family WHERE family_name = 'African Pea'), 'Vigna unguiculata', 'Unguiculata');

INSERT INTO species (family_id, latin_name, species_name)
VALUES ((SELECT family_id FROM family WHERE family_name = 'Beans'), 'Phaseolus vulgaris', 'Vulgaris');

INSERT INTO species (family_id, latin_name, species_name)
VALUES ((SELECT family_id FROM family WHERE family_name = 'Beets'), 'Beta vulgaris', 'Vulgaris');

INSERT INTO species (family_id, latin_name, species_name)
VALUES ((SELECT family_id FROM family WHERE family_name = 'Collards'), 'Brassica oleracea', 'Oleracea');

INSERT INTO species (family_id, latin_name, species_name)
VALUES ((SELECT family_id FROM family WHERE family_name = 'Okra'), 'Abelmoschus esculentus', 'Esculentus');

INSERT INTO species (family_id, latin_name, species_name)
VALUES ((SELECT family_id FROM family WHERE family_name = 'Peppers, Hot'), 'Capsicum baccatum', 'Baccatum');

INSERT INTO species (family_id, latin_name, species_name)
VALUES ((SELECT family_id FROM family WHERE family_name = 'Peppers, Hot'), 'Capsicum annum', 'Annum');

INSERT INTO species (family_id, latin_name, species_name)
VALUES ((SELECT family_id FROM family WHERE family_name = 'Peppers, Hot'), 'Capsicum chinense', 'Chinense');

INSERT INTO species (family_id, latin_name, species_name)
VALUES ((SELECT family_id FROM family WHERE family_name = 'Radish'), 'Raphanus sativus', 'Sativus');

INSERT INTO species (family_id, latin_name, species_name)
VALUES ((SELECT family_id FROM family WHERE family_name = 'Sorghum'), 'Sorghum bicolor', 'Bicolor');

INSERT INTO species (family_id, latin_name, species_name)
VALUES ((SELECT family_id FROM family WHERE family_name = 'Squash'), 'Cucurbita maxima', 'Maxima');

INSERT INTO species (family_id, latin_name, species_name)
VALUES ((SELECT family_id FROM family WHERE family_name = 'Squash'), 'Cucurbita moschata', 'Moschata');

INSERT INTO species (family_id, latin_name, species_name)
VALUES ((SELECT family_id FROM family WHERE family_name = 'Tomatos'), 'Solanum lycopersicum', 'Lycopersicum');

-- -- Variety

INSERT INTO variety (species_id, variety_name)
VALUES ((SELECT species_id FROM species WHERE species_name = 'Unguiculata'), 'Iron and Clay');
INSERT INTO crop_infos 
(variety_id, crop_type, days_to_maturity, plant_spacing_harvest, plant_spacing_seed, row_spacing_harvest, row_spacing_seed, days_to_maturity_harvest, days_to_maturity_seed, days_to_transplantation, days_to_direct_sow, days_to_harvest, days_to_seed_harvest, frost_sensitivity_rating) 
VALUES ((SELECT variety_id FROM variety WHERE variety_name = 'Iron and Clay'), '', 100, 12, 3, 24, 18, 75, 7, NULL, NULL, 90, 100, 3);

INSERT INTO variety (species_id, variety_name)
VALUES ((SELECT species_id FROM species WHERE species_name = 'Unguiculata'), 'Nigerian Clay');
INSERT INTO crop_infos 
(variety_id, crop_type, days_to_maturity, plant_spacing_harvest, plant_spacing_seed, row_spacing_harvest, row_spacing_seed, days_to_maturity_harvest, days_to_maturity_seed, days_to_transplantation, days_to_direct_sow, days_to_harvest, days_to_seed_harvest, frost_sensitivity_rating) 
VALUES ((SELECT variety_id FROM variety WHERE variety_name = 'Nigerian Clay'), '', 75, 30, 30, 75, 75, 25, 25, NULL, 0, 75, 90, 3);

INSERT INTO variety (species_id, variety_name)
VALUES ((SELECT species_id FROM species WHERE species_id = 2), 'Dragon Tongue');
INSERT INTO crop_infos 
(variety_id, crop_type, days_to_maturity, plant_spacing_harvest, plant_spacing_seed, row_spacing_harvest, row_spacing_seed, days_to_maturity_harvest, days_to_maturity_seed, days_to_transplantation, days_to_direct_sow, days_to_harvest, days_to_seed_harvest, frost_sensitivity_rating) 
VALUES ((SELECT variety_id FROM variety WHERE variety_name = 'Dragon Tongue'), 'Bush', 60, 2, 2, 36, 36, 60, 7, NULL, 0, 60, 80, 3);

INSERT INTO variety (species_id, variety_name)
VALUES ((SELECT species_id FROM species WHERE species_id = 2), 'Mbombo Beans');
INSERT INTO crop_infos 
(variety_id, crop_type, days_to_maturity, plant_spacing_harvest, plant_spacing_seed, row_spacing_harvest, row_spacing_seed, days_to_maturity_harvest, days_to_maturity_seed, days_to_transplantation, days_to_direct_sow, days_to_harvest, days_to_seed_harvest, frost_sensitivity_rating) 
VALUES ((SELECT variety_id FROM variety WHERE variety_name = 'Mbombo Beans'), 'Semi-Vining', 60, 12, 12, 24, 24, 60, 60, NULL, 0, 60, 60, 3);

INSERT INTO variety (species_id, variety_name)
VALUES ((SELECT species_id FROM species WHERE species_id = 3), 'Early Wonder Tall Top');
INSERT INTO crop_infos 
(variety_id, crop_type, days_to_maturity, plant_spacing_harvest, plant_spacing_seed, row_spacing_harvest, row_spacing_seed, days_to_maturity_harvest, days_to_maturity_seed, days_to_transplantation, days_to_direct_sow, days_to_harvest, days_to_seed_harvest, frost_sensitivity_rating) 
VALUES ((SELECT variety_id FROM variety WHERE variety_name = 'Early Wonder Tall Top'), '', 60, 5, 1, 18, 18, 60, 60, NULL, 28, 60, 60, 2);

INSERT INTO variety (species_id, variety_name)
VALUES ((SELECT species_id FROM species WHERE species_id = 3), 'Golden Beets');
INSERT INTO crop_infos 
(variety_id, crop_type, days_to_maturity, plant_spacing_harvest, plant_spacing_seed, row_spacing_harvest, row_spacing_seed, days_to_maturity_harvest, days_to_maturity_seed, days_to_transplantation, days_to_direct_sow, days_to_harvest, days_to_seed_harvest, frost_sensitivity_rating) 
VALUES ((SELECT variety_id FROM variety WHERE variety_name = 'Golden Beets'), '', 70, 5, 2, 18, 18, 70, 60, 20, 28, 60, 60, 2);

INSERT INTO variety (species_id, variety_name)
VALUES ((SELECT species_id FROM species WHERE species_name = 'Oleracea'), 'Green Glaze');
INSERT INTO crop_infos 
(variety_id, crop_type, days_to_maturity, plant_spacing_harvest, plant_spacing_seed, row_spacing_harvest, row_spacing_seed, days_to_maturity_harvest, days_to_maturity_seed, days_to_transplantation, days_to_direct_sow, days_to_harvest, days_to_seed_harvest, frost_sensitivity_rating) 
VALUES ((SELECT variety_id FROM variety WHERE variety_name = 'Green Glaze'), '', 80, 30, 30, NULL, NULL, 80, 80, 20, 20, 80, 100, 2);

INSERT INTO variety (species_id, variety_name)
VALUES ((SELECT species_id FROM species WHERE species_name = 'Oleracea'), 'Nancy Purple Wheat Collards');
INSERT INTO crop_infos 
(variety_id, crop_type, days_to_maturity, plant_spacing_harvest, plant_spacing_seed, row_spacing_harvest, row_spacing_seed, days_to_maturity_harvest, days_to_maturity_seed, days_to_transplantation, days_to_direct_sow, days_to_harvest, days_to_seed_harvest, frost_sensitivity_rating) 
VALUES ((SELECT variety_id FROM variety WHERE variety_name = 'Nancy Purple Wheat Collards'), '', 70, 30, 30, NULL, NULL, 70, 70, 20, 20, 70, 90, 2);

INSERT INTO variety (species_id, variety_name)
VALUES ((SELECT species_id FROM species WHERE species_name = 'Esculentus'), 'Jade');
INSERT INTO crop_infos 
(variety_id, crop_type, days_to_maturity, plant_spacing_harvest, plant_spacing_seed, row_spacing_harvest, row_spacing_seed, days_to_maturity_harvest, days_to_maturity_seed, days_to_transplantation, days_to_direct_sow, days_to_harvest, days_to_seed_harvest, frost_sensitivity_rating) 
VALUES ((SELECT variety_id FROM variety WHERE variety_name = 'Jade'), '', 60, 18, 12, 42, 42, 60, 20, 28, 21, 60, 80, 3);

INSERT INTO variety (species_id, variety_name)
VALUES ((SELECT species_id FROM species WHERE species_name = 'Esculentus'), 'Star of David');
INSERT INTO crop_infos 
(variety_id, crop_type, days_to_maturity, plant_spacing_harvest, plant_spacing_seed, row_spacing_harvest, row_spacing_seed, days_to_maturity_harvest, days_to_maturity_seed, days_to_transplantation, days_to_direct_sow, days_to_harvest, days_to_seed_harvest, frost_sensitivity_rating) 
VALUES ((SELECT variety_id FROM variety WHERE variety_name = 'Star of David'), '', 70, 18, 18, 42, 42, 70, 20, 35, 21, 70, 90, 3);

INSERT INTO variety (species_id, variety_name)
VALUES ((SELECT species_id FROM species WHERE species_name = 'Baccatum'), 'Aji Amarillo');
INSERT INTO crop_infos 
(variety_id, crop_type, days_to_maturity, plant_spacing_harvest, plant_spacing_seed, row_spacing_harvest, row_spacing_seed, days_to_maturity_harvest, days_to_maturity_seed, days_to_transplantation, days_to_direct_sow, days_to_harvest, days_to_seed_harvest, frost_sensitivity_rating) 
VALUES ((SELECT variety_id FROM variety WHERE variety_name = 'Aji Amarillo'), '', 120, 18, 18, 36, 18, 120, 120, 60, 0, 120, 120, 3);

INSERT INTO variety (species_id, variety_name)
VALUES ((SELECT species_id FROM species WHERE species_name = 'Annum'), 'Fish Peppers');
INSERT INTO crop_infos 
(variety_id, crop_type, days_to_maturity, plant_spacing_harvest, plant_spacing_seed, row_spacing_harvest, row_spacing_seed, days_to_maturity_harvest, days_to_maturity_seed, days_to_transplantation, days_to_direct_sow, days_to_harvest, days_to_seed_harvest, frost_sensitivity_rating) 
VALUES ((SELECT variety_id FROM variety WHERE variety_name = 'Fish Peppers'), '',  75, 24, 24, 36, 36, 75, 75, 42, 0, 75, 75, 3);

INSERT INTO variety (species_id, variety_name)
VALUES ((SELECT species_id FROM species WHERE species_name = 'Chinense'), 'Red Scotch Bonnet');
INSERT INTO crop_infos 
(variety_id, crop_type, days_to_maturity, plant_spacing_harvest, plant_spacing_seed, row_spacing_harvest, row_spacing_seed, days_to_maturity_harvest, days_to_maturity_seed, days_to_transplantation, days_to_direct_sow, days_to_harvest, days_to_seed_harvest, frost_sensitivity_rating) 
VALUES ((SELECT variety_id FROM variety WHERE variety_name = 'Red Scotch Bonnet'), '',  100, 36, 36, 60, 36, 100, 100, 56, 60, 84, 84, 3);

INSERT INTO variety (species_id, variety_name)
VALUES ((SELECT species_id FROM species WHERE species_name = 'Sativus'), 'Misato Rose');
INSERT INTO crop_infos 
(variety_id, crop_type, days_to_maturity, plant_spacing_harvest, plant_spacing_seed, row_spacing_harvest, row_spacing_seed, days_to_maturity_harvest, days_to_maturity_seed, days_to_transplantation, days_to_direct_sow, days_to_harvest, days_to_seed_harvest, frost_sensitivity_rating) 
VALUES ((SELECT variety_id FROM variety WHERE variety_name = 'Misato Rose'), '',  60, 4, NULL, 12, 18, 60, 60, NULL, 60, 60, NULL, 3);

INSERT INTO variety (species_id, variety_name)
VALUES ((SELECT species_id FROM species WHERE species_name = 'Sativus'), 'Cherry Belle');
INSERT INTO crop_infos 
(variety_id, crop_type, days_to_maturity, plant_spacing_harvest, plant_spacing_seed, row_spacing_harvest, row_spacing_seed, days_to_maturity_harvest, days_to_maturity_seed, days_to_transplantation, days_to_direct_sow, days_to_harvest, days_to_seed_harvest, frost_sensitivity_rating) 
VALUES ((SELECT variety_id FROM variety WHERE variety_name = 'Cherry Belle'), '',  21, 2.5, 1, 12, 12, 21, 21, NULL, 30, 21, NULL, 2);

INSERT INTO variety (species_id, variety_name)
VALUES ((SELECT species_id FROM species WHERE species_name = 'Bicolor'), 'Dorado');
INSERT INTO crop_infos 
(variety_id, crop_type, days_to_maturity, plant_spacing_harvest, plant_spacing_seed, row_spacing_harvest, row_spacing_seed, days_to_maturity_harvest, days_to_maturity_seed, days_to_transplantation, days_to_direct_sow, days_to_harvest, days_to_seed_harvest, frost_sensitivity_rating) 
VALUES ((SELECT variety_id FROM variety WHERE variety_name = 'Dorado'), '',  130, 28, 6, 36, 36, 130, 130, 28, 21, 130, 130, 3);

INSERT INTO variety (species_id, variety_name)
VALUES ((SELECT species_id FROM species WHERE species_name = 'Bicolor'), 'Texicoa');
INSERT INTO crop_infos 
(variety_id, crop_type, days_to_maturity, plant_spacing_harvest, plant_spacing_seed, row_spacing_harvest, row_spacing_seed, days_to_maturity_harvest, days_to_maturity_seed, days_to_transplantation, days_to_direct_sow, days_to_harvest, days_to_seed_harvest, frost_sensitivity_rating) 
VALUES ((SELECT variety_id FROM variety WHERE variety_name = 'Texicoa'), '',  90, 15, 4, 40, 40, 90, 90, NULL, 0, 90, 90, 3);

INSERT INTO variety (species_id, variety_name)
VALUES ((SELECT species_id FROM species WHERE species_name = 'Maxima'), 'Nanticoke');
INSERT INTO crop_infos 
(variety_id, crop_type, days_to_maturity, plant_spacing_harvest, plant_spacing_seed, row_spacing_harvest, row_spacing_seed, days_to_maturity_harvest, days_to_maturity_seed, days_to_transplantation, days_to_direct_sow, days_to_harvest, days_to_seed_harvest, frost_sensitivity_rating) 
VALUES ((SELECT variety_id FROM variety WHERE variety_name = 'Nanticoke'), '',  120, 36, 24, 72, 48, 120, 100, 28, 21, 120, 140, 3);

INSERT INTO variety (species_id, variety_name)
VALUES ((SELECT species_id FROM species WHERE species_name = 'Moschata'), 'Mrs. Amersons');
INSERT INTO crop_infos 
(variety_id, crop_type, days_to_maturity, plant_spacing_harvest, plant_spacing_seed, row_spacing_harvest, row_spacing_seed, days_to_maturity_harvest, days_to_maturity_seed, days_to_transplantation, days_to_direct_sow, days_to_harvest, days_to_seed_harvest, frost_sensitivity_rating) 
VALUES ((SELECT variety_id FROM variety WHERE variety_name = 'Mrs. Amersons'), '',  110, 24, 12, 48, 24, 110, 10, 21, NULL, 110, 110, 2);

INSERT INTO variety (species_id, variety_name)
VALUES ((SELECT species_id FROM species WHERE species_name = 'Lycopersicum'), 'Aunt Lous Underground Railroad');
INSERT INTO crop_infos 
(variety_id, crop_type, days_to_maturity, plant_spacing_harvest, plant_spacing_seed, row_spacing_harvest, row_spacing_seed, days_to_maturity_harvest, days_to_maturity_seed, days_to_transplantation, days_to_direct_sow, days_to_harvest, days_to_seed_harvest, frost_sensitivity_rating) 
VALUES ((SELECT variety_id FROM variety WHERE variety_name = 'Aunt Lous Underground Railroad'), '', 80, 24, 18, 36, 30, 70, 80, 21, NULL, 70, 80, 3);

INSERT INTO variety (species_id, variety_name)
VALUES ((SELECT species_id FROM species WHERE species_name = 'Lycopersicum'), 'Cherokee Purple');
INSERT INTO crop_infos 
(variety_id, crop_type, days_to_maturity, plant_spacing_harvest, plant_spacing_seed, row_spacing_harvest, row_spacing_seed, days_to_maturity_harvest, days_to_maturity_seed, days_to_transplantation, days_to_direct_sow, days_to_harvest, days_to_seed_harvest, frost_sensitivity_rating) 
VALUES ((SELECT variety_id FROM variety WHERE variety_name = 'Cherokee Purple'), '',  90, 18,18,36,36,90,140,50,NULL,NULL,140,3);

COMMIT;
