import csv
import re

import vobject


def format_phone_number(number):
    # Remove any non-digit characters
    digits = re.sub(r"\D", "", number)

    # Check if the number has 10 digits
    if len(digits) == 10:
        return "+1" + digits
    elif len(digits) == 11 and digits.startswith("1"):
        return "+" + digits
    else:
        # Return the original number if it's not in the expected format
        return number


def process_contacts(vcard_path, output_path):
    # Read the vCard file
    with open(vcard_path, "r") as vcard_file:
        vcard_data = vcard_file.read()

    # Parse the vCard data
    vcards = vobject.readComponents(vcard_data)

    # Open CSV file for writing
    with open(output_path, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Name", "Phone Number", "Email"])  # Column headers

        # Extract data from each vCard and write to CSV
        for vcard in vcards:
            name = vcard.fn.value if hasattr(vcard, "fn") else "No Name"
            phone_number = (
                format_phone_number(vcard.tel.value) if hasattr(vcard, "tel") else ""
            )
            email = vcard.email.value if hasattr(vcard, "email") else ""
            writer.writerow([name, phone_number, email])

    print(f"Contacts have been exported to {output_path}")


if __name__ == "__main__":
    # Path to your exported vCard file
    vcard_path = "vcards/Clive Unger and 598 others.vcf"

    # Path to the CSV file you want to create
    csv_path = "contacts.csv"

    process_contacts(vcard_path, csv_path)
