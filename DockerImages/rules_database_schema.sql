
DROP TABLE IF EXISTS "public"."rules";
DROP TABLE IF EXISTS "public"."alerts";

DROP TYPE IF EXISTS "public"."enum_actuator_type";
DROP TYPE IF EXISTS "public"."enum_sensor_type";
DROP TYPE IF EXISTS "public"."enum_relation";

CREATE TYPE "public"."enum_actuator_type" AS ENUM ('sprinkler', 'pump');
CREATE TYPE "public"."enum_relation" AS ENUM ('<', '>', '<=', '>=', '==');
CREATE TYPE "public"."enum_sensor_type" AS ENUM ('temperature', 'soil_moisture', 'water_level', 'water_pollution');

-- Table Definition
CREATE TABLE "public"."rules" (
    "id" serial PRIMARY KEY,
    "subject_sensor" varchar(50) NOT NULL,
    "sensor_reading" INTEGER NOT NULL,
    "relation" "public"."enum_relation" NOT NULL,
    "actuator_id" varchar(50) UNIQUE NOT NULL,
    "actuator_type" "public"."enum_actuator_type" NOT NULL,
    "actuator_state" BOOLEAN NOT NULL,
    "intensity" SMALLINT NOT NULL,
    "duration" SMALLINT NOT NULL,
    "created_at" TIMESTAMP NOT NULL DEFAULT NOW(),
    "updated_at" TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE "public"."alerts" (
    "id" serial PRIMARY KEY,
    "sensor_id" varchar(50) UNIQUE NOT NULL,
    "sensor_type" "public"."enum_sensor_type" NOT NULL,
    "threshold" INTEGER NULL,
    "relation" "public"."enum_relation" NOT NULL,
    "created_at" TIMESTAMP NOT NULL DEFAULT NOW(),
    "updated_at" TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Function Definition
CREATE OR REPLACE FUNCTION trigger_set_timestamp()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger Definition
CREATE TRIGGER set_timestamp_rules
BEFORE UPDATE ON rules
FOR EACH ROW
EXECUTE PROCEDURE trigger_set_timestamp();

CREATE TRIGGER set_timestamp_alerts
BEFORE UPDATE ON alerts
FOR EACH ROW
EXECUTE PROCEDURE trigger_set_timestamp();
