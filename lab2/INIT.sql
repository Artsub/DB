INSERT INTO clients (firstname, lastname, email) VALUES ('John', 'Doe', 'john.doe@example.com');
INSERT INTO clients (firstname, lastname, email) VALUES ('Jane', 'Smith', 'jane.smith@example.com');
INSERT INTO clients (firstname, lastname, email) VALUES ('Michael', 'Brown', 'michael.brown@example.com');
INSERT INTO clients (firstname, lastname, email) VALUES ('Emily', 'Davis', 'emily.davis@example.com');
INSERT INTO clients (firstname, lastname, email) VALUES ('Chris', 'Wilson', 'chris.wilson@example.com');
INSERT INTO clients (firstname, lastname, email) VALUES ('Sophia', 'Taylor', 'sophia.taylor@example.com');
INSERT INTO clients (firstname, lastname, email) VALUES ('James', 'Anderson', 'james.anderson@example.com');
INSERT INTO clients (firstname, lastname, email) VALUES ('Isabella', 'Thomas', 'isabella.thomas@example.com');
INSERT INTO clients (firstname, lastname, email) VALUES ('Daniel', 'Jackson', 'daniel.jackson@example.com');
INSERT INTO clients (firstname, lastname, email) VALUES ('Olivia', 'White', 'olivia.white@example.com');
INSERT INTO clients (firstname, lastname, email) VALUES ('Ethan', 'Harris', 'ethan.harris@example.com');
INSERT INTO clients (firstname, lastname, email) VALUES ('Mia', 'Martin', 'mia.martin@example.com');
INSERT INTO clients (firstname, lastname, email) VALUES ('Alexander', 'Garcia', 'alexander.garcia@example.com');
INSERT INTO clients (firstname, lastname, email) VALUES ('Charlotte', 'Martinez', 'charlotte.martinez@example.com');
INSERT INTO clients (firstname, lastname, email) VALUES ('Benjamin', 'Clark', 'benjamin.clark@example.com');

INSERT INTO properties (adress, price, type, availability) VALUES ('123 Main St', 1200, 'Apartment', 'rented');
INSERT INTO properties (adress, price, type, availability) VALUES ('456 Oak St', 1500, 'House', 'rented');
INSERT INTO properties (adress, price, type, availability) VALUES ('789 Pine St', 1000, 'Apartment', 'rented');
INSERT INTO properties (adress, price, type, availability) VALUES ('101 Maple Ave', 2000, 'Condo', 'rented');
INSERT INTO properties (adress, price, type, availability) VALUES ('202 Elm St', 800, 'Studio', 'available');
INSERT INTO properties (adress, price, type, availability) VALUES ('303 Cedar Rd', 1300, 'Apartment', 'rented');
INSERT INTO properties (adress, price, type, availability) VALUES ('404 Birch Dr', 1700, 'House', 'available');
INSERT INTO properties (adress, price, type, availability) VALUES ('505 Spruce Ln', 1100, 'Studio', 'rented');
INSERT INTO properties (adress, price, type, availability) VALUES ('606 Aspen Ct', 2500, 'Condo', 'available');
INSERT INTO properties (adress, price, type, availability) VALUES ('707 Walnut Blvd', 900, 'Apartment', 'available');
INSERT INTO properties (adress, price, type, availability) VALUES ('808 Chestnut Way', 1400, 'Apartment', 'available');
INSERT INTO properties (adress, price, type, availability) VALUES ('909 Redwood Pl', 1800, 'House', 'available');
INSERT INTO properties (adress, price, type, availability) VALUES ('1010 Cypress St', 2200, 'Condo', 'available');
INSERT INTO properties (adress, price, type, availability) VALUES ('1111 Willow Cir', 950, 'Studio', 'available');
INSERT INTO properties (adress, price, type, availability) VALUES ('1212 Poplar St', 1900, 'House', 'available');

INSERT INTO rental_contracts (start_date, end_date, client, property, contract_type) VALUES 
('2024-01-01', '2024-06-30', 1, 3, 'long-term');

INSERT INTO rental_contracts (start_date, end_date, client, property, contract_type) VALUES 
('2024-02-01', '2024-04-30', 1, 7, 'short-term');

INSERT INTO rental_contracts (start_date, end_date, client, property, contract_type) VALUES 
('2024-03-01', '2024-09-01', 2, 5, 'long-term');

INSERT INTO rental_contracts (start_date, end_date, client, property, contract_type) VALUES 
('2024-02-15', '2024-08-15', 3, 8, 'long-term');

INSERT INTO rental_contracts (start_date, end_date, client, property, contract_type) VALUES 
('2024-04-01', '2024-07-31', 4, 2, 'short-term');

INSERT INTO rental_contracts (start_date, end_date, client, property, contract_type) VALUES 
('2024-06-01', '2024-12-01', 5, 10, 'long-term');

INSERT INTO rental_contracts (start_date, end_date, client, property, contract_type) VALUES 
('2024-01-01', '2024-03-31', 6, 4, 'short-term');

INSERT INTO rental_contracts (start_date, end_date, client, property, contract_type) VALUES 
('2024-05-01', '2024-11-01', 6, 9, 'long-term');

INSERT INTO rental_contracts (start_date, end_date, client, property, contract_type) VALUES 
('2024-07-01', '2024-12-31', 7, 11, 'long-term');

INSERT INTO rental_contracts (start_date, end_date, client, property, contract_type) VALUES 
('2024-08-01', '2025-02-28', 8, 13, 'long-term');

INSERT INTO rental_contracts (start_date, end_date, client, property, contract_type) VALUES 
('2024-01-15', '2024-05-15', 9, 6, 'short-term');

INSERT INTO rental_contracts (start_date, end_date, client, property, contract_type) VALUES 
('2024-04-01', '2024-09-30', 10, 15, 'long-term');

INSERT INTO rental_contracts (start_date, end_date, client, property, contract_type) VALUES 
('2024-09-01', '2025-03-01', 11, 14, 'long-term');

INSERT INTO rental_contracts (start_date, end_date, client, property, contract_type) VALUES 
('2024-06-01', '2024-10-31', 12, 12, 'short-term');

INSERT INTO rental_contracts (start_date, end_date, client, property, contract_type) VALUES 
('2024-07-01', '2025-01-01', 13, 1, 'long-term');