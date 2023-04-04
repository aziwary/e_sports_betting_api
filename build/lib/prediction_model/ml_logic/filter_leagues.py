import pandas as pd

def filter_league(dataframe, league_list):
    return dataframe.loc[dataframe['league'].isin(league_list)]
