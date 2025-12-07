# agents/schema_agent.py
import re
from typing import List
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_conn():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )

class SchemaAgent:
    def __init__(self):
        pass

    def introspect(self) -> dict:
        conn = get_db_conn()
        cur = conn.cursor()
        cur.execute("""
            SELECT table_name, column_name, data_type
            FROM information_schema.columns
            WHERE table_schema='public'
        """)
        rows = cur.fetchall()
        schema = {}
        for table, column, dtype in rows:
            schema.setdefault(table, []).append((column, dtype))
        cur.close()
        conn.close()
        return schema

    def find_relevant(self, query: str) -> List[str]:
        """
        Very simple: look for known table/column keywords in query.
        Returns list of likely tables (ordered).
        """
        q = query.lower()
        schema = self.introspect()
        candidates = []
        # table name match
        for table in schema.keys():
            if table in q:
                candidates.append(table)
        # column name match
        for table, cols in schema.items():
            for col, _ in cols:
                if re.search(r'\b' + re.escape(col.lower()) + r'\b', q):
                    if table not in candidates:
                        candidates.append(table)
        # keyword heuristics
        keywords = {
            "sales": ["sale", "sales", "revenue", "amount", "total"],
            "customers": ["customer", "client", "buyer", "customers"],
            "employees": ["employee", "staff", "manager", "hired"],
            "projects": ["project", "projects", "project_name"]
        }
        for table, keys in keywords.items():
            if any(k in q for k in keys) and table not in candidates and table in schema:
                candidates.append(table)

        # fallback: return all tables
        if not candidates:
            candidates = list(schema.keys())
        return candidates
