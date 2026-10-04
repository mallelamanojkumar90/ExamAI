"""Export local PostgreSQL data as SQL INSERT statements for Supabase import."""

import json
import os
from datetime import date, datetime
from decimal import Decimal

from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect, text

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


def fmt(value):
    if value is None:
        return "NULL"
    if isinstance(value, bool):
        return "TRUE" if value else "FALSE"
    if isinstance(value, (int, float, Decimal)):
        return str(value)
    if isinstance(value, (dict, list)):
        return "'" + json.dumps(value).replace("'", "''") + "'::jsonb"
    if isinstance(value, (datetime, date)):
        return f"'{value.isoformat()}'"
    if isinstance(value, str):
        return "'" + value.replace("\\", "/").replace("'", "''") + "'"
    return "'" + str(value).replace("'", "''") + "'"


def main() -> None:
    engine = create_engine(os.getenv("DATABASE_URL"))
    output_path = os.path.join(os.path.dirname(__file__), "supabase_data_export.sql")

    with engine.connect() as conn, open(output_path, "w", encoding="utf-8") as out:
        out.write("BEGIN;\n")
        for table in TABLE_ORDER:
            if table not in inspect(engine).get_table_names():
                continue
            rows = conn.execute(text(f"SELECT * FROM {table}")).mappings().all()
            out.write(f"\n-- {table}: {len(rows)} rows\n")
            for row in rows:
                columns = list(row.keys())
                values = ", ".join(fmt(row[column]) for column in columns)
                column_list = ", ".join(columns)
                out.write(
                    f"INSERT INTO {table} ({column_list}) VALUES ({values});\n"
                )
        out.write("COMMIT;\n")

    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
