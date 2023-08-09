TRUNCATE TABLE anomaly CASCADE;
INSERT INTO anomaly (id, type, severity_level, message) VALUES (1, 'RAM Event', 0, 'A event has occured');
INSERT INTO anomaly (id, type, severity_level, message) VALUES (2, 'RAM Event', 1, 'A event has occured without reason');
INSERT INTO anomaly (id, type, severity_level, message) VALUES (3, 'CPU Event', 1, 'A event has occured without reason');
INSERT INTO anomaly (id, type, severity_level, message) VALUES (4, 'CPU Event', 1, 'A event has occured without reason');
INSERT INTO anomaly (id, type, severity_level, message) VALUES (5, 'RAM Anomaly', 1, 'A ram anomaly has occured');
INSERT INTO anomaly (id, type, severity_level, message) VALUES (6, 'CPU Anomaly', 1, 'A ram anomaly has occured');
