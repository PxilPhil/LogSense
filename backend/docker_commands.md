# install docker for logSense

## Port needs to be open for the Docker to run

```shell
netstat -ano | findstr :5432
```

=> use taskmanager to stop process

---

## Create Docker

```shell
docker run -d --name logsense_timescaledb -p 5432:5432 -v C:\projects\logsense\backend -e POSTGRES_PASSWORD=smthsecureidk timescale/timescaledb-ha:pg15-latest
```

[install Postgres & map environment variable to get access to the psql command](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads)

### connect to Docker

```shell
psql -U postgres -h localhost
```

---

```sql
CREATE database logsense;
```

> check running databases:

```shell
\l
```

connect to database to test if it works propperly

```shell
\c logsense
```

---

## If things changed:

If you have changed port,host, name of the database, want to use another user or the password it is possible to change these things in the `config.ini` file.
