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
    hardwareUUID varchar UNIQUE,
    clientName varchar,
    manufacturer varchar,
    model varchar,
    FOREIGN KEY (USER_ID) REFERENCES logSenseUser (ID),
    UNIQUE (clientName, USER_ID)
);

CREATE TABLE IF NOT EXISTS applicationdata (
    ApplicationID BIGSERIAL,
    PcData_ID INT REFERENCES PcData(ID),
    measurement_time TIMESTAMP NOT NULL,
    name VARCHAR,
    path VARCHAR,
    cpu DOUBLE PRECISION,
    ram BIGINT,
    State VARCHAR,
    "user" VARCHAR,
    contextSwitches INT,
    majorFaults INT,
    bitness INT,
    commandLine VARCHAR,
    "currentWorkingDirectory" VARCHAR,
    openFiles INT,
    parentProcessID INT,
    threadCount INT,
    upTime BIGINT,
    processCountDifference INT
);

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM timescaledb_information.hypertables
        WHERE hypertable_name = 'applicationdata'
    )
    THEN
        PERFORM create_hypertable('applicationdata', 'measurement_time');
    END IF;
END $$;



--DROP Table pc_measurements;
--CREATE TABLE IF NOT EXISTS pc_measurements (
--    measurement_time TIMESTAMP NOT NULL,
--    user_id bigserial,
--    measurement_value FLOAT
--);
--SELECT create_hypertable('pc_measurements', 'measurement_time');
--SELECT create_hypertable('pc_measurements', 'measurement_time', chunk_time_interval => INTERVAL '1 day');