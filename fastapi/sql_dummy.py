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
    start_date = datetime(2024, 5, 1, 0, 0, 0)
    end_date   = datetime(2025, 1, 30, 0, 0, 0)

    # Hourly increments
    delta = timedelta(hours=1)

    # Example devices, customers, building types, regions
    devices = [i for i in range(1, n_devices + 1)]
    customers = [i for i in range(1, n_customers + 1)]
    building_types = ["Rumah", "Kantor", "Pabrik", "Rumah Sakit", "Sekolah", "Ruko"]
    regions = ["Jakarta", "Bogor", "Depok", "Tangerang", "Bekasi"]

    # Add these functions at the start of main(), before the database connection
    def get_region_multiplier(region):
        # Jakarta and Tangerang have higher power usage
        multipliers = {
            "Jakarta": 2.5,
            "Tangerang": 1.8,
            "Bekasi": 1.2,
            "Bogor": 1.0,
            "Depok": 1.0
        }
        return multipliers.get(region, 1.0)

    def get_time_multiplier(timestamp):
        hour = timestamp.hour
        weekday = timestamp.weekday()  # 0-6 (Monday-Sunday)
        
        # Base multiplier for day/night
        if 8 <= hour <= 17:  # Daytime hours
            time_mult = 1.5
        elif 18 <= hour <= 22:  # Evening hours
            time_mult = 1.2
        else:  # Night hours
            time_mult = 0.6
            
        # Weekend adjustment for commercial buildings
        is_weekday = weekday < 5
        return time_mult, is_weekday

    def get_building_multiplier(building_type, is_weekday):
        if building_type in ["Kantor", "Pabrik", "Sekolah", "Ruko"]:
            return 1.5 if is_weekday else 0.2
        return 1.0

    # Create high usage entities
    high_usage_devices = random.sample(devices, int(n_devices * 0.1))  # 10% of devices
    high_usage_customers = random.sample(customers, int(n_customers * 0.15))  # 15% of customers

    # -----------------------------------------------
    # 4) Generate and insert data hour by hour
    # -----------------------------------------------
    current_ts = start_date
    insert_sql = """
    INSERT INTO l4_power_agg_stats (
        ts_hour, device_id, customer_id, building_type, region,
        usage_count, usage_sum, usage_min, usage_max
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
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

            # Apply multipliers
            region_mult = get_region_multiplier(region)
            time_mult, is_weekday = get_time_multiplier(current_ts)
            building_mult = get_building_multiplier(building_type, is_weekday)
            
            # Additional multiplier for high-usage entities
            entity_mult = 1.0
            if device_id in high_usage_devices:
                entity_mult *= random.uniform(2.0, 3.0)
            if customer_id in high_usage_customers:
                entity_mult *= random.uniform(1.5, 2.5)

            # Usage metrics with multipliers
            usage_count = random.randint(1, 100)
            base_min = random.uniform(0.0, 2.0)
            base_max = base_min + random.uniform(0.1, 5.0)
            
            # Apply all multipliers to the usage values
            total_mult = region_mult * time_mult * building_mult * entity_mult
            usage_min = base_min * total_mult
            usage_max = base_max * total_mult
            avg_usage = (usage_min + usage_max) / 2
            usage_sum = usage_count * avg_usage

            # Prepare the row
            row = (
                current_ts.strftime("%Y-%m-%d %H:%M:%S"),  # ts_hour
                device_id,
                customer_id,
                building_type,
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
    main(n_devices=200, n_customers=50)