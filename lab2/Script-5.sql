ALTER TABLE properties 
DROP COLUMN availability;

ALTER TABLE properties 
add COLUMN availability VARCHAR(20)
check (availability in ('available', 'rented'));