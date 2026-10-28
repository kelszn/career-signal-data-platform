import time  # to wait during requests
import requests # for HTTP requests
from dotenv import load_dotenv # to load environment variables to python environment
import os 
import json

# load environment variables
load_dotenv()

API_KEY = os.getenv("RAPIDAPI_KEY")
API_HOST = os.getenv("RAPIDAPI_HOST")

if not (API_KEY and API_HOST):
    print("Authentication Failed!")
    raise SystemExit("Authentication Failed!")
    
else:
    print("Authentication credentials were present !")
    


Base_url = "https://daily-international-job-postings.p.rapidapi.com"
Search_Endpoint = "/api/v2/jobs/search"
count_endpoint = "/api/v2/jobs/count"

URL = Base_url + Search_Endpoint
print(URL)

HEADERS = {
    "X-RapidAPI-Key" : API_KEY,
    "X-RapidAPI-Host": API_HOST
}

QUERY_PARAMS = {
    "countryCode" : "de",
    "title" : '"data engineer"',
    "dateCreatedMin" : "2026-09-01",
    "dateCreatedMax" : "2026-09-30"

}

current_cursor = "true"
max_batches = 3
batch_number = 1

while current_cursor and (batch_number <= max_batches):
    reqst_params = QUERY_PARAMS.copy()
    reqst_params['cursor'] = current_cursor
    response = requests.get(URL, params=reqst_params, headers=HEADERS )

    if response.status_code != 200:
        print(response.status_code)
        break

    resp_data = response.json()
    print(json.dumps(resp_data, indent=4))

    path = f"/Users/kelszn/Documents/Career_Signal/data/raw/Techmap_batch{batch_number:03}.json"

    with open(path, "w") as file_path:
        json.dump(resp_data, file_path, indent=4)
    print(batch_number)
    print(len(resp_data["result"]))

    next_cursor = resp_data.get("nextCursor")

    current_cursor = next_cursor
    batch_number += 1

    if current_cursor and batch_number<= max_batches:
        time.sleep(1)

if not current_cursor:
    print("API traversal finished naturally")

elif batch_number > max_batches:
    print("Stopped because development safety limit was reached")





