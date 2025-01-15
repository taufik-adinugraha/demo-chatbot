from setup import *

table_schemas_sqlite = """
    CREATE TABLE IF NOT EXISTS l4_power_agg_stats (
        id            INTEGER PRIMARY KEY AUTOINCREMENT,
        ts_hour       TEXT NOT NULL,
        device_id     INTEGER NOT NULL,
        customer_id   TEXT NOT NULL,
        building_type TEXT NOT NULL,
        region        TEXT NOT NULL,
        usage_count   INTEGER NOT NULL,
        usage_sum     REAL NOT NULL,
        usage_min     REAL NOT NULL,
        usage_max     REAL NOT NULL
    );
Notes:
- device = alat/perangkat, region = wilayah/area
"""


table_schemas_clickhouse = """
CREATE TABLE layer_4.power_agg_stats
(
    ts_hour         DateTime,
    day_of_week     String,
    hour_of_day     Int16,
    device_id       String,
    customer_id     String,
    building_type   String,
    region          String,
    usage_count     AggregateFunction(count, Float64),
    usage_sum       AggregateFunction(sum, Float64),
    usage_min       AggregateFunction(min, Float64),
    usage_max       AggregateFunction(max, Float64)
)
ENGINE = AggregatingMergeTree()
PARTITION BY toYYYYMM(ts_hour)

Notes:
- For AggregateFunction types strictly use sumMerge(), countMerge(), minMerge(), maxMerge() functions instead of ordinary SQL syntax SUM(), COUNT(), MIN(), MAX() functions.
- device = alat/perangkat, region = wilayah/area
- for queries related to date, use something like toDate('2025-01-15')
- SQL multi-statements are not allowed
"""


table_schemas_map = {
    "sqlite": table_schemas_sqlite,
    "clickhouse": table_schemas_clickhouse
}

table_schemas = table_schemas_map[db_type]