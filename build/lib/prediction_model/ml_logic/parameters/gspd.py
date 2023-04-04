import pandas as pd
import numpy as np

def get_gspd(df_2021, df_2022, df_2023, weighting_n):
    """
    Get gspd
    """

    ### Historical gspd
    # 2022
    tmp = pd.DataFrame(df_2022.groupby('teamid').count().iloc[:, 0])
    gspd_in_2021 = df_2021.groupby('teamid')['gspd'].mean() * 100
    historical_gspd_2022 = pd.merge(tmp, gspd_in_2021, how='left', left_index=True, right_index=True)
    historical_gspd_2022.fillna(value=0, inplace=True)

    # 2023
    tmp = pd.DataFrame(df_2023.groupby('teamid').count().iloc[:, 0])
    gspd_in_2022 = df_2022.groupby('teamid')['gspd'].mean() * 100
    historical_gspd_2023 = pd.merge(tmp, gspd_in_2022, how='left', left_index=True, right_index=True)
    historical_gspd_2023.fillna(value=0, inplace=True)

    n_games = weighting_n

    ### Dynamic gspd
    # 2022
    tmp = df_2022[['date', 'teamid', 'gameid', 'gspd']].reset_index().set_index(['teamid', 'date']).sort_index()
    games_played_dynamic = pd.DataFrame()

    # Need to adapt, so that the information is as before the game
    games_played_dynamic['total_games'] = tmp.groupby('teamid')['gspd'].cumcount()
    games_played_dynamic['dynamic_weighting'] = np.clip(0, games_played_dynamic['total_games']/n_games, 1) # dynamic weighting factor
    gspd_dynamic = pd.DataFrame(tmp.groupby('teamid')['gspd'].shift()).groupby('teamid')['gspd'].cumsum()

    tmp = pd.merge(tmp, games_played_dynamic,  how='left', left_on=['date','teamid'], right_on = ['date','teamid'])
    tmp = pd.merge(tmp, gspd_dynamic, how='left', left_on=['date','teamid'], right_on = ['date','teamid'])
    tmp['dynamic_gspd'] = tmp['gspd_y'] / tmp['total_games'] * 100

    tmp.fillna(value=0, inplace=True)
    dynamic_gspd_2022 = tmp

    # 2023
    tmp = df_2023[['date', 'teamid', 'gameid', 'gspd']].reset_index().set_index(['teamid', 'date']).sort_index()
    games_played_dynamic = pd.DataFrame()

    # Need to adapt, so that the information is as before the game
    games_played_dynamic['total_games'] = tmp.groupby('teamid')['gspd'].cumcount()
    games_played_dynamic['dynamic_weighting'] = np.clip(0, games_played_dynamic['total_games']/n_games, 1) # dynamic weighting factor
    gspd_dynamic = pd.DataFrame(tmp.groupby('teamid')['gspd'].shift()).groupby('teamid')['gspd'].cumsum()

    tmp = pd.merge(tmp, games_played_dynamic,  how='left', left_on=['date','teamid'], right_on = ['date','teamid'])
    tmp = pd.merge(tmp, gspd_dynamic, how='left', left_on=['date','teamid'], right_on = ['date','teamid'])
    tmp['dynamic_gspd'] = tmp['gspd_y'] / tmp['total_games'] * 100

    tmp.fillna(value=0, inplace=True)
    dynamic_gspd_2023 = tmp

    gspd_2022 = pd.merge(dynamic_gspd_2022, historical_gspd_2022, how='left', left_on='teamid', right_on='teamid').reset_index()
    gspd_2022['mixed_gspd'] = gspd_2022['dynamic_gspd'] * gspd_2022['dynamic_weighting'] + gspd_2022['gspd'] * (1 - gspd_2022['dynamic_weighting'])

    gspd_2023 = pd.merge(dynamic_gspd_2023, historical_gspd_2023, how='left', left_on='teamid', right_on='teamid').reset_index()
    gspd_2023['mixed_gspd'] = gspd_2023['dynamic_gspd'] * gspd_2022['dynamic_weighting'] + gspd_2023['gspd'] * (1 - gspd_2022['dynamic_weighting'])

    gspd = pd.concat([gspd_2022, gspd_2023], ignore_index=True).set_index(['gameid_x', 'teamid'])['mixed_gspd']

    gspd.replace([np.inf, -np.inf], np.nan, inplace=True)
    gspd = gspd.fillna(method='bfill')

    return gspd
