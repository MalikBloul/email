-- Creating tables --

CREATE TABLE IF NOT EXISTS degrees (
    id INTEGER,
    course_name TEXT NOT NULL,
    level INTEGER NOT NULL,
    description TEXT NOT NULL,
    uac_code INTEGER NOT NULL,
    duration INTEGER NOT NULL,
    selection_rank INTEGER NOT NULL,
    part_time INTEGER NOT NULL,
    full_time INTEGER NOT NULL,
    off_campus INTEGER NOT NULL,
    on_campus INTEGER NOT NULL,
    PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS key_dates (
    id INTEGER,
    name TEXT NOT NULL,
    location TEXT NOT NULL,
    start_date TEXT,
    open_date TEXT,
    close_date TEXT,
    PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS html_blocks (
    id INTEGER,
    type TEXT,
    enquirer TEXT,
    block TEXT,
    PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS date_link (
    degree_id INTEGER,
    session_id INTEGER,
    FOREIGN KEY(degree_id) REFERENCES degrees(id),
    FOREIGN KEY(session_id) REFERENCES key_dates(id)
);

