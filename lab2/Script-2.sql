create table clients
(
	client_id SERIAL primary key,
	FirstName VARCHAR(30) not null,
    LastName VARCHAR(30),
    Email VARCHAR(30) not null
);

create table properties
(
	property_id SERIAL primary key,
	adress VARCHAR(150) not null,
    price INTEGER not null,
    type VARCHAR(30),
    availability INTEGER not null
);

create table rental_contracts
(
	rental_contract_id SERIAL primary key,
	start_date DATE not null,
	end_date DATE not null,
	client INTEGER references clients(client_id),
	property INTEGER references properties(property_id)
);
