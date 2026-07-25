create schema if not exists bronze;

create or replace view bronze.telemetry_raw as
select
    * exclude (filename)
from read_parquet(
    'data/bronze/telemetry/**/*.parquet',
    hive_partitioning = true,
    filename = true
);

create or replace view bronze.session_raw as
select
    * exclude (filename)
from read_parquet(
    'data/bronze/sessions/**/*.parquet',
    hive_partitioning = true,
    filename = true
);
