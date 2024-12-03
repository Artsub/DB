select p.type, count(rc.rental_contract_id) 
from properties as p, rental_contracts as rc 
where rc.property = p.property_id 
group by p.type;