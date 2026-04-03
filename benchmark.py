import sqlite3
import time
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "mire_demo.db"

QUERY = """
SELECT
    s.segment_id,
    s.route_name,
    s.aadt,
    COUNT(c.crash_id) AS total_crashes
FROM mire_segments s
LEFT JOIN crashes c
    ON s.segment_id = c.segment_id
GROUP BY s.segment_id, s.route_name, s.aadt
ORDER BY total_crashes DESC;
"""

def time_query(conn: sqlite3.Connection, repeats: int = 5000) -> float:
    start = time.perf_counter()
    for _ in range(repeats):
        conn.execute(QUERY).fetchall()
    return time.perf_counter() - start

conn = sqlite3.connect(DB_PATH)

conn.execute("DROP INDEX IF EXISTS idx_crashes_segment_id")
conn.commit()
no_index_time = time_query(conn)

conn.execute("CREATE INDEX idx_crashes_segment_id ON crashes(segment_id)")
conn.commit()
with_index_time = time_query(conn)

print(f"Without index: {no_index_time:.6f} sec")
print(f"With index:    {with_index_time:.6f} sec")

conn.close()