CREATE TABLE IF NOT EXISTS logSenseUser (
    ID bigserial PRIMARY KEY,
    name varchar,
    email varchar UNIQUE NOT NULL,
    password_hash varchar NOT NULL,
    salt varchar NOT NULL
);

CREATE TABLE IF NOT EXISTS PC(
    ID bigserial PRIMARY KEY,
    user_ID bigint,
    hardware_UUID varchar UNIQUE,
    client_Name varchar,
    manufacturer varchar,
    model varchar,
    FOREIGN KEY (USER_ID) REFERENCES logSenseUser (ID),
    UNIQUE (client_Name, USER_ID)
);

CREATE TABLE IF NOT EXISTS PCState(
  id bigserial PRIMARY KEY,
  pc_id bigint,
  total_memory_size bigint,
  memory_page_size int,
  processor_name varchar,
  processor_identifier varchar,
  processor_id varchar,
  processor_vendor varchar,
  processor_bitness int,
  physical_package_count int,
  physical_processor_count int,
  logical_processor_count int,
    FOREIGN KEY (pc_ID) REFERENCES PC (ID)
);

CREATE TABLE IF NOT EXISTS pcdata(
  id bigserial,
  state_id bigint REFERENCES PCState(ID),
  pc_id bigint REFERENCES pc (ID),
  measurement_time timestamp NOT NULL,
  free_disk_space bigint,
  partition_major_faults int,
  partition_minor_faults int,
  available_memory bigint,
  names_power_source varchar,
  discharging_power_sources boolean,
  power_online_power_sources boolean,
  remaining_capacity_percent_power_sources double precision,
  context_switches_processor bigint,
  interrupts_processor bigint,
  total_cpu double precision,
  total_ram bigint,
  total_context_switches int,
  total_major_faults int,
  total_minor_faults int,
  total_open_files int,
  total_thread_count int
);

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM timescaledb_information.hypertables
        WHERE hypertable_name = 'pcdata'
    )
    THEN
        PERFORM create_hypertable('pcdata', 'measurement_time');
    END IF;
END $$;


CREATE TABLE IF NOT EXISTS applicationdata (
    ID BIGSERIAL,
    PcData_ID bigint,
    measurement_time TIMESTAMP NOT NULL,
    name VARCHAR,
    path VARCHAR,
    cpu DOUBLE PRECISION,
    ram BIGINT,
    state VARCHAR,
    "user" VARCHAR,
    context_switches int,
    major_faults int,
    bitness int,
    commandline VARCHAR,
    "current_Working_Directory" VARCHAR,
    open_Files int,
    parent_Process_ID int,
    thread_count int,
    uptime BIGINT,
    process_count_difference int
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

CREATE TABLE IF NOT EXISTS anomaly (
  id bigserial PRIMARY KEY,
  user_id bigint REFERENCES logSenseUser (id), --NULL
  type varchar,
  severity_level int,
  message varchar,
  condition json                                --NULL
);

CREATE TABLE IF NOT EXISTS applicationdata_anomaly (
  anomaly_id bigint REFERENCES anomaly (id),
  applicationdata_id bigint,
  user_id bigint REFERENCES logsenseuser (id),
  type varchar,
  PRIMARY KEY (anomaly_id, applicationdata_id)
);


CREATE TABLE IF NOT EXISTS networkInterface (
  id bigserial PRIMARY KEY,
  pcdata_id bigint,
  name varchar,
  display_name varchar,
  ipv4_address varchar,
  ipv6_address varchar,
  subnet_mask varchar,
  mac_address varchar,
  bytes_received bigint,
  bytes_sent bigint,
  packets_received bigint,
  packets_sent bigint
);

CREATE TABLE IF NOT EXISTS Connection (
    ID bigserial PRIMARY KEY,
    pcdata_ID varchar,
    localAddress varchar,
    localPort int,
    foreignAddress varchar,
    foreignPort int,
    state varchar,
    type varchar,
    owningProcessID int
);

CREATE TABLE IF NOT EXISTS disk (
  id bigserial PRIMARY KEY,
  pcdata_id bigint,
  model varchar,
  name varchar,
  size bigint
);

CREATE TABLE IF NOT EXISTS diskpartition (
  id bigserial PRIMARY KEY,
  disk_id bigint REFERENCES disk (id),
  disk_store_name varchar,
  identification varchar,
  name varchar,
  type varchar,
  mount_point varchar,
  size bigint,
  major_faults int,
  minor_faults int
);
