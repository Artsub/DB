select rc.client , c.firstname, c.lastname, c.email, count(*) 
from rental_contracts as rc, clients as c 
where c.client_id = rc.client 
group by rc.client, c.firstname, c.lastname, c.email 
order by count(*) desc 
