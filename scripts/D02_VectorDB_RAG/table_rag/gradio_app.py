import gradio as gr
import pandas as pd
import sqlite3
from typing import Tuple, Optional
import os

# Import RAG functions from table_rag.py
from table_rag import rag, create_sql_query

# SQL table schema information
SQL_TABLE_INFO = """
coffee_sales (
    sale_id INT PRIMARY KEY,
    product_name VARCHAR(100),
    origin_country VARCHAR(50),
    bean_type VARCHAR(50),
    roast_level VARCHAR(20),
    price_per_kg DECIMAL(6,2),
    quantity_kg DECIMAL(6,2),
    sale_date DATE,
    customer_id INT,
    region VARCHAR(50),
    organic BOOLEAN,
    certification VARCHAR(50)
);
"""

# Database path
DB_PATH = "coffee_sales.db"


def validate_sql_query(query: str) -> bool:
    """Validate that the SQL query is a SELECT statement only."""
    query_upper = query.strip().upper()
    return query_upper.startswith("SELECT") and not any(
        keyword in query_upper
        for keyword in ["DROP", "DELETE", "UPDATE", "INSERT", "ALTER", "CREATE", "TRUNCATE"]
    )


def validate_input(user_query: str) -> Tuple[bool, Optional[str]]:
    """Validate user input."""
    if not user_query or not user_query.strip():
        return False, "Please enter a question."
    if len(user_query) > 1000:
        return False, "Question is too long. Please keep it under 1000 characters."
    return True, None


def fetch_information_from_db_with_columns(query: str) -> Tuple[list, list]:
    """Fetch information from database and return results with column names."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        columns = [description[0] for description in cursor.description] if cursor.description else []
        conn.close()
        return results, columns
    except Exception as e:
        conn.close()
        print(f"Error executing query: {e}")
        return [], []


def format_query_results(results: list, columns: list) -> pd.DataFrame:
    """Format database query results as a pandas DataFrame."""
    if not results:
        return pd.DataFrame()
    
    if columns:
        return pd.DataFrame(results, columns=columns)
    else:
        # Fallback: use generic column names
        num_cols = len(results[0]) if results else 0
        columns = [f"Column_{i+1}" for i in range(num_cols)]
        return pd.DataFrame(results, columns=columns)


def process_query(user_query: str) -> Tuple[str, pd.DataFrame, str]:
    """
    Main processing function for Gradio.
    Returns: (sql_query, results_dataframe, ai_answer)
    """
    # Validate input
    is_valid, error_msg = validate_input(user_query)
    if not is_valid:
        return "", pd.DataFrame(), f"Error: {error_msg}"
    
    try:
        # Generate SQL query
        sql_result = create_sql_query(user_query, SQL_TABLE_INFO)
        sql_query = sql_result['sql_query']
        
        # Validate SQL query (ensure SELECT only)
        if not validate_sql_query(sql_query):
            return (
                sql_query,
                pd.DataFrame(),
                "Error: Generated query is not a safe SELECT statement. Please try rephrasing your question."
            )
        
        # Execute query and get results with column names
        retrieved_info, columns = fetch_information_from_db_with_columns(sql_query)
        results_df = format_query_results(retrieved_info, columns)
        
        # Generate AI answer using RAG
        ai_answer = rag(user_query, SQL_TABLE_INFO)
        
        return sql_query, results_df, ai_answer
        
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        return "", pd.DataFrame(), error_message


# Custom CSS for better styling
css = """
.gradio-container {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}
h1 {
    text-align: center;
    color: #2c3e50;
}
"""


# Create Gradio interface
with gr.Blocks(css=css, title="Table RAG - Coffee Sales Query System") as demo:
    # Header section
    gr.Markdown(
        """
        # ☕ Table RAG - Coffee Sales Query System
        
        Ask natural language questions about the coffee sales database and get AI-powered answers!
        
        **How it works:**
        1. Enter your question in natural language
        2. The system generates a SQL query
        3. Results are retrieved from the database
        4. An AI assistant provides a natural language answer
        
        **Example questions:**
        - "What is the total sales over all time?"
        - "What's the average price of organic coffee compared to non-organic?"
        - "How does the price depend on the roast level?"
        """,
        elem_classes=["header"]
    )
    
    with gr.Row():
        with gr.Column(scale=2):
            # Input section
            query_input = gr.Textbox(
                label="Your Question",
                placeholder="Enter your question about coffee sales...",
                lines=3,
                max_lines=5
            )
            submit_btn = gr.Button("Ask Question", variant="primary", size="lg")
        
        with gr.Column(scale=1):
            gr.Markdown(
                """
                ### 💡 Tips
                - Be specific in your questions
                - Ask about sales, prices, regions, or product details
                - The system will show you the SQL query it generates
                """
            )
    
    # Output sections
    with gr.Tabs():
        with gr.TabItem("AI Answer"):
            answer_output = gr.Markdown(
                label="AI-Generated Answer",
                value="Your answer will appear here..."
            )
        
        with gr.TabItem("SQL Query"):
            sql_output = gr.Code(
                label="Generated SQL Query",
                language="sql",
                value="-- SQL query will appear here --"
            )
        
        with gr.TabItem("Query Results"):
            results_output = gr.Dataframe(
                label="Database Results",
                wrap=True,
                interactive=False
            )
    
    # Connect the submit button to the processing function
    submit_btn.click(
        fn=process_query,
        inputs=query_input,
        outputs=[sql_output, results_output, answer_output]
    )
    
    # Also allow Enter key to submit
    query_input.submit(
        fn=process_query,
        inputs=query_input,
        outputs=[sql_output, results_output, answer_output]
    )
    
    # Footer
    gr.Markdown(
        """
        ---
        **Note:** This system uses LangChain with Groq (Llama 3.3 70B) to generate SQL queries and provide answers.
        All database queries are read-only (SELECT statements only).
        """
    )


if __name__ == "__main__":
    # Check if database exists
    if not os.path.exists(DB_PATH):
        print(f"Warning: Database file '{DB_PATH}' not found.")
        print("Please run data_prep.py first to create the database.")
    
    # Launch the Gradio app
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False
    )
