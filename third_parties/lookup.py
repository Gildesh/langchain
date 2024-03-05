import requests

api_key = "WqninkymSXVGC7a_7ocAXA"
headers = {"Authorization": "Bearer " + api_key}
api_endpoint = "https://nubela.co/proxycurl/api/linkedin/profile/resolve"
params = {
    "company_domain": "https://www.grazitti.com/",
    "first_name": "Abhay",
    "similarity_checks": "include",
    "enrich_profile": "enrich",
    "location": "Seattle",
    "title": "Co-chair",
    "last_name": "Gates",
}
response = requests.get(api_endpoint, params=params, headers=headers)
print(response.content)
