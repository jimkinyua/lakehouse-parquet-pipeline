import os
import json
import pyarrow as pa
import pyarrow.parquet as pq

SCHEMA = pa.schema([
    pa.field("order_id", pa.string()),
    pa.field("customer_id", pa.string()),
    pa.field("region", pa.string()),
    pa.field("category", pa.string()),
    pa.field("amount", pa.float64()),
    pa.field("currency", pa.string()),
    pa.field("payment_method", pa.string()),
    pa.field("order_timestamp", pa.string()),
    pa.field("year", pa.int32()),
    pa.field("month", pa.int32())
])

def ingest_to_lakehouse(input_json: str = "data/raw/orders_batch.json", output_lake_dir: str = "data/lakehouse"):
    if not os.path.exists(input_json):
        raise FileNotFoundError(f"Input file not found: {input_json}")

    os.makedirs(output_lake_dir, exist_ok=True)

    with open(input_json, "r", encoding="utf-8") as f:
        records = json.load(f)

    table = pa.Table.from_pylist(records, schema=SCHEMA)

    pq.write_to_dataset(
        table,
        root_path=output_lake_dir,
        partition_cols=["year", "region"],
        compression="snappy",
        use_dictionary=["region", "category", "payment_method"]
    )

    print(f"Ingested {table.num_rows} records into lakehouse partitioned dataset at: {output_lake_dir}")

if __name__ == "__main__":
    ingest_to_lakehouse()
