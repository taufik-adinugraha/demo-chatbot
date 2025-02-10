from setup import *

table_schemas_sqlite = """
    CREATE TABLE IF NOT EXISTS l4_power_agg_stats (
        id            INTEGER,
        ts_hour       TEXT,
        device_id     INTEGER,
        customer_id   TEXT,
        building_type TEXT,
        region        TEXT,
        usage_count   INTEGER,
        usage_sum     REAL,
        usage_min     REAL,
        usage_max     REAL
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
"""


table_schemas_map = {
    "sqlite": table_schemas_sqlite,
    "clickhouse": table_schemas_clickhouse
}

table_schemas = table_schemas_map[db_type]