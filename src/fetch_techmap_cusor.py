import json # to parse json, convert json to string and python object (list, dictionar)
import os  # retrieves environment variables
from dotenv import load_dotenv # loads values from .env into the environment
import requests


load_dotenv() # loads the environment files

API_HOST = os.getenv("RAPIDAPI_HOST")
API_KEY = os.getenv("RAPIDAPI_KEY")
print(bool(API_KEY and API_HOST))

if not (API_KEY and API_HOST):
    print("failed!")
else:
    print("SUCCESS")
      


# get authorization header, query params and url

HEADERS = {
    "X-RapidAPI-Host" : API_HOST,
    "X-RapidAPI-Key" : API_KEY
}

QUERY_PARAMS = {
    "countryCode" : "de",
    "isDuplicate": "false",
    "title": '"data engineer"',
    "dateCreatedMin" : "2026-09-01",
    "dateCreatedMax" : "2026-09-30",
    "cursor" : "true"
}

API_URL = "https://daily-international-job-postings.p.rapidapi.com/api/v2/jobs/search"

response = requests.get(API_URL, params=QUERY_PARAMS, headers=HEADERS)

if response.status_code == 200:
    response_data = response.json()
    next_cursor = response_data.get("nextCursor")
    with open("/Users/kelszn/Documents/Career_Signal/data/raw/techmap_cusor_sample.json", "w") as json_file:
        json.dump(response_data, json_file, indent=4) # dumps a fine printed json into a json file

    print("Second request status:", response.status_code)
    print("Jobs returned:", len(response_data["result"]))
    print("Total count:", response_data["totalCount"])
    print("Next cursor:", next_cursor)
else:
    print(response.status_code)
    





if next_cursor:
    QUERY_PARAMS["cursor"] = next_cursor

    response2 = requests.get(
        API_URL,
        params=QUERY_PARAMS,
        headers=HEADERS
    )

    if response2.status_code == 200:
        response_data2 = response2.json()

        next_cursor2 = response_data2.get("nextCursor")

        print("Second request status:", response2.status_code)
        print("Jobs returned:", len(response_data2["result"]))
        print("Total count:", response_data2["totalCount"])
        print("Next cursor:", next_cursor2)

        with open(
            "/Users/kelszn/Documents/Career_Signal/data/raw/techmap_cursor_sample_002.json",
            "w"
        ) as json_file:
            json.dump(response_data2, json_file, indent=4)

    else:
        print(response2.status_code)
        print(response2.text)





'''
START
  ↓
current_cursor = initial cursor mode
batch_number = 1
max_batches = 3
  ↓
WHILE
cursor exists
AND
batch_number <= max_batches
  ↓
put current cursor into request parameters
  ↓
send HTTP request
  ↓
successful?
 ├── NO → stop/report failure
 │
 └── YES
       ↓
     parse JSON
       ↓
     save complete raw batch
       ↓
     read nextCursor
       ↓
     current_cursor = nextCursor
       ↓
     batch_number += 1
       ↓
     LOOP

'''

