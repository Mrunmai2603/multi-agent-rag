# agents/synthesizer_agent.py
from typing import List, Dict

class SynthesizerAgent:
    def __init__(self):
        pass

    def synthesize(self, query: str, sql: str, rows: List[Dict], meta: dict) -> str:
        """
        Create a human friendly answer.
        """
        if 'error' in meta:
            return f"Error executing SQL: {meta['error']}"

        # If aggregation result exists
        if len(rows) == 1 and 'result' in rows[0]:
            val = rows[0]['result']
            if val is None:
                return "Query executed but no matching records were found."
            return f"Result: {val}"

        # If rows returned, show summary + first few rows
        if rows:
            summary = f"I found {len(rows)} rows. Showing up to 5 rows:\n"
            preview = rows[:5]
            lines = []
            for r in preview:
                parts = [f"{k}: {v}" for k, v in r.items()]
                lines.append("; ".join(parts))
            return summary + "\n".join(lines)

        return "No matching records found."

