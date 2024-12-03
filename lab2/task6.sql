create table task6(
	client_id serial primary key,
	total_rental INT
);

INSERT INTO task6 (client_id, total_rental)
select distinct rc.client, SUM(p.price)
from rental_contracts as rc, properties as p
where p.property_id = rc.property 
group by rc.client
