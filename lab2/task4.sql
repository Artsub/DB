select distinct c.client_id, c.firstname, c.lastname, c.email 
from rental_contracts as rc, clients as c
where c.client_id = rc.client 
and start_date >= '2024-01-01' and end_date <= '2024-06-30';
