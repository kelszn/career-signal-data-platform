import json


with open(
    "/Users/kelszn/Documents/Career_Signal/data/raw/techmap_cusor_sample.json",
    "r"
) as json_file:
    response_data = json.load(json_file)

jobs = response_data["result"]
first_job = jobs[1]

#print(response_data.keys())
#print(type(jobs))
#print(len(jobs))
#print(type(first_job))

#print(json.dumps(first_job, indent=4))

# inspect what columns the first job has 
jobs_keys = first_job.keys()
#print(jobs_keys)
for k, v in first_job.items():
    print(k, "\t", type(v))

print(response_data.keys())

print("jsonLD:")
print(json.dumps(first_job["jsonLD"], indent=4))

print("skills:")
print(json.dumps(first_job["skills"], indent=4))

print("careerLevel:")
print(json.dumps(first_job["careerLevel"], indent=4))

print("workType:")
print(json.dumps(first_job["workType"], indent=4))

print("\n\n\n\n\t\t\t\t")
    
print(jobs[3].keys(),"\n\n\n\n" ,jobs[4].keys())
# coiunt completeness of each iten n the jobs list of objects 

missing_feilds = [
    "",
    [],
    None,
    {}
]

for job in jobs:
    completeness = 0
    total_count  = len(job.keys())

    for k, v in job.items():
        if v not in missing_feilds:
            completeness +=1
    print(f"{completeness}/{total_count}")



'''

field_counts = {}

for job in jobs:
    for key in job.keys():
        if key in field_counts:
            field_counts[key] += 1
        else:
            field_counts[key] = 1

total_jobs = len(jobs)

for field, count in field_counts.items():
    print(f"{field}: {count}/{total_jobs}")'''
       



jsonld_field_counts = {}

for job in jobs:
    jsonld = job["jsonLD"]

    for key in jsonld.keys():
        if key in jsonld_field_counts:
            jsonld_field_counts[key] += 1
        else:
            jsonld_field_counts[key] = 1

total_jobs = len(jobs)

for field, count in jsonld_field_counts.items():
    print(f"{field}: {count}/{total_jobs}")



for job in jobs:
    title = job["title"]
    jdtitle = job["jsonLD"]["title"]
    print(repr(title))
    print(repr(jdtitle))
    print(title == jdtitle)



with open(f"/Users/kelszn/Documents/Career_Signal/data/raw/techmap_cursor_sample_002.json", "r") as json_file2:
    response_data2 = json.load(json_file2)

jobs2 = response_data2["result"]


print(json.dumps(jobs2, indent=4))

print(f"Pages =========={response_data2["page"]}")
print(f"PageSize =========={response_data2["pageSize"]}")
print(f"NumberOfRows =========={len(response_data2["result"])}")
print(f"TotalCount =========={response_data2["totalCount"]}")

print(f"Pages =========={response_data["page"]}")
print(f"PageSize =========={response_data["pageSize"]}")
print(f"NumberOfRows =========={len(response_data["result"])}")
print(f"TotalCount =========={response_data["totalCount"]}")
print()
print()
print(response_data["query"] == response_data2["query"])

# loop through a ist of jobs and extract the jsonLD identifier for the each page and the compare using sets the list of job identifier from the two pages
page_1_ids = []

for job in jobs:
    id = job["jsonLD"]["identifier"]
    page_1_ids.append(id)
print(len(page_1_ids))

page_2_ids = []
for job in jobs2:
    page_2_ids.append(job["jsonLD"]["identifier"])
print(len(page_2_ids))


page_1_ids = set(page_1_ids)
page_2_ids = set(page_2_ids)

print(type(page_1_ids), type(page_2_ids))

diff = page_1_ids.difference(page_2_ids)
dup = page_1_ids.intersection(page_2_ids)
print(len(diff))
print(dup)

print(type(response_data.keys()))