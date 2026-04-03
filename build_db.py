import sqlite3
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = BASE_DIR / "mire_demo.db"

conn = sqlite3.connect(DB_PATH)

# Load raw data
segments = pd.read_csv(DATA_DIR / "raw_segments.csv")
intersections = pd.read_csv(DATA_DIR / "raw_intersections.csv")
crashes = pd.read_csv(DATA_DIR / "raw_crashes.csv")

# Save raw tables
segments.to_sql("raw_segments", conn, if_exists="replace", index=False)
intersections.to_sql("raw_intersections", conn, if_exists="replace", index=False)
crashes.to_sql("raw_crashes", conn, if_exists="replace", index=False)

# Standardize schema
segments = segments.rename(columns={
    "segment": "segment_id",
    "AADT": "aadt",
    "func_class": "functional_class",
    "lanes": "through_lanes",
    "surface": "surface_type"
})

intersections = intersections.rename(columns={
    "jxn_id": "junction_id",
    "road1_seg": "road1_segment_id",
    "road2_seg": "road2_segment_id",
    "traffic_ctrl": "intersection_traffic_control",
    "geometry": "intersection_geometry"
})

crashes = crashes.rename(columns={
    "seg_id": "segment_id"
})

# Fix missing lanes
segments["through_lanes"] = segments["through_lanes"].fillna(2).astype(int)
# Save clean tables
segments.to_sql("mire_segments", conn, if_exists="replace", index=False)
intersections.to_sql("mire_intersections", conn, if_exists="replace", index=False)
crashes.to_sql("crashes", conn, if_exists="replace", index=False)

# Create view
conn.execute("""
CREATE VIEW IF NOT EXISTS segment_crash_summary AS
SELECT
    s.segment_id,
    s.route_name,
    s.aadt,
    s.functional_class,
    s.through_lanes,
    COUNT(c.crash_id) AS total_crashes
FROM mire_segments s
LEFT JOIN crashes c
ON s.segment_id = c.segment_id
GROUP BY s.segment_id
""")

conn.commit()
conn.close()

print("Database created!")