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
###  Examples
###

#queue type = 'norm', 'norms', 'solo', 'flex', 'aram'
#match count pick number between 0 and 100.
#fetch_match_list('INSERT_NAME_HERE', 'aram', 50)

fetch_time_wasted('INSERT_NAME_HERE', 'norms')