import re
import sqlite3
from setup import *
import pandas as pd
from db_schemas import *
from datetime import datetime



# Function to generate SQL syntax for fund details
def generate_sql_syntax(question: str, db: str) -> str:
    table_schemas = table_schemas_map[db]
    prompt = f"""
    Rules:
    1. Return ONLY the SQL query, nothing else
    2. Only use columns that exist in the schemas
    3. Use proper SQL syntax for {db}
    4. Anticipate typos by using LIKE operator
    5. Anticipate uppercase/lowercase issues by using LOWER() function
    6. Sort the results by most relevant columns first
    7. Round the results to 2 decimal places
    Given these {db} table schemas:
    {table_schemas}
    and current date: {datetime.now().strftime("%Y-%m-%d")}
    Generate a SQL query to answer this question: {question} by following the rules.
    """
    return prompt



# Function to present SQL results
def present_sql_results(results: pd.DataFrame) -> str:   
    # Convert results to string format and append to prompt
    prompt = f"""
    Results found:
    {results.to_dict(orient='records')}
    Present data in an organized way.
    Split data to some tables if necessary. Elaborate on the data and provide insights.
    """
    return prompt