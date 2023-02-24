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
    "username" varchar(150) NOT NULL,
    "password" varchar(300) NOT NULL,
    "disable" bool DEFAULT false,
    "role" "public"."enum_users_role" DEFAULT 'user'::enum_users_role,
    PRIMARY KEY ("id")
);

INSERT INTO "public"."users" ("id", "username", "password", "disable", "role") VALUES
(1, 'admin', '$2a$12$JSR03lduQ6WNuM5ltjcUh.ANvLywn1F0GkjVJ.z5Rc.zfNU80fNOu', 'f', 'admin'),
(2, 'moderator', '$2a$12$JSR03lduQ6WNuM5ltjcUh.ANvLywn1F0GkjVJ.z5Rc.zfNU80fNOu', 'f', 'moderator'),
(3, 'Bob', '$2a$12$JSR03lduQ6WNuM5ltjcUh.ANvLywn1F0GkjVJ.z5Rc.zfNU80fNOu', 'f', 'user'),
(4, 'Alice', '$2a$12$JSR03lduQ6WNuM5ltjcUh.ANvLywn1F0GkjVJ.z5Rc.zfNU80fNOu', 'f', 'user');
