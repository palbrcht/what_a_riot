import os
from pickle import FALSE
import requests
import pandas
from dotenv import load_dotenv
load_dotenv()

### Custom functions
from match_parse import get_match_data

###TODO - dump results into a postgresql table so dont have to load from CSV
csv_source = os.path.join("what_a_riot.csv")

what_a_riot_import = pandas.read_csv(csv_source)

def compile_match_data():

    for temp_matchid in pandas.unique(what_a_riot_import['matchid']):
        print(temp_matchid)

        temp_match_data = get_match_data(temp_matchid)

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
    

    print('Query complete.')

    return(compiled_match_data)


test_df = compile_match_data()

print(test_df)