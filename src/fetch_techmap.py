import os # for reading env file 
from dotenv import load_dotenv
import requests
import json 


#load our env 
load_dotenv()

# create variables to call api 
api_key = os.getenv('RAPIDAPI_KEY')
api_host = os.getenv('RAPIDAPI_HOST')

print(bool(api_key and api_host))

api_url = "https://daily-international-job-postings.p.rapidapi.com/api/v2/jobs/search"
page_number = 2
query_params = {
    "countryCode" : "de",
    "title": '"data engineer"',
    "isDuplicate" : "false",
    "dateCreatedMin" : "2026-09-01",
    "dateCreatedMax" : "2026-09-30",
    "page" : page_number
}

#define headerswhich is api keys or authoristion 

headers = {
    "x-rapidapi-key" : api_key,
    "x-rapidapi-host"      : api_host
}

response = requests.get(api_url, params=query_params, headers=headers )

if response.status_code == 200:
    response_data = response.json()
    with open(f"/Users/kelszn/Documents/Career_Signal/data/raw/techmap_sample{page_number:03d}.json", "w") as json_file:
        json.dump(response_data, json_file, indent=4)



else:
    print(response.status_code)
    print(response.headers)
    print(response.text)
