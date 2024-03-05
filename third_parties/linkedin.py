import requests
import os
def scrape_linkedin_profile(linkedin_profile_url: str):
    api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"
    api_key = os.environ.get("PROXYURL_API_KEY")  # 'WqninkymSXVGC7a_7ocAXA'
    print('zakt')
    print(api_key)
    headers = {"Authorization": "Bearer " + str(api_key)}
    params = {
        "linkedin_profile_url": linkedin_profile_url,
    }
    response = requests.get(api_endpoint, params=params, headers=headers)
    data = response.json()
    data = {k: v for k, v in data.items() if v not in ([], "", "", None)}
    if data.get("groups"):
        for group_dict in data.get("groups"):
            group_dict.pop("profile_pic_url")
    return data
