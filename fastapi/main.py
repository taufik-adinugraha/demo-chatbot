import json
import sqlite3
import pandas as pd
from fastapi import HTTPException
from fastapi.responses import StreamingResponse, PlainTextResponse
from functions import *
from tools import *
from setup import *
from db_schemas import *
from report_queries import *
import clickhouse_connect

######################################################## Initialization
# System instructions
def get_system_instructions(table_schemas: str, language: str, response_type: str, number_of_sections: int):
    if response_type == "chat":
        system_instructions = f"""
        You are a data analyst, providing a help for user in providing insights from database with friendly and casual tone.
        Use simple, clear text for explanation. For headers, use <b><span style="color:#5772f9; font-size:18px;">some text</span></b>, do not use heading tags.
        Use <b><span style="color:#900C3F ;">some text or numbers</span></b> to highlight numbers and important information.
        Table schemas:
        {table_schemas}
        Always generate response in {language} language.
        Do not proceed if the query is not related to the insights from the database (mention to user what kind of data can be retrieved from the database).
        """
    elif response_type == "report":
        system_instructions = f"""
        You are a data analyst who is tasked with generating a formal and comprehensive report based on the data in the database.
        Give a thorough analysis and provide important insights. Use formal language as commonly used in the report.
        The report is divided into {number_of_sections} sections. If the section number is more than 1, that means the previous section has been completed, continue with the next section. 
        Always mention the section number and the title of the section in your response.
        For section titles, use <b><span style="color:#5772f9; font-size:18px;">some text</span></b>, do not use heading tags.
        For headers, use <b><span style="font-size:18px;">some text</span></b>, do not use heading tags.
        Use <b><span style="color:#900C3F ;">some text or numbers</span></b> to highlight numbers and important information.
        Always generate response in {language} language, including section titles and headers (Section is Bagian in Indonesian).
        """
    return system_instructions

function_map = {
    "generate_sql_syntax": generate_sql_syntax
}
######################################################## End of Initialization



######################################################## Chat API endpoint
@app.post("/api_chat")
async def api_chat(request: ChatRequest):
    # Initialize messages
    system_prompt = get_system_instructions(table_schemas, request.language, "chat", None)
    messages = [{"role": "system", "content": system_prompt}]
    messages.append({"role": "user", "content": request.query})
    
    # Call OpenAI API
    response_tool_call = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        tools=tools, # Use function calling
        temperature=0.7,
    )

    # Extract tool calls (function calling)
    tool_calls = response_tool_call.choices[0].message.tool_calls

    if tool_calls is not None:
        tool_call = tool_calls[0]
        function_name = tool_call.function.name

        # print(f'Calling function: {tool_call.function.name}')
        
        sql_generation_prompt = function_map[function_name](request.query, db)

        # Generate SQL query using OpenAI
        query_response = openai_client.beta.chat.completions.parse(
            model='gpt-4o',
            messages=[{"role": "system", "content": sql_generation_prompt}],
            temperature=0.7,
            response_format=SQLresponse, # Use structured output
        )
        
        # Extract the SQL syntax from the response
        sql_syntax = query_response.choices[0].message.parsed.sql_syntax
        
        # Execute generated query
        if db == "sqlite":
            conn = sqlite3.connect("dummy_data.db")
            results = pd.read_sql_query(sql_syntax, conn)
            conn.close()
        elif db == "clickhouse":
            clickhouse_client = clickhouse_connect.get_client(host=clickhouse_host, port=clickhouse_port, user=clickhouse_user, password=clickhouse_password)
            results = clickhouse_client.query_df(sql_syntax)
            clickhouse_client.close()

        if not results.empty:
            prompt = present_sql_results(results)
        else:
            prompt = f"No results found in the database. Ask user to check the query."
        messages.append({"role": "user", "content": prompt})

    try:
        def data_generator():
            # Call the OpenAI API
            response = openai_client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                temperature=1,
                stream=True
            )
            for chunk in response:
                content = chunk.choices[0].delta.content
                if content:
                    yield content
        
        return StreamingResponse(data_generator(), media_type="text/plain")

    except Exception as e:
        # Log the error for debugging purposes
        print(f"Error calling OpenAI API: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
######################################################## End of Chat API endpoint



######################################################## Report API endpoint
@app.post("/api_report")
async def api_report(request: ReportRequest):
    # Initialize messages
    system_prompt = get_system_instructions(table_schemas, request.language, "report", len(list_of_queries))
    
    async def data_generator():
        for query in list_of_queries:
            messages = [{"role": "system", "content": system_prompt}]
            messages.append({"role": "user", "content": query})

            # Call OpenAI API for tool calling
            response_tool_call = openai_client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                tools=tools,
                temperature=0.7,
            )

            tool_calls = response_tool_call.choices[0].message.tool_calls

            if tool_calls is not None:
                tool_call = tool_calls[0]
                function_name = tool_call.function.name

                # print(f'Calling function: {tool_call.function.name}')
                
                sql_generation_prompt = function_map[function_name](query, db)

                # Generate SQL query using OpenAI
                query_response = openai_client.beta.chat.completions.parse(
                    model='gpt-4o',
                    messages=[{"role": "system", "content": sql_generation_prompt}],
                    temperature=0.7,
                    response_format=SQLresponse, # Use structured output
                )
                
                # Extract the SQL syntax from the response
                sql_syntax = query_response.choices[0].message.parsed.sql_syntax
                
                # Execute generated query
                if db == "sqlite":
                    conn = sqlite3.connect("dummy_data.db")
                    results = pd.read_sql_query(sql_syntax, conn)
                    conn.close()
                elif db == "clickhouse":
                    clickhouse_client = clickhouse_connect.get_client(host=clickhouse_host, port=clickhouse_port, user=clickhouse_user, password=clickhouse_password)
                    results = clickhouse_client.query_df(sql_syntax)
                    clickhouse_client.close()

                if not results.empty:
                    prompt = present_sql_results(results)
                else:
                    prompt = f"No results found in the database. Ask user to check the query."
                messages.append({"role": "user", "content": prompt})

            try:
                # Stream the response for this query
                response = openai_client.chat.completions.create(
                    model="gpt-4o",
                    messages=messages,
                    temperature=1,
                    stream=True
                )
                for chunk in response:
                    content = chunk.choices[0].delta.content
                    if content:
                        yield content
                
                # Add a separator between sections
                yield "\n\n"

            except Exception as e:
                print(f"Error calling OpenAI API: {e}")
                yield f"Error processing query: {str(e)}\n\n"

    return StreamingResponse(data_generator(), media_type="text/plain")
######################################################## End of Report API endpoint