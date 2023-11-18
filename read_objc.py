"""
Experimenting with how to read Objective-C datatypes in Python
"""

import sqlite3

from Foundation import NSAttributedString, NSData, NSUnarchiver


def deserialize_nsunarchiver(blob_data):
    ns_data = NSData.dataWithBytes_length_(blob_data, len(blob_data))
    if ns_data is None:
        raise ValueError("Unable to create NSData from blob")

    # Initialize the unarchiver
    unarchiver = NSUnarchiver.alloc().initForReadingWithData_(ns_data)
    if unarchiver is None:
        raise ValueError("Unable to create NSUnarchiver from NSData")

    # Attempt to decode the object
    try:
        deserialized_data = unarchiver.decodeObject()
        return deserialized_data
    except Exception as e:
        raise ValueError(f"Error during decoding: {e}")


def deserialize_attributed_string(blob_data):
    ns_data = NSData.dataWithBytes_length_(blob_data, len(blob_data))
    if ns_data is None:
        raise ValueError("Unable to create NSData from blob")

    attributed_string = NSUnarchiver.unarchiveObjectWithData_(ns_data)
    if not isinstance(attributed_string, NSAttributedString):
        raise ValueError("Deserialized object is not an NSAttributedString")

    return attributed_string.string()


# Connect to your SQLite database
conn = sqlite3.connect("chat.db")
cursor = conn.cursor()

# Execute a query to get the BLOB data
# message_summary_info is a plist, but it seems attributedBody is not
cursor.execute("SELECT attributedBody FROM message WHERE ROWID = ?;", (369151,))
row = cursor.fetchone()

if row:
    blob_data = row[0]
    # print(blob_data)

    # Attempt to deserialize the BLOB data
    # blob_data should be the raw binary data from your SQLite BLOB field
    deserialized_data = deserialize_nsunarchiver(blob_data)
    print(deserialized_data)

    plain_text = deserialize_attributed_string(blob_data)
    print(plain_text)

# Close the database connection
conn.close()
