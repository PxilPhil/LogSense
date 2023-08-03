INSERT INTO anomaly (type, severity_level, message)
SELECT 'Event', 1, 'A event has occurred without a reason'
WHERE NOT EXISTS (
    SELECT 1 FROM anomaly
    WHERE type = 'Anomaly' AND severity_level = 1 AND message = 'A anomaly has occurred'
);

INSERT INTO anomaly (type, severity_level, message)
SELECT 'Event', 0, 'A event has occurred'
WHERE NOT EXISTS (
    SELECT 1 FROM anomaly
    WHERE type = 'Event' AND severity_level = 0 AND message = 'A event has occurred'
);

INSERT INTO anomaly (type, severity_level, message)
SELECT 'Anomaly', 2, 'A anomaly has occurred'
WHERE NOT EXISTS (
    SELECT 1 FROM anomaly
    WHERE type = 'Anomaly' AND severity_level = 2 AND message = 'A anomaly has occurred'
);
