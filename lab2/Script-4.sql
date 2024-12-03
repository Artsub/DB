ALTER TABLE properties
MODIFY availability type VARCHAR(15) 
check (availability in ('available', 'rented') not NULL;