select c.client_id, c.firstname,c.lastname,c.email,
sum(p.price) from rental_contracts as rc, 
clients as c, properties as p
where rc.client = c.client_id 
and rc.property = p.property_id
group by c.client_id 
having sum(p.price) > 2000 