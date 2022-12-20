import csv
import requests

# Replace YOUR_JAMF_URL and YOUR_API_USERNAME_AND_PASSWORD with your own Jamf URL and API username and password
JAMF_URL = "YOUR_JAMF_URL"
API_USERNAME_AND_PASSWORD = "YOUR_API_USERNAME_AND_PASSWORD"

# Read the CSV file
with open('file.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    # Get the first column from the first row (assuming the first row contains the column names)
    first_column_name = next(csv_reader)[0]
    # Go back to the beginning of the file
    csv_file.seek(0)
    # Iterate through the rows of the CSV file
    for row in csv_reader:
        # Check if the first column is in Jamf
        if check_if_in_jamf(row[0]):
            print(f"'{row[0]}' is in Jamf")
        else:
            print(f"'{row[0]}' is not in Jamf")

def check_if_in_jamf(value):
    # Set up the API request to get the list of computers from Jamf
    headers = {'Accept': 'application/xml'}
    params = {'search': f"{first_column_name}={value}"}
    r = requests.get(f"{JAMF_URL}/JSSResource/computers", auth=API_USERNAME_AND_PASSWORD, headers=headers, params=params)
    # Check the response status code
    if r.status_code == 200:
        # Parse the XML response
        root = ET.fromstring(r.text)
        # Check if there are any computers with the specified value in the first column
        if int(root.find('size').text) > 0:
            return True
        else:
            return False
    else:
        print(f"Error: {r.status_code} {r.text}")
        return False
