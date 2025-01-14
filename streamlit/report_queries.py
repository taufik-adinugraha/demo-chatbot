general_query = f"""
Default unit is kWh.
For subsections, use 1.1, 1.2, 1.3, etc where the first number is the section number and the second number is the subsection number.
"""

query_1 = f"""
Section 1: Monthly Total Usage
- Show the total consumption (sum of usage) across all devices/customers/locations for the month.
- Compare it with the previous month. Give also the percentage change.
{general_query}
"""

query_2 = f"""
Section 2: Monthly Average Usage
- Present the average monthly usage in the past 3 months, to give an easy way to gauge typical consumption levels
- How these values change over time
{general_query}
"""

query_3 = f"""
Section 3: Segmentation by Region
- Break down total usage (sum) and average usage by region. Present in both kWh and percentage of total usage.
- Show which regions have the highest consumption.
{general_query}
"""

query_4 = f"""
Section 4: Segmentation by Building Type
- Break down total usage (sum) and average usage by building type. Present in both kWh and percentage of total usage.
- Show which building types have the highest consumption.
{general_query}
"""

query_5 = f"""
Section 5: Top 5 Customers
- Show top 5 customers that had the largest total usage in the month.
{general_query}
"""


list_of_queries = [
    query_1,
    query_2,
    query_3,
    query_4,
    query_5,
]