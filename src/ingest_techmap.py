import time  # to wait during requests
import requests # for HTTP requests
from dotenv import load_dotenv # to load environment variables to python environment
import os 
import json
from requests.exceptions import ConnectionError, Timeout



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
max_batches = 1
batch_number = 1
stopped_reason = None

MAX_ATTEMPTS = 2
RETRY_WAIT_SECONDS = 3
TIMEOUT_SECONDS = 30 


while current_cursor and (batch_number <= max_batches):
    reqst_params = QUERY_PARAMS.copy()
    reqst_params['cursor'] = current_cursor

    response = None
    attempts = 1

    while attempts <= MAX_ATTEMPTS:

        try:
            response = requests.get(URL, params=reqst_params, headers=HEADERS , timeout=TIMEOUT_SECONDS)
            break
        except (ConnectionError, Timeout)as error:

            print(f"connection failed on Batch{batch_number:03}, {type(error).__name__}")
            attempts +=1    
            if attempts <= MAX_ATTEMPTS:
                print("Retrying Connection...")
                time.sleep(RETRY_WAIT_SECONDS)
                
    if response is None :
        print(f'Batch_{batch_number:03} failed after {MAX_ATTEMPTS} attempts to retry')
        stopped_reason = f"No answer after {MAX_ATTEMPTS} attempts"
        break
    if response.status_code != 200:
        print(response.headers)
        print(f'Batch{batch_number:03}: {response.status_code}')
        stopped_reason = f"Unsuccessful status code : {response.status_code}"
        break
    
    #parse json payload
    resp_data = response.json()
    print(json.dumps(resp_data, indent=4))

    if "result" not in resp_data:
        print(f"{batch_number:03} response has an unexpected shape")
        stopped_reason = "unexpected response shape"
        break


    #dynamic path
    path = f"/Users/kelszn/Documents/Career_Signal/data/raw/Techmap_batch{batch_number:03}.json"

    #write json to file path
    with open(path, "w") as file_path:
        json.dump(resp_data, file_path, indent=4)
    print(len(resp_data["result"]))

    next_cursor = resp_data.get("nextCursor")

    current_cursor = next_cursor
    batch_number += 1

    if current_cursor and batch_number<= max_batches:
        time.sleep(1)
if stopped_reason is not None:
    print(f"run stopped early: request stopped on batch{batch_number:03} -- {stopped_reason}")
elif  not current_cursor:
    print("API traversal finished naturally")

elif batch_number > max_batches:
    print("Stopped because development safety limit was reached")





