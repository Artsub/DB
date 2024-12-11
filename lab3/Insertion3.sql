INSERT INTO sports (sport_name, category) VALUES
('Cycling', 'individual'),
('Swimming', 'individual'),
('Basketball', 'command'),
('Tennis', 'individual'),
('Football', 'command'),
('Handball', 'command'),
('Volleyball', 'command'),
('Badminton', 'individual');

-- Таблица sponsors
INSERT INTO sponsors(name) VALUES
('Nike'),
('Adidas'),
('Puma'),
('Reebok'),
('Under Armour');

-- Таблица teams
INSERT INTO teams (name) VALUES
('Alpha Warriors'),
('Titan Gladiators'),
('Storm Troopers'),
('Red Dragons'),
('Blue Thunder'),
('Red Falcons');

-- Таблица sportsmen
INSERT INTO sportsmen (name, surname, age, sports_category) 
VALUES 
('John', 'Doe', 25, 'intermediate'),
('Jane', 'Smith', 28, 'advanced'),
('Alice', 'Johnson', 30, 'professional'),
('Bob', 'Brown', 22, 'intermediate'),
('Charlie', 'Williams', 32, 'advanced'),
('David', 'Miller', 27, 'professional'),
('Eva', 'Davis', 24, 'intermediate'),
('Frank', 'Garcia', 29, 'advanced'),
('Grace', 'Martinez', 26, 'professional'),
('Henry', 'Rodriguez', 31, 'advanced'),
('Isabel', 'Taylor', 23, 'intermediate'),
('Jack', 'Anderson', 33, 'advanced'),
('Karen', 'Thomas', 29, 'professional'),
('Louis', 'Hernandez', 26, 'intermediate'),
('Mona', 'Moore', 34, 'advanced'),
('Nina', 'Jackson', 25, 'professional'),
('Oscar', 'White', 27, 'intermediate'),
('Paula', 'Lopez', 32, 'advanced'),
('Quincy', 'Perez', 30, 'professional'),
('Rita', 'Clark', 24, 'intermediate'),
('Steve', 'Lewis', 28, 'advanced'),
('Tina', 'Young', 29, 'professional'),
('Ursula', 'King', 31, 'intermediate'),
('Victor', 'Wright', 26, 'advanced'),
('Walter', 'Scott', 32, 'professional');

INSERT INTO results (winner_team_id, winner_sportsman_id) VALUES
(NULL, 1), -- Max Sullivan выиграл в велоспорте (индивидуальный)
(NULL, 5), -- Olivia Hayes выиграла в теннисе (индивидуальный)
(1, NULL), -- Liam Parker выиграл в плавании (индивидуальный)
(NULL, 7), -- Sophia Richards выиграла в бадминтоне (индивидуальный)
(4, NULL), -- Alpha Warriors выиграли в баскетболе (командный)
(5, NULL), -- Titan Gladiators выиграли в футболе (командный)
(5, NULL); -- Blue Thunder выиграли в гандболе (командный)

-- Таблица competitions
INSERT INTO competitions (name, sport_id, location, date, result_id) VALUES
('Cycling World Championship', 1, 'Berlin', '2024-05-10', 1),
('International Swimming Cup', 2, 'London', '2024-06-15', 2),
('Basketball Championship Final', 3, 'New York', '2024-07-01', 3),
('Tennis Masters', 4, 'Paris', '2024-08-20', 4),
('Football World Cup', 5, 'Moscow', '2024-09-10', 5),
('Handball World Cup', 6, 'Paris', '2024-10-05', 6),
('Volleyball World League', 7, 'Rio de Janeiro', '2024-11-10', 7);

-- Таблица competitions_sportsmen
-- Спортивмены участвуют только в индивидуальных соревнованиях
INSERT INTO competitions_sportsmen  (competition_id, sportsman_id) VALUES 
(1, 1),  
(1, 2),  
(1, 3),  
(2, 4),  
(2, 5),  
(2, 6),  
(4, 7),  
(4, 8),  
(4, 9),  
(4, 10), 
(4, 11), 
(4, 12);

-- Таблица competitions_teams
-- Команды участвуют только в командных соревнованиях
INSERT INTO competitions_teams (competition_id, team_id) VALUES
(3, 1),  
(3, 2),  
(3, 3), 
(5, 4),  
(5, 5),  
(6, 5), 
(6, 6), 
(7, 5), 
(7, 6);


-- Таблица sponsors_sportsmen
INSERT INTO sponsors_sportsmen (sponsor_id, sportsman_id) VALUES
(1, 1), 
(1, 4),  
(1, 6),  
(2, 3),  
(2, 5),  
(3, 10),
(3,11),
(3,12),
(4,13),
(4,15),
(5,20);


-- Таблица teams_sportsmen
-- Спортивмены в командах только в командных соревнованиях
INSERT INTO teams_sportsmen (team_id, sportsman_id) VALUES
(1, 13), 
(1, 14), 
(1, 15),  
(2, 16), 
(2, 17), 
(3, 18),  
(3, 19),  
(3, 20),
(4, 21),
(4, 22),
(5, 23),
(5, 24),
(6, 25),
(6, 1);