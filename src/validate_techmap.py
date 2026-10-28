import json
from pathlib import Path # makes objects out of a path string

raw_folder = Path("/Users/kelszn/Documents/Career_Signal/data/raw")

#set file pattern
file_pattern = "Techmap_batch*.json"

#GET matching_files from raw_directory using glob
matching_files = raw_folder.glob(file_pattern)

matching_files = sorted(matching_files)

all_ids = [] # empty list where we will add all ids and compare using set

for f in matching_files:
    with open(f, "r") as file:
        data = json.load(file)
    jobs = data["result"]

    batch_ids = []

    for job in jobs :
        batch_ids.append(job["jsonLD"]["identifier"]) 
        all_ids.append(job["jsonLD"]["identifier"])  
    print(f.name)
    print(len(batch_ids))
    

total_ids = len(all_ids)
unique_ids = len(set(all_ids))

if total_ids == unique_ids:
    print("No Duplicates")
else:
    print("duplicates exists")



