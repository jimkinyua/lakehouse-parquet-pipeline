import duckdb
import time

def run_lakehouse_benchmarks(lakehouse_path: str = "data/lakehouse"):
    conn = duckdb.connect()

    parquet_glob = f"{lakehouse_path}/*/*/*.parquet"

    print("=== Lakehouse Query Engine (DuckDB on Parquet) ===")
    
    # 1. Total volume and count by region
    t0 = time.perf_counter()
    res1 = conn.execute(f"""
        SELECT 
            region,
            COUNT(*) AS total_orders,
            ROUND(SUM(amount), 2) AS total_revenue,
            ROUND(AVG(amount), 2) AS avg_order_value
        FROM read_parquet('{parquet_glob}', hive_partitioning = true)
        GROUP BY region
        ORDER BY total_revenue DESC;
    """).fetchdf()
    d1 = (time.perf_counter() - t0) * 1000
    print(f"\n[Query 1] Regional Revenue Aggregations ({d1:.2f}ms):")
    print(res1)

    # 2. Partition pruned query (Only EMEA region)
    t0 = time.perf_counter()
    res2 = conn.execute(f"""
        SELECT 
            category,
            payment_method,
            COUNT(*) AS orders,
            ROUND(SUM(amount), 2) AS sales
        FROM read_parquet('{parquet_glob}', hive_partitioning = true)
        WHERE region = 'EMEA'
        GROUP BY category, payment_method
        ORDER BY sales DESC
        LIMIT 5;
    """).fetchdf()
    d2 = (time.perf_counter() - t0) * 1000
    print(f"\n[Query 2] Partition Pruning - Top Category/Payment in EMEA ({d2:.2f}ms):")
    print(res2)

if __name__ == "__main__":
    run_lakehouse_benchmarks()
