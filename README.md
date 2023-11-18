# iMessage Data Analysis

## Requirements
You will need [PyObjC](https://pyobjc.readthedocs.io/en/latest/install.html) to be able to read some of the Objective-C data types that are serialized in the sqlite db. Also [vobject](https://pypi.org/project/vobject/) for reading your Contacts data

## Setup
1. Copy your iMessage SQLite file from `/Users/<username>/Library/Messages/chat.db`
2. Export your contacts to map phone numbers to names. Open Contacts App > Select All Contact Cards > File > Export > Export vCards. It will save to a file like "Your Name and 500+ others.vcf"
3. Change `vcard_path` in `process_contacts.py` then run `python3 process_contacts.py` to get a `contacts.csv` of all your contacts.
4. Change `SENDER_NAME` in `process_chat.py` to your name, then run `python3 process_chat.py` to get a nice denormalized sqlite db of your imessage chats stored in `chat_denormalized.db`

All the other files are just exporatory stuff