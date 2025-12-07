import random
import datetime
import psycopg2
from psycopg2.extras import execute_values

conn = psycopg2.connect(
    dbname="ragdb",
    user="raguser",
    password="ragpass",
    host="localhost",
    port=5432
)

cur = conn.cursor()

customer_ids = list(range(1, 11))
project_ids = list(range(1, 6))
employee_ids = list(range(1, 7))

rows = []
start = datetime.date(2019, 1, 1)
end = datetime.date(2024, 12, 31)

for _ in range(200):
    customer = random.choice(customer_ids)
    project = random.choice(project_ids)
    employee = random.choice(employee_ids)
    amount = round(random.uniform(5000, 200000), 2)
    delta = random.randint(0, (end - start).days)
    sale_date = start + datetime.timedelta(days=delta)
    rows.append((customer, project, employee, amount, sale_date))

execute_values(cur,
    "INSERT INTO sales (customer_id, project_id, employee_id, amount, sale_date) VALUES %s",
    rows
)

conn.commit()
cur.close()
conn.close()

print("Seeded additional sales rows.")

