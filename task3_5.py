import pandas as pd
import re
import json
import sqlite3

def convert_to_usd(price):
    if price.startswith("$"):
        return float(price[1:])

    return float(price[1:]) * 1.2    

with open("task1_d.json", "r") as f:
    data = f.read()

clean_data = re.sub(r":([a-z]+)=>", r'"\1":', data)
data_json = json.loads(clean_data)

df = pd.DataFrame(data_json)
df["id"] = df["id"].astype(str)

with sqlite3.connect("task35.db") as conn:
    cursor = conn.cursor()

    conn.create_function("convert_to_usd", 1, convert_to_usd)

    df.to_sql("books", conn, if_exists="replace")

    cursor.execute("DROP TABLE IF EXISTS books_summary")

    cursor.execute("""CREATE TABLE books_summary AS SELECT 
    year, 
    COUNT(*) AS book_count,
    ROUND(AVG(convert_to_usd(price)), 2) AS average_price    
    FROM books 
    GROUP BY year
    """)

    df_summary = pd.read_sql("SELECT * FROM books_summary", conn)
    df_summary.to_csv("summary.csv", index=False)