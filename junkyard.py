
### Loops through the JSON object and its values
import os
import requests
import pandas
from dotenv import load_dotenv
load_dotenv()

ENV_API_KEY = os.getenv('RIOT_API_KEY')
url_domain = 'https://americas.api.riotgames.com/lol/match/v5/matches/'
url_match = 'NA1_4182863077'
url_api_key = ENV_API_KEY

query_string = (url_domain + url_match + '?api_key=' + url_api_key)
api_request = requests.get(query_string)
json_data = api_request.json()

temp_match_data = json_data['info']['participants'][1]

for key, value in temp_match_data.items():
    temp_key = key
    #temp_key_2 = value['key']
    print(temp_key)
    print(value)
    #print(temp_key_2)
    data = [{key, value}]
