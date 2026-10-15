# Lakehouse Parquet Pipeline

A lightweight, serverless Data Lakehouse ingestion and query pipeline using **PyArrow**, **Polars**, and **DuckDB**. Transforms raw semi-structured JSON batch feeds into Hive-partitioned columnar Parquet datasets for low-latency analytical queries.

## Architecture

```text
  [ Raw JSON Event Logs ]
            │
            ▼
  [ PyArrow Ingestion Engine ]
   - Strict Schema Casting
   - Dictionary Encoding (Categories, Regions)
   - Snappy Compression
            │
            ▼
  [ Lakehouse Partitioned Layout ]
   data/lakehouse/
     ├── year=2026/
     │   ├── region=NA/
     │   │   └── data.parquet
     │   ├── region=EMEA/
     │   │   └── data.parquet
     │   └── ...
            │
            ▼
  [ DuckDB Query Engine ]
   - Hive Partition Pruning
   - Vectorized Columnar Scans
```

## Project Structure

```text
├── .gitignore
├── requirements.txt         # PyArrow, Polars, DuckDB
├── generator.py             # Generates sample JSON transaction feeds
├── ingest_parquet.py        # PyArrow partitioned dataset writer
├── query_lakehouse.py       # Vectorized SQL queries & partition pruning
└── README.md
```

## Quickstart

### 1. Install dependencies
```bash
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
```

### 2. Generate raw transaction data
```bash
python generator.py
```
Generates 1,000 multi-region JSON order events in `data/raw/orders_batch.json`.

### 3. Ingest into Partitioned Parquet Lakehouse
```bash
python ingest_parquet.py
```
Parses JSON, validates against Arrow schema, applies dictionary encoding, and writes partitioned Parquet files under `data/lakehouse/year=YYYY/region=XX/`.

### 4. Run Analytical Benchmarks
```bash
python query_lakehouse.py
```
Executes vectorized aggregation queries directly on the Parquet files using DuckDB with automatic partition pruning.

## Design Highlights

- **Storage Efficiency**: Snappy compression combined with dictionary encoding for low-cardinality strings (`region`, `category`, `payment_method`) achieves significant size reduction over raw JSON.
- **Partition Pruning**: Queries filtering by partition keys (`region = 'EMEA'`) skip scanning irrelevant directories on disk.
- **Zero Cluster Overhead**: Fast columnar analytics on modern hardware without spinning up Spark or Hadoop clusters.
