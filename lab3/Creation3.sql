
CREATE TABLE sports (
    sport_id SERIAL PRIMARY KEY,
    sport_name VARCHAR(100) NOT NULL,
    category VARCHAR(20) check(category IN('individual', 'command'))
);

CREATE TABLE sponsors (
    sponsor_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT null 
);

CREATE TABLE teams (
    team_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT null
);

CREATE TABLE sportsmen (
    sportsman_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    surname VARCHAR(100) NOT NULL,
    age INT NOT NULL,
    sports_category VARCHAR(50)
);

CREATE TABLE results (
    result_id SERIAL PRIMARY KEY,
    winner_team_id INT references teams(team_id),
    winner_sportsman_id INT references sportsmen(sportsman_id)
);

CREATE TABLE competitions (
    competition_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    sport_id INT references sports(sport_id) not null unique,
    location VARCHAR(150),
    date DATE NOT NULL,
    result_id INT references results(result_id) not null unique
);

CREATE TABLE competitions_sportsmen (
    competition_id INT NOT null references competitions(competition_id),
    sportsman_id INT NOT null references sportsmen(sportsman_id),
    PRIMARY KEY (competition_id, sportsman_id)
);

CREATE TABLE competitions_teams (
    competition_id INT NOT null references competitions(competition_id),
    team_id INT NOT null references teams(team_id),
    PRIMARY KEY (competition_id, team_id)
);

CREATE TABLE sponsors_sportsmen (
    sponsor_id INT NOT null references sponsors(sponsor_id),
    sportsman_id INT NOT null references sportsmen(sportsman_id),
    PRIMARY KEY (sponsor_id, sportsman_id)
);

CREATE TABLE teams_sportsmen (
    sportsman_id INT NOT null references sportsmen(sportsman_id),
    team_id INT NOT null references teams(team_id),
    PRIMARY KEY (team_id, sportsman_id)
);

