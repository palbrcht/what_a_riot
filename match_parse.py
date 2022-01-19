

import os
import requests
import pandas
from dotenv import load_dotenv
load_dotenv()


def get_match_data(matchid):        
    ###  Import API key from environment file
    ENV_API_KEY = os.getenv('RIOT_API_KEY')

    ###  Construct API query
    url_domain = 'https://americas.api.riotgames.com/lol/match/v5/matches/'
    url_match = matchid
    url_api_key = ENV_API_KEY
    
    ###  Query API for match data.
    print('Getting data for match ' + matchid + '...')
    query_string = (url_domain + url_match + '?api_key=' + url_api_key)
    api_request = requests.get(query_string)
    json_data = api_request.json()

    for iteration in range(0,10):
        ###   Compiling the data.
        temp_match_data = json_data['info']['participants'][iteration]

        temp_summmonerName = json_data['info']['participants'][iteration]['summonerName']
        temp_kills = json_data['info']['participants'][iteration]['kills']
        temp_deaths = json_data['info']['participants'][iteration]['deaths']
        temp_assists = json_data['info']['participants'][iteration]['assists']
        temp_champion = json_data['info']['participants'][iteration]['championName']
        print(temp_summmonerName+ ":" + ' Kills: ' + str(temp_kills) + " Assists: " + str(temp_assists) +" Deaths: " + str(temp_deaths) + " Champion: " + temp_champion)
        ###  Concatenating data into data frame.
        data = [{'summonerName': temp_summmonerName, 'kills': temp_kills, 'assists': temp_assists, 'deaths': temp_deaths, 'championName': temp_champion, 'matchid': matchid}]
        temp_df = pandas.DataFrame(data)

    print(data)

get_match_data('NA1_4182863077')


ENV_API_KEY = os.getenv('RIOT_API_KEY')
url_domain = 'https://americas.api.riotgames.com/lol/match/v5/matches/'
url_match = 'NA1_4182863077'
url_api_key = ENV_API_KEY

query_string = (url_domain + url_match + '?api_key=' + url_api_key)
api_request = requests.get(query_string)
json_data = api_request.json()

temp_match_data = json_data['info']['participants'][1]


###TODO: use key/value to loop through JSON data
for key, value in temp_match_data.items():
    temp_key = key
    #temp_key_2 = value['key']
    print(temp_key)
    print(value)
    #print(temp_key_2)
    data = [{key, value}]


pandas.DataFrame.from_dict(temp_match_data, orient='index')


output_df = pandas.DataFrame.from_dict(temp_match_data)

test = output_df.head(1) ##TODO: This is hacky but works. The JSON makes it have 2 rows due to children. This just leaves the top row.
test

print(os. getcwd())
output_df.to_csv('player_data.csv', header=True, index=False)
