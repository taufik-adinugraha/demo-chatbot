# Wealth Management Assistant API

A FastAPI-based application that provides wealth management assistance and portfolio optimization services.

## Components

### Data Directory
Contains various data files including:
- Mutual Fund data (Excel)
- Historical transaction data (CSV)
- Customer data (CSV)
- Optimized portfolio data (CSV)
- SQLite database file

### data.py
Handles all data-related operations:
- Loading data from Excel and CSV files
- SQLite database operations
- Data transformation and preprocessing
- Table schema management

### functions.py
Contains core business logic functions:
- User profile presentation
- Portfolio optimization
- Historical transaction analysis
- Portfolio recalculation
- SQL query generation for product details

### setup.py
Manages application setup and configuration:
- Environment variable loading
- OpenAI client initialization
- FastAPI application setup
- Database path configuration

### tools.py
Defines function calling tools for:
- User profile presentation
- Portfolio optimization
- Portfolio recalculation
- Historical transaction presentation
- SQL syntax generation

## Getting Started

1. Ensure all required data files are present in the `data/` directory
2. Set up environment variables:
   ```
   BATI_OPENAI_API_KEY=your_api_key
   ```
3. Install dependencies
4. Run the FastAPI application


## Environment Variables
- `BATI_OPENAI_API_KEY`: OpenAI API key for AI functionality
