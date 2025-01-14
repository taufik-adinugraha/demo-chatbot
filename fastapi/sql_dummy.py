#!/usr/bin/env python3

import sqlite3
import random
from datetime import datetime, timedelta

def main(n_devices=100, n_customers=20):
    # -----------------------------------------------
    # 1) Connect to (or create) the SQLite database
    # -----------------------------------------------
    conn = sqlite3.connect('dummy_data.db')
    cur = conn.cursor()

    # -----------------------------------------------
    # 2) Drop existing table and create a new one
    # -----------------------------------------------
    drop_table_sql = "DROP TABLE IF EXISTS l4_power_agg_stats;"
    create_table_sql = """
    CREATE TABLE l4_power_agg_stats (
        id            INTEGER PRIMARY KEY AUTOINCREMENT,
        ts_hour       TEXT NOT NULL,
        device_id     INTEGER NOT NULL,
        customer_id   INTEGER NOT NULL,
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
    cur.execute(drop_table_sql)
    cur.execute(create_table_sql)
    conn.commit()

    # -----------------------------------------------
    # 3) Prepare your dummy data parameters
    # -----------------------------------------------
    # Let's define a start_date (inclusive) and end_date (exclusive) for 1 year
    start_date = datetime(2024, 1, 1, 0, 0, 0)
    end_date   = datetime(2025, 1, 25, 0, 0, 0)

    # Hourly increments
    delta = timedelta(hours=1)

    # Example devices, customers, building types, regions
    devices = [i for i in range(1, n_devices + 1)]
    customers = [i for i in range(1, n_customers + 1)]
    building_types = ["Rumah", "Kantor", "Pabrik", "Rumah Sakit", "Sekolah", "Ruko"]
    regions = ["Jakarta", "Bogor", "Depok", "Tangerang", "Bekasi"]

    # -----------------------------------------------
    # 4) Generate and insert data hour by hour
    # -----------------------------------------------
    current_ts = start_date
    insert_sql = """
    INSERT INTO l4_power_agg_stats (
        ts_hour, device_id, customer_id, building_type,
        latitude, longitude, region,
        usage_count, usage_sum, usage_min, usage_max
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """

    # We'll collect rows in a list, then insert in bulk for performance
    batch_size = 5000
    rows_to_insert = []

    while current_ts < end_date:
        for device_id in devices:
            # Randomly select associated attributes
            customer_id   = random.choice(customers)
            building_type = random.choice(building_types)
            region        = random.choice(regions)

            # For demo, pick a random lat/long near some general area
            latitude  = random.uniform(30.0, 45.0)
            longitude = random.uniform(-120.0, -80.0)

            # Usage metrics
            usage_count = random.randint(1, 100)
            # usage_min < usage_max, usage_sum ~ usage_count * average usage
            usage_min = random.uniform(0.0, 2.0)
            usage_max = usage_min + random.uniform(0.1, 5.0)
            avg_usage = (usage_min + usage_max) / 2
            usage_sum = usage_count * avg_usage

            # Prepare the row
            row = (
                current_ts.strftime("%Y-%m-%d %H:%M:%S"),  # ts_hour
                device_id,
                customer_id,
                building_type,
                latitude,
                longitude,
                region,
                usage_count,
                round(usage_sum, 3),  # round for neatness
                round(usage_min, 3),
                round(usage_max, 3)
            )
            rows_to_insert.append(row)

            # Insert in batches to avoid large transactions
            if len(rows_to_insert) >= batch_size:
                cur.executemany(insert_sql, rows_to_insert)
                conn.commit()
                rows_to_insert.clear()

        # Move to the next hour
        current_ts += delta

    # Insert any remaining rows
    if rows_to_insert:
        cur.executemany(insert_sql, rows_to_insert)
        conn.commit()

    # -----------------------------------------------
    # 5) Close the database connection
    # -----------------------------------------------
    print("Data generation complete. Closing connection.")
    conn.close()


if __name__ == "__main__":
    main(n_devices=100, n_customers=20)