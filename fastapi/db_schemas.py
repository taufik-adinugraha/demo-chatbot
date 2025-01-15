from setup import *

table_schemas_sqlite = """
    CREATE TABLE IF NOT EXISTS l4_power_agg_stats (
        id            INTEGER PRIMARY KEY AUTOINCREMENT,
        ts_hour       TEXT NOT NULL,
        device_id     INTEGER NOT NULL,
        customer_id   TEXT NOT NULL,
        building_type TEXT NOT NULL,
        latitude      REAL NOT NULL,
        longitude     REAL NOT NULL,
        region        TEXT NOT NULL,
        usage_count   INTEGER NOT NULL,
        usage_sum     REAL NOT NULL,
        usage_min     REAL NOT NULL,
        usage_max     REAL NOT NULL
    );
"""


table_schemas_clickhouse = """
TABLE: layer_4.power_agg_stats
Fields:
    ts_hour         DateTime,
    day_of_week     String,
    hour_of_day     Int16,
    device_id       String,
    customer_id     String,
    building_type   String,
    region          String,
    latitude        Float64,
    longitude       Float64,
    usage_count     Float64,
    usage_sum       Float64,
    usage_min       Float64,
    usage_max       Float64
"""


table_schemas_map = {
    "sqlite": table_schemas_sqlite,
    "clickhouse": table_schemas_clickhouse
}

table_schemas = table_schemas_map[db]