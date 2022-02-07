import discord
from discord.ext import commands
import os
import requests
import pandas
from dotenv import load_dotenv


###
###  Load .env variables...
###
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
ENV_API_KEY = os.getenv('RIOT_API_KEY')


client = discord.Client()
bot = commands.Bot(command_prefix='!')

###
###
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
###
###

@bot.command(name='last', help='Gets account info from a Summoner name.')
async def last(ctx, summoner_name: str):

    await ctx.send('Fetching the last game for ' + summoner_name + ".... one moment....")

    summoner_puuid = fetch_puuid(summoner_name)
    
    ###  Get match history for specific player.
    url_domain = 'https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/'
    url_puuid = summoner_puuid
    url_api_key = ENV_API_KEY
    query_string = (url_domain + url_puuid + '/ids?count=' + str(1) + '&api_key=' + url_api_key)
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

    await ctx.send(summoner_name + " 's last game:")
    await ctx.send(match_data)


@bot.command(name='find', help='Gets account info from a Summoner name.')
async def find(ctx, summoner_name:str, req_kills:int, req_deaths:int, req_assists:int):
    
    await ctx.send("Searching for game...")
    
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
            print(temp_summ)
            temp_kills = json_data['info']['participants'][iteration]['kills']
            temp_deaths = json_data['info']['participants'][iteration]['deaths']
            temp_assists = json_data['info']['participants'][iteration]['assists']
            temp_champion = json_data['info']['participants'][iteration]['championName']
            ###  Concatenating data into data frame.
            data = [{'summonerName': temp_summ, 'kills': temp_kills, 'deaths': temp_deaths, 'assists': temp_assists, 'championName': temp_champion, 'matchid': temp_match}]
            temp_df = pandas.DataFrame(data)
            match_data = pandas.concat([match_data, temp_df], ignore_index=True)
            print(match_data)

    


    desired_match = match_data[match_data["summonerName"] == summoner_name]
    desired_match = desired_match[desired_match["kills"] == req_kills]
    desired_match = desired_match[desired_match["deaths"] == req_deaths]
    desired_match = desired_match[desired_match["assists"] == req_assists]

    desired_match_id = str(desired_match['matchid'])

    print(desired_match)
    print('Match found. Match ID: ' + desired_match_id)
    await ctx.send('Match found. Match ID: ' + desired_match_id)
    await ctx.send(desired_match)


bot.run(DISCORD_TOKEN)