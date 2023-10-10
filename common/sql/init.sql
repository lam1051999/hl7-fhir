CREATE TABLE healthcare_process (
    "id" serial PRIMARY KEY,
    "process" VARCHAR(500),
    "subprocess" VARCHAR(500)
);

CREATE TYPE file_status AS ENUM('UPLOAD_SUCCESS', 'UPLOAD_FAILED', 'VALIDATION_SUCCESS', 'VALIDATION_FAILED', 'INGESTION_SUCCESS', 'INGESTION_FAILED', 'LOAD_SUCCESS', 'LOAD_FAILED');

CREATE TABLE file_monitor (
    "file_name" VARCHAR(500) PRIMARY KEY,
    "original_file_name" VARCHAR(500),
    "status" file_status,
    "description" text,
    "created" timestamp,
    "updated" timestamp
);