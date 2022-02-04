import os
import requests
import pandas
from dotenv import load_dotenv
load_dotenv()
import time

### Custom functions
from match_parse import get_match_data

###TODO - dump results into a postgresql table so dont have to load from CSV
csv_source = os.path.join("what_a_riot.csv")

what_a_riot_import = pandas.read_csv(csv_source)

def compile_match_data():

    for temp_matchId in pandas.unique(what_a_riot_import['matchId']):
        time.sleep(0.9)
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

compiled_data = compile_match_data()

###TODO Change the matching to be puuid.
###     OR make the manual input the puuid, not summoner name.
###     We are losing information on 'Rando' inputted names that got S's. They are not matching.

merged_df = pandas.merge(compiled_data, what_a_riot_import, how = 'left', on=['matchId','championName'])

merged_df.to_csv('training_data_export.csv', header=True, index=False)