# LogSense Documentation

# How to run

## Step 1: Starting the agent
Install JDK 17
https://www.oracle.com/de/java/technologies/downloads/#jdk17-windows

Create a new environment variable "JAVA_HOME" with the path to the installation directory of the JDK

Add a new entry to the "PATH" environment variable with the path to the bin directory in the installation directory of the JDK

Double-click the LogSense.exe file to run the Agent

## Step 2: Setting up the backend

### Setting up the docker

Port needs to be open for the Docker to run

```shell
netstat -ano | findstr :5432
```

Can use Taskmanager to stop the process


```shell
docker run -d --name logsense_timescaledb -p 5432:5432 -v C:\projects\logsense\backend -e POSTGRES_PASSWORD=smthsecureidk timescale/timescaledb-ha:pg15-latest
```

[install Postgres & map environment variable to get access to the psql command](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads)

### Connect to Docker

```shell
psql -U postgres -h localhost
```

---
**Only this in Pycharm/Intelij is also ok**
```sql
CREATE database logsense;
```

The database is required to be named logsense or else the application won't work

The standard defined username and password in config.ini are postgres and smthsecureidk respectively


#### Access Swagger Definition

Type in https://localhost:7253/swagger
#### If things have been changed:

If you have changed port, host, name of the database or want to use another user or the password then it is possible to change these things in the `config.ini` file.


### Setting up the python REST application

#### Install libraries

Libraries are placed in the requirements.txt file and can be installed via 
```
pip install -r requirements.txt
```

#### Starting application

You need to run the main.py file to start the entire backend application

## Step 3: Start the Frontend

Install Node.js which includes Node Package Manager

Open Angular Project in Webstorm and run:
npm install 

Run the Project with:
ng serve
