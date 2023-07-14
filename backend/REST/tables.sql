CREATE TABLE IF NOT EXISTS logSenseUser (
    ID bigserial PRIMARY KEY,
    --Group_ID int,
    Name varchar,
    EMail varchar UNIQUE NOT NULL,
    PasswordHash varchar NOT NULL,
    Salt varchar NOT NULL
);

CREATE TABLE IF NOT EXISTS PC(
    ID bigserial PRIMARY KEY,
    USER_ID int,
    hardwareUUID varchar,
    manufacturer varchar,
    model varchar,
    FOREIGN KEY (USER_ID) REFERENCES logSenseUser (ID)
);

--DROP Table pc_measurements;
--CREATE TABLE IF NOT EXISTS pc_measurements (
--    measurement_time TIMESTAMP NOT NULL,
--    user_id bigserial,
--    measurement_value FLOAT
--);
--SELECT create_hypertable('pc_measurements', 'measurement_time');
--SELECT create_hypertable('pc_measurements', 'measurement_time', chunk_time_interval => INTERVAL '1 day');