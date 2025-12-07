# create-files.ps1 — automatically creates all project files

$files = @{
    ".\agents\schema_agent.py" = 'def get_tables():`n    return ["customers", "employees", "projects", "sales"]'
    ".\agents\sql_generator_agent.py" = 'def generate_select(table, columns="*"):`n    return f"SELECT {columns} FROM {table};"'
    ".\agents\retriever_agent.py" = 'import psycopg2`n`ndef fetch_data(query):`n    conn = psycopg2.connect(dbname="ragdb", user="raguser", password="ragpass", host="localhost", port=5432)`n    cur = conn.cursor()`n    cur.execute(query)`n    rows = cur.fetchall()`n    cur.close()`n    conn.close()`n    return rows'
    ".\agents\synthesizer_agent.py" = 'def summarize_data(rows):`n    return f"Total rows fetched: {len(rows)}"'
    ".\rag_pipeline.py" = 'from agents.schema_agent import get_tables`nfrom agents.sql_generator_agent import generate_select`nfrom agents.retriever_agent import fetch_data`nfrom agents.synthesizer_agent import summarize_data`n`ndef run_pipeline():`n    tables = get_tables()`n    for table in tables:`n        query = generate_select(table)`n        rows = fetch_data(query)`n        summary = summarize_data(rows)`n        print(f"{table}: {summary}")`n`nif __name__ == "__main__":`n    run_pipeline()'
    ".\main.py" = 'from rag_pipeline import run_pipeline`n`nif __name__ == "__main__":`n    print("Starting RAG pipeline...")`n    run_pipeline()'
    ".\.env" = "DB_NAME=ragdb`nDB_USER=raguser`nDB_PASS=ragpass`nDB_HOST=localhost`nDB_PORT=5432"
    ".\requirements.txt" = "psycopg2-binary"
}

# Create agents folder if not exists
if (!(Test-Path ".\agents")) { mkdir .\agents }

foreach ($file in $files.Keys) {
    $content = $files[$file]
    Set-Content -Path $file -Value $content
}

Write-Host "All files created successfully!"
