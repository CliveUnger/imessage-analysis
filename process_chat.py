import csv
import sqlite3

from Foundation import NSAttributedString, NSData, NSUnarchiver

# TODO Change this to be your name for proper sender/receiver name mapping
SENDER_NAME = "Clive Unger"


def create_sender_mapping(contacts_path):
    mapping = {}
    with open(contacts_path, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            mapping[row["Phone Number"]] = row["Name"]
            if row["Email"]:
                mapping[row["Email"]] = row["Name"]
    return mapping


def deserialize_attributed_string(blob_data):
    # Handle when blob_data is None
    if blob_data is None:
        return None

    ns_data = NSData.dataWithBytes_length_(blob_data, len(blob_data))
    if ns_data is None:
        raise ValueError("Unable to create NSData from blob")

    attributed_string = NSUnarchiver.unarchiveObjectWithData_(ns_data)
    if not isinstance(attributed_string, NSAttributedString):
        raise ValueError("Deserialized object is not an NSAttributedString")

    return attributed_string.string()


def denormalize_chat_db(chat_db_path, contacts_path):
    denormalize_query = """
    select 
        m.guid,
        datetime((m.date / 1000000000) + 978307200, 'unixepoch', 'localtime') as TextDate,
        m.text,
        m.attributedBody,
        m.handle_id,
        h.id as "Sender",
        m.service,
        m.is_from_me,
        cmj.message_id,
        cmj.chat_id,
        c.service_name,
        c.group_id,
        c.display_name,
        m.associated_message_type,
        associated_msg.guid as "associated_msg_guid",
        associated_msg.text as "Associated Text",
        associated_handle.id as "Associated Sender"
    from message m
    left join handle h on m.handle_id = h.ROWID
    left join chat_message_join cmj on m.ROWID = cmj.message_id  
    left join chat c on cmj.chat_id = c.ROWID
    left join message associated_msg ON associated_msg.guid = SUBSTR(m.associated_message_guid, 5) --LIKE '%' || m.guid
    left join handle associated_handle on associated_msg.handle_id = associated_handle.ROWID 
    where m.service = c.service_name
    order by m.date DESC
    """

    sender_mapping = create_sender_mapping(contacts_path)

    # Connect to your SQLite database chat.db
    with sqlite3.connect(chat_db_path) as conn:
        cursor = conn.cursor()
        # Execute a query to get the BLOB data
        # message_summary_info is a plist, but it seems attributedBody is not
        cursor.execute(denormalize_query)
        rows = cursor.fetchall()
        # convert row to list of lists instead of list of tuples
        rows = [list(row) for row in rows]

        # For each row run the deserialization function on the attributedBody column and add a new column with the result
        for r in rows:
            blob_data = r[3]
            plain_text = deserialize_attributed_string(blob_data)
            r[3] = plain_text

            sender = r[5]  # Assuming 'Sender' is in the 6th column
            r[5] = sender_mapping.get(sender, sender) if sender else SENDER_NAME

            associated_sender = r[16]  # Assuming 'Sender' is in the 5th column
            r[16] = (
                sender_mapping.get(associated_sender, associated_sender)
                if sender
                else SENDER_NAME
            )

    # Store the results in a new database
    with sqlite3.connect("chat_denormalized.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS message")
        cursor.execute(
            "CREATE TABLE message (guid, TextDate, text, attributedText, handle_id, Sender, service, is_from_me, message_id, chat_id, service_name, group_id, display_name, associated_message_type, associated_message_guid, associated_text, associated_sender)"
        )
        cursor.executemany(
            "INSERT INTO message VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", rows
        )
        conn.commit()


if __name__ == "__main__":
    denormalize_chat_db("chat.db", "contacts.csv")
