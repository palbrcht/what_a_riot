import os
import requests
import pandas
import time
from dotenv import load_dotenv
load_dotenv()

ENV_API_KEY = os.getenv('RIOT_API_KEY')
ENV_SUMMONER_NAME_LIST = os.getenv('SUMMONER_NAME_LIST')
summoner_name_list = ENV_SUMMONER_NAME_LIST.split(", ")

###
###  Fetch account info
###

player_data = pandas.DataFrame(columns=['id','accountId','puuid' ,'name'])

for temp_name in summoner_name_list:

  time.sleep(0.2)

  temp_url_param = 'https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/'
  temp_url_api_key = ENV_API_KEY
  query_string = (temp_url_param + temp_name + '?api_key=' + temp_url_api_key)
  api_request = requests.get(query_string)
  json_data = api_request.json()
  print('Account data retrieved for ' + temp_name + '.')

  temp_id = json_data['id']
  temp_accountId = json_data['accountId']
  temp_puuid = json_data['puuid']
  temp_name = json_data['name']

  temp_df = pandas.DataFrame([[temp_id, temp_accountId, temp_puuid, temp_name]],columns=['id','accountId','puuid' ,'name'])

  player_data = pandas.concat([player_data, temp_df], ignore_index=True)

#print(os. getcwd())
#player_data.to_csv('player_data.csv', header=True, index=False)

###
###  Fetch MatchID's by puuid.
###

match_list = pandas.DataFrame(columns=['matchid', 'puuid'])

for temp_puuid in player_data['puuid']:

  time.sleep(0.2)

  url_domain = 'https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/'
  url_puuid = temp_puuid
  url_start = '1641442774'
  url_queue = '420'
  url_api_key = ENV_API_KEY

  query_string = (url_domain + url_puuid + '/ids?startTime=' + url_start + '&queue=' + url_queue + '&api_key=' + url_api_key)
  api_request = requests.get(query_string)
  json_data = api_request.json()

  temp_df = pandas.DataFrame(json_data, columns = ['matchid'])
  temp_df['puuid'] = temp_puuid

  match_list = pandas.concat([match_list, temp_df], ignore_index=True)

#print(os. getcwd())
#match_list.to_csv('match_list.csv', header=True, index=False)

###
###  Fetch game durations by match id.
###

match_times = pandas.DataFrame(columns=['matchid', 'gameDuration'])

for temp_match in match_list['matchid']:

  time.sleep(1)

  url_domain = 'https://americas.api.riotgames.com/lol/match/v5/matches/'
  url_match = temp_match
  url_api_key = ENV_API_KEY

  print('Getting data for match ' + temp_match + '.')

  query_string = (url_domain + url_match + '?api_key=' + url_api_key)
  api_request = requests.get(query_string)
  json_data = api_request.json()

  print(query_string)

  temp_time = json_data['info']['gameDuration']
  temp_df = pandas.DataFrame([temp_time], columns = ['gameDuration'])
  temp_df['matchid'] = temp_match

  match_times = pandas.concat([match_times, temp_df], ignore_index=True)

# print(os. getcwd())
# match_times.to_csv('match_times.csv', header=True, index=False)

print(match_times)

total_time = match_times['gameDuration'].sum()
total_games = match_times.count()

print(total_time)
print(total_games)

