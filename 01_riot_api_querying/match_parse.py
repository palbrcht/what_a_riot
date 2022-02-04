import os
from numpy import place
import requests
import pandas
from dotenv import load_dotenv
load_dotenv()

def get_match_data(matchId):        
    ###  Import API key from environment file
    ENV_API_KEY = os.getenv('RIOT_API_KEY')

    ###  Construct API query
    url_domain = 'https://americas.api.riotgames.com/lol/match/v5/matches/'
    url_match = matchId
    url_api_key = ENV_API_KEY
    
    ###  Query API for match data.
    print('Getting data for match ' + matchId + '...')
    query_string = (url_domain + url_match + '?api_key=' + url_api_key)
    api_request = requests.get(query_string)
    json_data = api_request.json()

    ###  TODO: this is hacky but works. it builds the structure of the DF that we will put the JSON data into.
    ###  This way we can concatenate all the other data into 1 df.
    ###  We start with the 0 slot to build the initial structure. Then in the loop we start with 1, not 0.

    temp_match_data = json_data['info']['participants'][0]
    placeholder_df = pandas.DataFrame.from_dict(temp_match_data)
    placeholder_df = placeholder_df.head(1)

    for iteration in range(1,10):
        ###   Compiling the data.
        temp_match_data = json_data['info']['participants'][iteration]

        output_df = pandas.DataFrame.from_dict(temp_match_data)

        temp_df  = output_df.head(1) ##TODO: This is hacky but works. The JSON makes it have 2 rows due to children. This just leaves the top row.
        
        placeholder_df = pandas.concat([placeholder_df, temp_df], ignore_index=True)

    placeholder_df['matchId'] = matchId

    return(placeholder_df)



get_match_data('NA1_4180281134')
