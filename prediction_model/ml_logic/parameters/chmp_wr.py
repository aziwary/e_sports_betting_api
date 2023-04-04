import pandas as pd
import numpy as np

def get_chmp_wr(champions_played, champions_wr):
    """
    Get average champion winrate of the champions played
    """

    champions = champions_played
    champions_wr_overview = champions_wr

    wr_chmp_player_1 = pd.merge(champions.reset_index(), champions_wr_overview, how='left', left_on=['patch', 'player_1'], right_on=['patch', 'name_clean'])["Win%"]
    wr_chmp_player_2 = pd.merge(champions.reset_index(), champions_wr_overview, how='left', left_on=['patch', 'player_2'], right_on=['patch', 'name_clean'])["Win%"]
    wr_chmp_player_3 = pd.merge(champions.reset_index(), champions_wr_overview, how='left', left_on=['patch', 'player_3'], right_on=['patch', 'name_clean'])["Win%"]
    wr_chmp_player_4 = pd.merge(champions.reset_index(), champions_wr_overview, how='left', left_on=['patch', 'player_4'], right_on=['patch', 'name_clean'])["Win%"]
    wr_chmp_player_5 = pd.merge(champions.reset_index(), champions_wr_overview, how='left', left_on=['patch', 'player_5'], right_on=['patch', 'name_clean'])["Win%"]
    wr_chmp_player_6 = pd.merge(champions.reset_index(), champions_wr_overview, how='left', left_on=['patch', 'player_6'], right_on=['patch', 'name_clean'])["Win%"]
    wr_chmp_player_7 = pd.merge(champions.reset_index(), champions_wr_overview, how='left', left_on=['patch', 'player_7'], right_on=['patch', 'name_clean'])["Win%"]
    wr_chmp_player_8 = pd.merge(champions.reset_index(), champions_wr_overview, how='left', left_on=['patch', 'player_8'], right_on=['patch', 'name_clean'])["Win%"]
    wr_chmp_player_9 = pd.merge(champions.reset_index(), champions_wr_overview, how='left', left_on=['patch', 'player_9'], right_on=['patch', 'name_clean'])["Win%"]
    wr_chmp_player_10 = pd.merge(champions.reset_index(), champions_wr_overview, how='left', left_on=['patch', 'player_10'], right_on=['patch', 'name_clean'])["Win%"]

    wr_chmp_player_1 = wr_chmp_player_1.replace([np.nan, 0],50)
    wr_chmp_player_2 = wr_chmp_player_2.replace([np.nan, 0],50)
    wr_chmp_player_3 = wr_chmp_player_3.replace([np.nan, 0],50)
    wr_chmp_player_4 = wr_chmp_player_4.replace([np.nan, 0],50)
    wr_chmp_player_5 = wr_chmp_player_5.replace([np.nan, 0],50)
    wr_chmp_player_6 = wr_chmp_player_6.replace([np.nan, 0],50)
    wr_chmp_player_7 = wr_chmp_player_7.replace([np.nan, 0],50)
    wr_chmp_player_8 = wr_chmp_player_8.replace([np.nan, 0],50)
    wr_chmp_player_9 = wr_chmp_player_9.replace([np.nan, 0],50)
    wr_chmp_player_10 = wr_chmp_player_10.replace([np.nan, 0],50)

    wr_chmp_list = [
    champions.reset_index()['gameid'],
    wr_chmp_player_1,
    wr_chmp_player_2,
    wr_chmp_player_3,
    wr_chmp_player_4,
    wr_chmp_player_5,
    wr_chmp_player_6,
    wr_chmp_player_7,
    wr_chmp_player_8,
    wr_chmp_player_9,
    wr_chmp_player_10,
    ]

    for i, series in enumerate(wr_chmp_list):
        if i == 0:
            chmp_wr = pd.DataFrame(series)
            chmp_wr.columns = ["gameid"]
        else:
            chmp_wr[f"player_{i}"] = series

    chmp_wr['avg_blue_champion_wr'] = (chmp_wr['player_1'] + chmp_wr['player_2'] + chmp_wr['player_3'] + chmp_wr['player_4'] + chmp_wr['player_5'])/5

    chmp_wr['avg_red_champion_wr'] = (chmp_wr['player_6'] + chmp_wr['player_7'] + chmp_wr['player_8'] + chmp_wr['player_9'] + chmp_wr['player_10'])/5

    chmp_wr['chmp_wr_diff'] = chmp_wr['avg_blue_champion_wr'] - chmp_wr['avg_red_champion_wr']

    chmp_wr = chmp_wr[['gameid', 'chmp_wr_diff']]

    return chmp_wr

def filter_league(dataframe, league_list):
    return dataframe.loc[dataframe['league'].isin(league_list)]
