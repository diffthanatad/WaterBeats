# RulesDataManagement
This API manages the actuator rules and sensor alerts.

## Quick Start

Create a Python virtual environment by executing the following command.
```sh
python3 -m venv .venv
```
Activate the Python virtual environment.
```sh
source .venv/bin/activate
```

### Setup InfluxDB & DataBackend

1. Follow the README.md file in the /TSDB directory to set up InfluxDB.
2. Follow the README.md file in the /DataBackend directory to set up DataBackend.

### Setup RulesDataManagement API

1. Start PostgreSQL with Docker.
```sh
docker run --name rules-postgres-db -e POSTGRES_USER=waterbeats -e POSTGRES_PASSWORD=password -e POSTGRES_DB=rules_db -p 3000:5432 -d postgres
```

2. Import the database schema rules_database_scheme.sql found in the /DockerImages directory into PostgreSQL
```sh
cat ../DockerImages/rules_database_scheme.sql | docker exec -i rules-postgres-db psql -U waterbeats -d rules_db
```

3. Install the required Python packages.
```sh
pip install -r requirements.txt
```

4. Export the required environment variables.
```sh
export RULES_API_URL="http://rules-data-management:3001/alert/sendAlert"
export RULES_BACKEND_URL="http://localhost:23334/rules_data/send_rules"
export RULES_DB_NAME="rules_db"
export RULES_DB_USER="waterbeats"
export RULES_DB_PASSWORD="password"
export RULES_DB_HOST="localhost"
export RULES_DB_PORT="3000"
export INFLUXDB_BASE_URL="http://influxdb:8086"
```

4. Export the required environment variables for our messaging service Twilio. This can be acquired by signing up [here](https://www.twilio.com/try-twilio).
```sh
export TWILIO_TOKEN="<auth-token>" # Twilio Auth Token
export TWILIO_SID="<account-sid> " # Twilio Account SID
export TWILIO_TO="<to-number>" # Receiver number for incoming messages
export TWILIO_FROM="<from-number>" # Sensder number for outgoing messages
```

5. Run the API by executing the following command:
```sh
python3 app.py
```

#### RulesDataManagement API Endpoint
```sh
http://localhost:3001
```
