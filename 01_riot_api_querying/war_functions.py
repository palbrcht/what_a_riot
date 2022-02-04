import os
import requests
import pandas
import time
from dotenv import load_dotenv
load_dotenv()

ENV_API_KEY = os.getenv('RIOT_API_KEY')

###
### Gets associated account data from a summoner name.
###
def fetch_account_info(summoner_name):
    url_domain = 'https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/'
    url_api_key = ENV_API_KEY
    query_string = (url_domain + summoner_name + '?api_key=' + url_api_key)
    api_request = requests.get(query_string)
    json_data = api_request.json()

    account_id = json_data['id']
    account_accountId = json_data['accountId']
    account_puuid = json_data['puuid']
    account_name = json_data['name']
    account_df = pandas.DataFrame([[account_id, account_accountId, account_puuid, account_name]],columns=['id','accountId','puuid' ,'name'])

    print('Account data retrieved for ' + summoner_name + '.')
    print(account_df)
    return(account_df)


###
### Just gets puuid from a summoner name.
###
def fetch_puuid(summoner_name):
    url_domain = 'https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/'
    url_api_key = ENV_API_KEY
    query_string = (url_domain + summoner_name + '?api_key=' + url_api_key)
    api_request = requests.get(query_string)
    json_data = api_request.json()
    print('PUUID retrieved for ' + summoner_name + '.')
    account_puuid = json_data['puuid']
    return(account_puuid)

###
###  Compiles list of matches for a given summoner.
###  Can indicate queue type and how many.
###
def fetch_match_list(summoner_name, queue, match_count):

    ###TODO: make better list of queue types translating to the queue number.

    ###TODO: make it so no match_count input would just be max count (100).

    ###TODO: make a time-based query (past day, week, month, etc.)

    ###TODO: make a 'all' queue type option.

    if queue == 'solo': 
      queue_value = 420
    
    if queue == 'norms':
      queue_value = 400

    if queue == 'norm':
      queue_value = 400

    if queue == 'flex':
      queue_value = 410

    #if queue == 'all':
    #  queue_value = NULL

    if queue == 'aram':
      queue_value = 450
    
    player_puuid = fetch_puuid(summoner_name)

    match_list = pandas.DataFrame(columns=['matchid', 'puuid'])

    url_domain = 'https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/'
    url_puuid = str(player_puuid)
    url_start = '1641442774'
    url_queue = str(queue_value)
    url_api_key = ENV_API_KEY

    query_string = (url_domain + url_puuid + '/ids?startTime=' + url_start + '&queue=' + str(url_queue) + '&count=' + str(match_count) +'&api_key=' + url_api_key)
    api_request = requests.get(query_string)
    json_data = api_request.json()

    temp_df = pandas.DataFrame(json_data, columns = ['matchid'])
    temp_df['puuid'] = player_puuid
    print(temp_df)
    return(temp_df)

###
###  Calculates time spent playing for a given queue.
###
###  #queue type = 'norm', 'norms', 'solo', 'flex', 'aram'
###  #match count pick number between 0 and 100.
###
def fetch_time_wasted(summoner_name, queue):
    
    match_list = fetch_match_list(summoner_name, queue, 100)
   
    match_times = pandas.DataFrame(columns=['matchid', 'gameDuration'])

    for temp_match in match_list['matchid']:
     
      time.sleep(0.9)
      url_domain = 'https://americas.api.riotgames.com/lol/match/v5/matches/'
      url_match = temp_match
      url_api_key = ENV_API_KEY
    
      print('Getting data for match ' + temp_match + '.')
      query_string = (url_domain + url_match + '?api_key=' + url_api_key)
      api_request = requests.get(query_string)
      json_data = api_request.json()
    
      temp_time = json_data['info']['gameDuration']
      temp_df = pandas.DataFrame([temp_time], columns = ['gameDuration'])
      temp_df['matchid'] = temp_match
      match_times = pandas.concat([match_times, temp_df], ignore_index=True)

    print(match_times)
    total_time = match_times['gameDuration'].sum()
    total_games = match_times.count()
    print(summoner_name + ' has played ' + queue + ' games for: ')
    print(str(total_time) + ' seconds.')
    print(str((total_time/60)) + ' minutes.')
    print(str(((total_time/60)/60))+ ' hours.')
    return(total_time)

###
###  Get previous matches of a player.
###
def fetch_last_matches(summoner_name, number_matches):
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
    url_number_matches = number_matches
    query_string = (url_domain + url_puuid + '/ids?count=' + str(number_matches) + '&api_key=' + url_api_key)
    api_request = requests.get(query_string)
    json_data = api_request.json()
    temp_df = pandas.DataFrame(json_data, columns = ['matchid'])
    temp_df['puuid'] = summoner_puuid
    match_list = temp_df
    print(summoner_name + "'s last matches are: " )
    print(temp_df['matchid'])

    ###  Get match data for a specific match. Loop through all matches to get basic data for all participants.
    print('Pulling match data to verify values...')
    match_data = pandas.DataFrame(columns=['summonerName', 'kills', 'deaths', 'assists', 'championName', 'matchid'])

    for temp_match in match_list['matchid']:
        url_domain = 'https://americas.api.riotgames.com/lol/match/v5/matches/'
        url_match = temp_match

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
            print(temp_summ + ":" + ' Kills: ' + str(temp_kills) + " Deaths: " + str(temp_deaths) + " Assists: " + str(temp_assists)  + " Champion: " + temp_champion)
            ###  Concatenating data into data frame.
            data = [{'summonerName': temp_summ, 'kills': temp_kills, 'deaths': temp_deaths, 'assists': temp_assists, 'championName': temp_champion, 'matchid': temp_match}]
            temp_df = pandas.DataFrame(data)
            match_data = pandas.concat([match_data, temp_df], ignore_index=True)
    
        
        print('----------')
    print('Match data compiled: ')
    print(match_data)


###
###  Merge manually entered grade data with Riot API data.
###
def compile_match_data():

    ###TODO: Fix pathing. Holding this here temporarily to add context for fixing later.
    csv_source = os.path.join("what_a_riot.csv")

    what_a_riot_import = pandas.read_csv(csv_source)

    for temp_matchId in pandas.unique(what_a_riot_import['matchId']):
        print(temp_matchId)

        temp_match_data = get_match_data(temp_matchId)

        try:
            compiled_match_data
        except NameError:
            var_exists = False
        else:
            var_exists = True

        if var_exists == False:
            compiled_match_data = temp_match_data
    
        if var_exists == True:
            compiled_match_data = pandas.concat([compiled_match_data, temp_match_data], ignore_index=True)

        print(compiled_match_data)
    

    print('Compilation complete.')

    return(compiled_match_data)


###
###  Find matchid given specific parameters.
###
def find_match(summoner_name, req_kills, req_deaths, req_assists, req_champ):
    
    ####  Load required
    import os
    import requests
    import pandas
    from dotenv import load_dotenv
    import time
    load_dotenv()

    ###  Import API key from environment file
    ENV_API_KEY = os.getenv('RIOT_API_KEY')
    
    ### Get account ID's for specific player.
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
    url_number_matches = 20
    query_string = (url_domain + url_puuid + '/ids?count=' + str(url_number_matches) + '&api_key=' + url_api_key)
    api_request = requests.get(query_string)
    json_data = api_request.json()
    temp_df = pandas.DataFrame(json_data, columns = ['matchid'])
    temp_df['puuid'] = summoner_puuid
    match_list = temp_df
    print('Recent matches retrieved for ' + summoner_name + '....')

    ###  Get match data for a specific match. Loop through all matches to get basic data for all participants.
    match_data = pandas.DataFrame(columns=['summonerName', 'kills', 'deaths', 'assists', 'championName', 'matchid'])

    
    print('Finding match...')
    for temp_match in match_list['matchid']:
        #time.sleep(1)
        url_domain = 'https://americas.api.riotgames.com/lol/match/v5/matches/'
        url_match = temp_match

        print("...")
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
            ###  Concatenating data into data frame.
            data = [{'summonerName': temp_summ, 'kills': temp_kills, 'deaths': temp_deaths, 'assists': temp_assists, 'championName': temp_champion, 'matchid': temp_match}]
            temp_df = pandas.DataFrame(data)
            match_data = pandas.concat([match_data, temp_df], ignore_index=True)


    desired_match = match_data[match_data["summonerName"] == summoner_name]
    desired_match = desired_match[desired_match["kills"] == req_kills]
    desired_match = desired_match[desired_match["deaths"] == req_deaths]
    desired_match = desired_match[desired_match["assists"] == req_assists]
    desired_match = desired_match[desired_match["championName"] == req_champ]

    desired_match_id = str(desired_match['matchid'])

    print(desired_match)
    print('Match found. Match ID: ' + desired_match_id)
