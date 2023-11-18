"""
Query experiment on chat.db
"""

import json
import sqlite3

# Define the SQL statement you want to execute
sql_statement = """
select 
    m.date,
    m.text,
    m.handle_id,
    h.id as "Sender",
    m.service,
    m.is_from_me,
    cmj.message_id,
    cmj.chat_id,
    c.service_name,
    c.group_id
from message m 
left join chat_message_join cmj on m.ROWID = cmj.message_id  
left join chat c on cmj.chat_id = c.ROWID
left join handle h on m.handle_id = h.ROWID 
where c.group_id = 'F10BB39C-461D-4E72-8D4C-8718998118CF'
    and m.text is not null
    and m.service = c.service_name
order by "date" ASC
"""

# Connect to the SQLite database
connection = sqlite3.connect("chat.db")

try:
    # Create a cursor object using the cursor() method
    cursor = connection.cursor()

    # Execute the SQL statement
    cursor.execute(sql_statement)

    # Fetch all the rows
    rows = cursor.fetchall()

    # Get the column names
    columns = [description[0] for description in cursor.description]

    # Prepare the data for JSON
    results = [dict(zip(columns, row)) for row in rows]

    # Write the results to a JSON file
    with open("results.json", "w") as json_file:
        json.dump(results, json_file, indent=4)

    print("JSON file was created successfully.")

except sqlite3.Error as error:
    print("Error while executing SQL statement", error)

finally:
    # Close the cursor and connection to SQLite
    if connection:
        cursor.close()
        connection.close()
        print("SQLite connection is closed.")

# Note: Replace YOUR_SQL_STATEMENT_HERE with your actual SQL statement.
