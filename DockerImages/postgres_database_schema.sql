-- Database: waterbeats
-- Generation Time: Thursday 23 Februrary 2023 21:24

DROP TABLE IF EXISTS "public"."users";

-- Sequence and defined type
CREATE SEQUENCE IF NOT EXISTS users_id_seq START 5;
DROP TYPE IF EXISTS "public"."enum_users_role";
CREATE TYPE "public"."enum_users_role" AS ENUM ('admin', 'moderator', 'user');

-- Table Definition
CREATE TABLE "public"."users" (
    "id" int4 NOT NULL DEFAULT nextval('users_id_seq'::regclass),
    "name" varchar(150) NOT NULL,
    "username" varchar(150) UNIQUE NOT NULL,
    "password" varchar(300) NOT NULL,
    "disable" bool DEFAULT false,
    "role" "public"."enum_users_role" DEFAULT 'user'::enum_users_role,
    PRIMARY KEY ("id")
);

INSERT INTO "public"."users" ("id", "name", "username", "password", "disable", "role") VALUES
(1, 'David Brown', 'david-b', '$2a$12$JSR03lduQ6WNuM5ltjcUh.ANvLywn1F0GkjVJ.z5Rc.zfNU80fNOu', 'f', 'admin'),
(2, 'Daniel Smith', 'daniel-s', '$2a$12$JSR03lduQ6WNuM5ltjcUh.ANvLywn1F0GkjVJ.z5Rc.zfNU80fNOu', 'f', 'moderator'),
(3, 'Bob Smith', 'bob-s', '$2a$12$JSR03lduQ6WNuM5ltjcUh.ANvLywn1F0GkjVJ.z5Rc.zfNU80fNOu', 'f', 'user'),
(4, 'Alice Mac', 'alice-m', '$2a$12$JSR03lduQ6WNuM5ltjcUh.ANvLywn1F0GkjVJ.z5Rc.zfNU80fNOu', 'f', 'user');
