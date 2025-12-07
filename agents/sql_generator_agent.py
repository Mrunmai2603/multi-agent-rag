# agents/sql_generator_agent.py
import re
from typing import Tuple, List
import sqlparse

class SQLGeneratorAgent:
    def __init__(self):
        pass

    def parse_time_ref(self, query: str):
        """
        Recognize phrases like 'last year', '2023', 'Q1 2023', 'last month'.
        Return a tuple (start_date, end_date) as strings, or None.
        Very simple heuristics.
        """
        q = query.lower()
        import datetime
        today = datetime.date.today()
        # last year
        m = re.search(r'last year', q)
        if m:
            start = datetime.date(today.year - 1, 1, 1)
            end = datetime.date(today.year - 1, 12, 31)
            return (start.isoformat(), end.isoformat())

        # explicit year e.g., 2023
        m = re.search(r'\b(20\d{2})\b', q)
        if m:
            year = int(m.group(1))
            return (f"{year}-01-01", f"{year}-12-31")

        # last month
        m = re.search(r'last month', q)
        if m:
            first = (today.replace(day=1) - datetime.timedelta(days=1)).replace(day=1)
            last = (today.replace(day=1) - datetime.timedelta(days=1))
            return (first.isoformat(), last.isoformat())

        return None

    def detect_aggregate(self, query: str) -> Tuple[str, str]:
        """
        Detect if user asks for SUM/AVG/COUNT.
        Returns (agg_function, agg_field) or (None, None)
        """
        q = query.lower()
        if "total" in q or "sum" in q or "total sales" in q or "sum of" in q:
            return ("SUM", "amount")
        if "average" in q or "avg" in q:
            return ("AVG", "amount")
        if "count" in q or "how many" in q:
            # try to infer what to count: customers or sales
            if "customer" in q:
                return ("COUNT", "distinct customer_id")
            return ("COUNT", "*")
        return (None, None)

    def generate(self, query: str, tables: List[str]) -> Tuple[str, dict]:
        """
        Return (sql, params)
        Very simple: support single table selects, aggregates, basic joins
        """
        q = query.lower()
        agg_func, agg_field = self.detect_aggregate(query)

        time_range = self.parse_time_ref(query)
        params = {}

        # If aggregate requested and sales in tables
        if agg_func and "sales" in tables:
            sql = f"SELECT {agg_func}({agg_field}) as result FROM sales"
            where_clauses = []
            if time_range:
                where_clauses.append("sale_date BETWEEN %(start)s AND %(end)s")
                params["start"], params["end"] = time_range
            # possible filter by city or project
            city_match = re.search(r'in (\w+)', q)
            if city_match and "customers" in tables:
                # join customers
                sql = ("SELECT {agg}({field}) as result FROM sales "
                       "JOIN customers ON sales.customer_id = customers.customer_id").format(agg=agg_func, field=agg_field)
                where_clauses.append("customers.city ILIKE %(city)s")
                params["city"] = city_match.group(1)
            if where_clauses:
                sql += " WHERE " + " AND ".join(where_clauses)
            return (sqlparse.format(sql, reindent=True), params)

        # If question about employees or projects or customers: attempt select
        # simple pattern: SELECT * FROM <table> WHERE <col> = value
        for table in ["sales", "customers", "employees", "projects"]:
            if table in tables:
                # try filters: by customer name
                if "customer" in q and "name" in q:
                    name = re.search(r'customer named ([\w\s]+)', q)
                    if name:
                        sql = f"SELECT * FROM customers WHERE name ILIKE %(name)s"
                        params["name"] = f"%{name.group(1).strip()}%"
                        return (sql, params)
                # by employee
                if "employee" in q and "sales" in q:
                    emp = re.search(r'by ([\w\s]+)', q)
                    if emp:
                        sql = ("SELECT s.* FROM sales s "
                               "JOIN employees e ON s.employee_id = e.employee_id "
                               "WHERE e.name ILIKE %(ename)s")
                        params["ename"] = f"%{emp.group(1).strip()}%"
                        return (sql, params)
                # fallback: select recent rows from that table
                sql = f"SELECT * FROM {table} ORDER BY 1 DESC LIMIT 10"
                return (sql, params)

        # ultimate fallback: select top 5 sales
        return ("SELECT * FROM sales ORDER BY sale_date DESC LIMIT 10", params)

