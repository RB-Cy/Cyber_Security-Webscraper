#Import the necessary libraries: requests for the webscraper and pandas to create the CSV file
import requests
import pandas as pd

url = "https://jobs-api14.p.rapidapi.com/list" #API link from which data is obtained

#The boundaries in this section can be edited to refine the search results for the type of job needed
querystring = {
    "query": " entry-level, cyber security",
    "location": "United States",
    "distance": "1.0",
    "language": "en_GB",
    "remoteOnly": "false",
    "datePosted": "month",
    "employmentTypes": "fulltime;parttime;intern;contractor",
    "index": "0",

#Headers comprising of your personal api key and the host link required for authentication 
}

headers = {
    "x-rapidapi-key": "place your api key here",
    "x-rapidapi-host": "jobs-api14.p.rapidapi.com",
}

#This line sends a GET request to the url to retrievethe job data
response = requests.get(url, headers=headers, params=querystring)

#Converts the data into JSON format
jobs_data = response.json()

#Creates a list that the results will be sorted into
job_list= []

#Ensures that the variable jobs_data is a dictionary before proceeding with the GET requests 
if isinstance(jobs_data, dict) and 'jobs' in jobs_data:
    #Retrieves the required job details and places them into jobs_list
    jobs_list = jobs_data['jobs']  
    for job in jobs_list:
        job_title = job.get('title', ' ')
        company = job.get('company', ' ')
        description= job.get('description',' ')
        job_providers = job.get('jobProviders', [])
        if job_providers and isinstance(job_providers, list):
            actual_url = job_providers[0].get('url', ' ')
        location= job.get('location', ' ') 
        employment_type= job.get('employmentType', ' ')
        posted_time= job.get('datePosted', ' ')
        salary= job.get('salaryRange', ' ')
        
        # Organnizes and appends extracted job details to empty list created above 'job_list'
        
        print(f"Job Title: {job_title}, Company: {company}, URL: {actual_url}, Salary: {salary}")
        job_list.append({
            'Job Title': job_title,
            'Company': company,
            'Location':location,
            'Employment Type': employment_type,
            'Description': description,
            'Salary': salary,
            'Posted?': posted_time,
            'URL': actual_url
        })

    #Converts job_list to a DataFrame
    df = pd.DataFrame(job_list)

    # Converts job_list to a CSV file with 'encoding' to help with properly converting special characters
    df.to_csv('jobscraper_results.csv', index=False, encoding='utf-8')

    print(f'{len(jobs_list)} jobs saved to CSV.')   

else:
    print("Unexpected response structure")
