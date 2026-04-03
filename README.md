# MIRE-Inspired SQL Safety Data System

## Goal

Build a small SQL-based system inspired by MIRE (Model Inventory of Roadway Elements) to simulate how standardized roadway data supports safety analysis.

---

## Problem

Real-world safety data systems face several challenges:

- inconsistent data across sources
- lack of standardized schema
- difficulty integrating roadway, traffic, and crash data
- unreliable analysis due to poor data quality

---

## What I Built

A small SQLite-based system that:

1. loads messy raw datasets (roadway, intersection, crash)
2. standardizes them into a consistent MIRE-style schema
3. integrates data using SQL joins
4. creates summary views for analysis
5. performs a simple query performance comparison using indexing

---

## Data Pipeline

### Raw Tables

- `raw_segments`
- `raw_intersections`
- `raw_crashes`

### Clean Tables

- `mire_segments`
- `mire_intersections`
- `crashes`

### Views

- `segment_crash_summary`
- `intersection_crash_summary`

---

## Example Analysis

### Crash summary per segment

- joins roadway + crash data
- aggregates crash counts and severity

### Risk proxy

- crashes per lane
- identifies higher-risk segments

---

## Performance Experiment

Tested query performance before and after indexing:

- without index: slower join performance
- with index: improved query execution time

Insight:

> indexing becomes meaningful only after schema and join keys are well-defined

---

## Key Insights

1. The main challenge is not analysis, but making data usable and consistent across sources.
2. Standardized schema (like MIRE) is critical for reliable joins and integration.
3. Once the data model is stable, analysis becomes straightforward.
4. Performance optimization (e.g., indexing) is effective only after data consistency is established.

---

## Tech Stack

- SQLite
- Python (pandas)
- SQL

---

## Future Improvements

- larger dataset for more realistic performance testing
- additional roadway features (e.g., intersections, traffic control)
- more advanced safety metrics
