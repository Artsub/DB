select rc.rental_contract_id, rc.start_date, 
rc.end_date,rc.contract_type, p.type
from rental_contracts as rc,
properties as p 
where p.property_id = rc.rental_contract_id 
and p.type like 'House'   