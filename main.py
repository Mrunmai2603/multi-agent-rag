from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from db import SessionLocal

app = FastAPI()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/ask")
def ask_question(query: dict, db: Session = Depends(get_db)):
    user_query = query.get("query")
    
    # Example: simple SQL execution
    sql = "SELECT SUM(sales) FROM sales_table WHERE year=2024"
    result = db.execute(sql).fetchall()
    return {"query": user_query, "result": result}



