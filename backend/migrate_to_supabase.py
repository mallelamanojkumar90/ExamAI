"""
Migrate data from local PostgreSQL to Supabase PostgreSQL.

Usage:
  1. Set SOURCE_DATABASE_URL to your current local Postgres connection string
  2. Set DATABASE_URL (or SUPABASE_DATABASE_URL) to your Supabase connection string
  3. Run: python migrate_to_supabase.py
"""

from __future__ import annotations

import json
import os
from datetime import datetime
from typing import Any

from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.engine import Engine

load_dotenv()

TABLE_ORDER = [
    "users",
    "exams",
    "exam_patterns",
    "syllabus",
    "questions",
    "exam_attempts",
    "answers",
    "study_materials",
    "subscriptions",
    "payments",
    "reports",
]


def get_engine(url: str, label: str) -> Engine:
    if not url:
        raise ValueError(f"{label} is not set")

    connect_args: dict[str, Any] = {}
    if url.startswith("postgresql"):
        connect_args = {"sslmode": "require", "connect_timeout": 30}

    return create_engine(url, echo=False, connect_args=connect_args, pool_pre_ping=True)


def serialize_value(value: Any) -> Any:
    if isinstance(value, datetime):
        return value
    return value


def fetch_rows(engine: Engine, table: str) -> list[dict[str, Any]]:
    with engine.connect() as conn:
        result = conn.execute(text(f"SELECT * FROM {table}"))
        return [dict(row._mapping) for row in result]


def reset_sequences(engine: Engine, table: str, pk_column: str) -> None:
    with engine.begin() as conn:
        conn.execute(
            text(
                f"""
                SELECT setval(
                    pg_get_serial_sequence('{table}', '{pk_column}'),
                    COALESCE((SELECT MAX({pk_column}) FROM {table}), 1),
                    (SELECT COUNT(*) > 0 FROM {table})
                )
                """
            )
        )


def insert_rows(engine: Engine, table: str, rows: list[dict[str, Any]]) -> int:
    if not rows:
        return 0

    columns = list(rows[0].keys())
    placeholders = ", ".join(f":{col}" for col in columns)
    column_list = ", ".join(columns)
    insert_sql = text(
        f"INSERT INTO {table} ({column_list}) VALUES ({placeholders})"
    )

    inserted = 0
    with engine.begin() as conn:
        for row in rows:
            payload = {key: serialize_value(value) for key, value in row.items()}
            result = conn.execute(insert_sql, payload)
            inserted += result.rowcount or 0

    pk_map = {
        "users": "user_id",
        "exams": "exam_id",
        "exam_patterns": "pattern_id",
        "syllabus": "syllabus_id",
        "questions": "question_id",
        "exam_attempts": "attempt_id",
        "answers": "answer_id",
        "study_materials": "material_id",
        "subscriptions": "subscription_id",
        "payments": "payment_id",
        "reports": "report_id",
    }
    if table in pk_map:
        reset_sequences(engine, table, pk_map[table])

    return inserted


def migrate_table(source: Engine, target: Engine, table: str) -> None:
    source_count = 0
    with source.connect() as conn:
        source_count = conn.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar() or 0

    if source_count == 0:
        print(f"  skip {table}: no rows")
        return

    rows = fetch_rows(source, table)
    inserted = insert_rows(target, table, rows)
    print(f"  {table}: migrated {inserted}/{len(rows)} rows")


def main() -> None:
    source_url = os.getenv("SOURCE_DATABASE_URL") or os.getenv("LOCAL_DATABASE_URL")
    target_url = os.getenv("SUPABASE_DATABASE_URL") or os.getenv("DATABASE_URL")

    if not source_url:
        raise SystemExit("Set SOURCE_DATABASE_URL to your local PostgreSQL connection string.")

    if not target_url or "supabase" not in target_url:
        raise SystemExit("Set DATABASE_URL or SUPABASE_DATABASE_URL to your Supabase connection string.")

    print("=" * 60)
    print("Migrating PostgreSQL -> Supabase")
    print("=" * 60)

    source = get_engine(source_url, "SOURCE_DATABASE_URL")
    target = get_engine(target_url, "SUPABASE_DATABASE_URL")

    source_tables = set(inspect(source).get_table_names())
    target_tables = set(inspect(target).get_table_names())

    for table in TABLE_ORDER:
        if table not in source_tables:
            print(f"  skip {table}: not in source")
            continue
        if table not in target_tables:
            print(f"  skip {table}: not in target (run schema migration first)")
            continue
        migrate_table(source, target, table)

    print("=" * 60)
    print("Migration complete")
    print("=" * 60)


if __name__ == "__main__":
    main()
