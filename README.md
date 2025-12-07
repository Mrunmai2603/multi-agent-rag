Multi-Agent RAG System for Natural Language Querying of a Relational Database

Introduction-

This is my project where I have built a Multi-Agent Retrieval-Augmented Generation (RAG) system with SQL database support.
The main idea is to use multiple agents to process queries, fetch data from a database, and generate useful responses.
I have implemented the backend using FastAPI and integrated PostgreSQL for storing and managing structured data.

What This Project Does-

* Uses multiple AI agents to handle different tasks
* Retrieves information from an SQL database
* Generates responses using RAG pipeline
* Provides clean API endpoints using FastAPI
* Easy to test through Postman
* Well-structured and simple to understand

Technologies Used-

* Python 3.12
* FastAPI
* SQLAlchemy
* PostgreSQL
* Docker (for database)
* Postman (for testing APIs)

Project Folder Structure-

```
multi-agent-rag-sql/
│
├── main.py               # FastAPI main application
├── database.py           # DB connection and models
├── agents/               # Logic for different agents
├── docs/                 # API screenshots and documentation
├── requirements.txt      # Packages used in the project
└── README.md
```

How to Run the Project-

 1. Clone or open the project folder

```
cd multi-agent-rag-sql
```

 2. Create a virtual environment

```
python -m venv .venv
```

 3. Activate the environment

Windows:

```
.venv\Scripts\activate
```

4. Install required libraries

```
pip install -r requirements.txt
```

 5. Start PostgreSQL using Docker

```
docker run --name rag-postgres -e POSTGRES_PASSWORD=ragpass -p 5432:5432 -d postgres
```

6. Run the FastAPI server

```
uvicorn main:app --reload
```

 7. Test the APIs

Open Postman and hit the endpoints:

 GET Example

`http://127.0.0.1:8000/users`

#### POST Example

`http://127.0.0.1:8000/agents/run`

## Sample API Response

```json
[
  {
    "id": 1,
    "name": "Alice",
    "email": "alice@example.com"
  },
  {
    "id": 2,
    "name": "Bob",
    "email": "bob@example.com"
  }
]
```

My Role-

I have worked on:

* Setting up FastAPI
* Designing the database structure
* Creating agent logic
* Writing API endpoints
* Testing everything on Postman
* Preparing documentation and folder structure

Conclusion-

This project shows how multiple agents can work together with a database-backed RAG system.
I have tried to keep the code clean, modular, and easy to understand so it can be extended further.








