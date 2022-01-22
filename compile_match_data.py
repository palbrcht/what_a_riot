


import os
import requests
import pandas
from dotenv import load_dotenv
load_dotenv()


### Custom functions
from match_parse import get_match_data

csv_source = os.path.join("what_a_riot.csv")

what_a_riot_import = pandas.read_csv(csv_source)

for temp_matchid in pandas.unique(what_a_riot_import['matchid']):
    print(temp_matchid)

    ###TODO - loop through matches, use match_parse() function to compile




##get_match_data('NA1_4182863077')