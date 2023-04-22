import mysql.connector
import requests
import csv
from requests.exceptions import Timeout, SSLError, RequestException
from bs4 import BeautifulSoup
import phpserialize

# Connect to the database
db = mysql.connector.connect(
  host="127.0.0.1",
  user="root",
  password="",
  database="muvap"
)

# Create a cursor object to execute queries
cursor = db.cursor()

# Execute the query to fetch all URLs from the database
query = "SELECT meta_value  FROM `gq5yigg_postmeta` WHERE meta_key = '_product_attributes';"
cursor.execute(query)

# Create a list to store the output
output = [["URL", "Status"]]

# Loop through the results and check each URL
for result in cursor.fetchall():
    meta_value = result[0]
    attributes = phpserialize.loads(meta_value.encode("utf-8"))
    weburl = attributes.get(b"weburl", {}).get(b"value", b"").decode("utf-8", "ignore")
    if weburl:
        try:
            # Make a GET request to the URL
            response = requests.get(weburl, timeout=10)

            # Check if the response status code is in the 2xx range
            if response.status_code >= 200 and response.status_code < 300:
                status = "OK"
            else:
                status = f"Broken (status code: {response.status_code})"

        except Timeout:
            status = "Timed out"

        except SSLError:
            status = "SSL error"

        except RequestException as e:
            status = f"Error: {e}"

        # Append the URL and status to the list
        output.append([weburl, status])
        print(f"{weburl}: {status}")

# Close the database connection
db.close()

# Write the output to a CSV file
with open("output.csv", mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerows(output)
