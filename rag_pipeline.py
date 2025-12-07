# rag_pipeline.py
from agents.schema_agent import SchemaAgent
from agents.sql_generator_agent import SQLGeneratorAgent
from agents.retriever_agent import RetrieverAgent
from agents.synthesizer_agent import SynthesizerAgent
from typing import Dict, Any

class RAGPipelineSQL:
    def __init__(self):
        self.schema_agent = SchemaAgent()
        self.sql_gen = SQLGeneratorAgent()
        self.retriever = RetrieverAgent()
        self.synth = SynthesizerAgent()

    def ask(self, query: str) -> Dict[str, Any]:
        # 1) Schema step
        schema = self.schema_agent.introspect()
        relevant_tables = self.schema_agent.find_relevant(query)

        # 2) SQL generation
        sql, params = self.sql_gen.generate(query, relevant_tables)

        # 3) Execute
        result = self.retriever.run_query(sql, params or {})

        # 4) Synthesize
        answer = self.synth.synthesize(query=query, sql=sql, rows=result.get("rows", []), meta=result)

        return {
            "query": query,
            "schema_candidates": relevant_tables,
            "generated_sql": sql,
            "sql_params": params,
            "execution_result": result,
            "answer": answer
        }
