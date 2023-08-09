# What is the best way to access the timescale db?

## How to build an connection

```python
import psycopg2

conn = psycopg2.connect(
    host=db_host,
    port=db_port,
    database=db_name,
    user=db_user,
    password=db_password,
)
cursor = conn.cursor()
```

## Normal insert

```python
import psycopg2

cursor.execute(query, (user_id, measurement_time, measurement_value))
conn.commit()
```

## Bulk insert

```python
import psycopg2
from psycopg2 import extras

psycopg2.extras.execute_values(cursor, query, items)
conn.commit()
```

## Select statements

```python
cursor.execute(query, userid)
rows = cursor.fetchall()

measurements = []
for row in rows:
    measurement = Measurement(row[0], row[1], row[2])
    measurements.append(measurement)
```
