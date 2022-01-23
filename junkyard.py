
### Loops through the JSON object and its values
# import os
# import requests
# import pandas
# from dotenv import load_dotenv
# load_dotenv()

# ENV_API_KEY = os.getenv('RIOT_API_KEY')
# url_domain = 'https://americas.api.riotgames.com/lol/match/v5/matches/'
# url_match = 'NA1_4182863077'
# url_api_key = ENV_API_KEY

# query_string = (url_domain + url_match + '?api_key=' + url_api_key)
# api_request = requests.get(query_string)
# json_data = api_request.json()

# temp_match_data = json_data['info']['participants'][1]

# for key, value in temp_match_data.items():
#     temp_key = key
#     #temp_key_2 = value['key']
#     print(temp_key)
#     print(value)
#     #print(temp_key_2)
#     data = [{key, value}]


###
###
###





##############
##############  Merging test
##############
# import os
# import pandas
# csv_source = os.path.join("training_data.csv")

# training_data_import = pandas.read_csv(csv_source)

# csv_source = os.path.join("what_a_riot.csv")

# what_a_riot_import = pandas.read_csv(csv_source)


# merged_df = pandas.merge(training_data_import, what_a_riot_import, on=['matchId','summonerName'])

# #print(merged_df)

# merged_df.to_csv('training_data_export_test.csv', header=True, index=False)



###############
##############
#############
#############


# ENV_API_KEY = os.getenv('RIOT_API_KEY')
# url_domain = 'https://americas.api.riotgames.com/lol/match/v5/matches/'
# url_match = 'NA1_4182863077'
# url_api_key = ENV_API_KEY

# query_string = (url_domain + url_match + '?api_key=' + url_api_key)
# api_request = requests.get(query_string)
# json_data = api_request.json()

# temp_match_data = json_data['info']['participants'][1]


# ###TODO: use key/value to loop through JSON data
# for key, value in temp_match_data.items():
#     temp_key = key
#     #temp_key_2 = value['key']
#     print(temp_key)
#     print(value)
#     #print(temp_key_2)
#     data = [{key, value}]


# pandas.DataFrame.from_dict(temp_match_data, orient='index')


# output_df = pandas.DataFrame.from_dict(temp_match_data)

# test = output_df.head(1) ##TODO: This is hacky but works. The JSON makes it have 2 rows due to children. This just leaves the top row.
# test

# print(os. getcwd())
# output_df.to_csv('player_data.csv', header=True, index=False)