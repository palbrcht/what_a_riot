import os
import requests
import pandas
from dotenv import load_dotenv
load_dotenv()

def get_last_match(summoner_name):
    ####  Load required
    import os
    import requests
    import pandas
    from dotenv import load_dotenv
    load_dotenv()

    ###  Import API key from environment file
    ENV_API_KEY = os.getenv('RIOT_API_KEY')
    
    ### Get account ID's for specific player.
    print('Getting last matches for ' + summoner_name + '...')
    print('Retrieving account info...' + summoner_name + '...')
    url_domain = 'https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/'
    url_api_key = ENV_API_KEY
    query_string = (url_domain + summoner_name + '?api_key=' + url_api_key)
    api_request = requests.get(query_string)
    json_data = api_request.json()
    summoner_puuid = json_data['puuid']
    print('Account info retrieved for ' + summoner_name + '....')

    ###  Get match history for specific player.
    url_domain = 'https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/'
    url_puuid = summoner_puuid
    url_api_key = ENV_API_KEY
    query_string = (url_domain + url_puuid + '/ids?count=5' + '&api_key=' + url_api_key)
    api_request = requests.get(query_string)
    json_data = api_request.json()
    temp_df = pandas.DataFrame(json_data, columns = ['matchid'])
    temp_df['puuid'] = summoner_puuid
    match_list = temp_df
    print(summoner_name + "'s last matches are: " )
    print(temp_df['matchid'])

    ###  Get match data for a specific match. Loop through all matches to get basic data for all participants.
    print('Pulling match data to verify values...')
    match_data = pandas.DataFrame(columns=['summonerName', 'kills' , 'assists' , 'deaths' , 'championName' , 'matchid'])

    for temp_match in match_list['matchid']:
        url_domain = 'https://americas.api.riotgames.com/lol/match/v5/matches/'
        url_match = temp_match
        url_api_key = ENV_API_KEY

        print('----------')
        print('----------')
        
        print('Getting data for match ' + temp_match + '...')
        query_string = (url_domain + url_match + '?api_key=' + url_api_key)
        api_request = requests.get(query_string)
        json_data = api_request.json()

        for iteration in range(0,10):
            ###   Compiling the data.
            temp_summ = json_data['info']['participants'][iteration]['summonerName']
            temp_kills = json_data['info']['participants'][iteration]['kills']
            temp_deaths = json_data['info']['participants'][iteration]['deaths']
            temp_assists = json_data['info']['participants'][iteration]['assists']
            temp_champion = json_data['info']['participants'][iteration]['championName']
            print(temp_summ + ":" + ' Kills: ' + str(temp_kills) + " Assists: " + str(temp_assists) +" Deaths: " + str(temp_deaths) + " Champion: " + temp_champion)
            ###  Concatenating data into data frame.
            data = [{'summonerName': temp_summ, 'kills': temp_kills, 'assists': temp_assists, 'deaths': temp_deaths, 'championName': temp_champion, 'matchid': temp_match}]
            temp_df = pandas.DataFrame(data)
            match_data = pandas.concat([match_data, temp_df], ignore_index=True)
    
        print('----------')
        print('----------')

    print('Match data compiled: ')

    print(match_data)

get_last_match('INSERT_NAME_HERE')
