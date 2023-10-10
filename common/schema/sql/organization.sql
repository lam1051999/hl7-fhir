CREATE TYPE t_coding AS (
    "system" VARCHAR(500),
    "version" VARCHAR(500),
    "code" VARCHAR(500),
    "display" VARCHAR(500),
    "userSelected" BOOLEAN
);

CREATE TYPE t_codeable_concept AS (
    "coding" t_coding[],
    "text" VARCHAR(500)
);

CREATE TYPE t_period AS (
    "start" date,
    "end" date
);

CREATE TYPE t_identifier AS (
    "use" VARCHAR(500),
    "type" t_codeable_concept,
    "system" VARCHAR(500),
    "value" VARCHAR(500),
    "period" t_period
);

CREATE TYPE t_human_name AS (
    "use" VARCHAR(500),
    "text" VARCHAR(500),
    "family" VARCHAR(500),
    "given" text[],
    "prefix" text[],
    "suffix" text[],
    "period" t_period
);

CREATE TYPE t_telecom AS (
    "system" VARCHAR(500),
    "value" VARCHAR(500),
    "use" VARCHAR(500),
    "rank" text[],
    "period" t_period
);

CREATE TYPE t_address AS (
    "use" VARCHAR(500),
    "type" VARCHAR(500),
    "text" VARCHAR(500),
    "line" text[],
    "city" VARCHAR(500),
    "district" VARCHAR(500),
    "state" VARCHAR(500),
    "postalCode" VARCHAR(500),
    "country" VARCHAR(500),
    "period" t_period
);

CREATE TYPE t_extended_contact_detail AS (
    "purpose" t_codeable_concept,
    "name" t_human_name[],
    "telecom" t_telecom[],
    "address" t_address,
    "period" t_period
);

--CREATE TABLE organization (
--    "id" VARCHAR(500) PRIMARY KEY,
--    "resourceType" VARCHAR(500),
--    "identifier" t_identifier[],
--    "active" BOOLEAN,
--    "type" t_codeable_concept[],
--    "name" VARCHAR(500),
--    "alias" text[],
--    "description" VARCHAR(500),
--    "contact" t_extended_contact_detail[]
--);

--CREATE TABLE organization_qualification (
--    "id" VARCHAR(500),
--    "identifier" t_identifier[],
--    "code" t_codeable_concept,
--    "period" t_period,
--    "organization_id" VARCHAR(500) REFERENCES organization (id)
--);

CREATE TABLE organization (
    "id" VARCHAR(500) PRIMARY KEY,
    "resourceType" VARCHAR(500),
    "identifier" JSON,
    "active" BOOLEAN,
    "type" JSON,
    "name" VARCHAR(500),
    "alias" text[],
    "description" VARCHAR(500),
    "contact" JSON
);

CREATE TABLE organization_qualification (
    "id" VARCHAR(500),
    "identifier" JSON,
    "code" t_codeable_concept,
    "period" t_period,
    "organization_id" VARCHAR(500) REFERENCES organization (id)
);