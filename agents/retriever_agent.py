# agents/retriever_agent.py
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

class RetrieverAgent:
    def __init__(self):
        pass

    def run_query(self, sql: str, params: dict):
        conn = get_db_conn()
        cur = conn.cursor()
        try:
            cur.execute(sql, params)
            cols = [desc[0] for desc in cur.description] if cur.description else []
            rows = cur.fetchall()
            cur.close()
            conn.close()
            # convert rows to list of dicts
            results = [dict(zip(cols, row)) for row in rows]
            return {"rows": results, "cols": cols}
        except Exception as e:
            cur.close()
            conn.close()
            return {"error": str(e)}

