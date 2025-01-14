import os
import dotenv
from openai import OpenAI
from fastapi import FastAPI
from pydantic import BaseModel

# Load environment variables
dotenv.load_dotenv()

# Database
db = os.getenv("DB")

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("MY_OPENAI_API_KEY"))

# FastAPI app
app = FastAPI()

# Request model for the chat API
class ChatRequest(BaseModel):
    query: str
    language: str
    response_type: str
    number_of_sections: int | None = None

# Response model for the SQL syntax
class SQLresponse(BaseModel):
    sql_syntax: str

if db == "clickhouse":
    host = os.getenv("CLICKHOUSE_HOST")
    port = os.getenv("CLICKHOUSE_PORT")
    user = os.getenv("CLICKHOUSE_USER")
    password = os.getenv("CLICKHOUSE_PASSWORD")
