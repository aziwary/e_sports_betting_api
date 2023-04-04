import pandas as pd
import numpy as np

def get_winrates(df_2021, df_2022, df_2023, weighting_n):
    """
    Get winrates
    """
    ### Historical WR
    # Group the DataFrame by team_id and count the number of games played
    games_played_2022 = df_2022.groupby('teamid')['result'].count()
    games_played_2021 = df_2021.groupby('teamid')['result'].count()

    # Group the DataFrame by team_id and count the number of wins
    wins_2022 = df_2022.groupby('teamid')['result'].sum()
    wins_2021 = df_2021.groupby('teamid')['result'].sum()

    # Calculate the win rate for each team
    win_rates_in_2022 = (wins_2022 / games_played_2022) * 100
    win_rates_in_2021 = (wins_2021 / games_played_2021) * 100

    tmp_1 = pd.DataFrame(df_2022.groupby('teamid').count().iloc[:, 0])
    tmp_2 = pd.DataFrame(df_2023.groupby('teamid').count().iloc[:, 0])

    historical_wr_2022 = pd.merge(tmp_1, win_rates_in_2021, how='left', left_index=True, right_index=True)
    historical_wr_2023 = pd.merge(tmp_2, win_rates_in_2022, how='left', left_index=True, right_index=True)

    historical_wr_2022.fillna(value=historical_wr_2022['result'].mean(), inplace=True)
    historical_wr_2023.fillna(value=historical_wr_2023['result'].mean(), inplace=True)

    n_games = weighting_n

    ### Dynamic WR
    # 2022
    tmp = df_2022[['date', 'teamid', 'gameid', 'result']].reset_index().set_index(['teamid', 'date']).sort_index()
    games_played_dynamic = pd.DataFrame()

    # Need to adapt, so that the information is as before the game
    games_played_dynamic['total_games'] = tmp.groupby('teamid')['result'].cumcount()
    games_played_dynamic['dynamic_weighting'] = np.clip(0, games_played_dynamic['total_games']/n_games, 1) # dynamic weighting factor
    games_won_dynamic = pd.DataFrame(tmp.groupby('teamid')['result'].shift()).groupby('teamid')['result'].cumsum()

    tmp = pd.merge(tmp, games_played_dynamic,  how='left', left_on=['date','teamid'], right_on = ['date','teamid'])
    tmp = pd.merge(tmp, games_won_dynamic, how='left', left_on=['date','teamid'], right_on = ['date','teamid'])
    tmp['dynamic_wr'] = tmp['result_y'] / tmp['total_games'] * 100

    # If no data available (new teams) replace with average of 50%
    tmp['dynamic_wr'] = tmp['dynamic_wr'].replace([np.inf, -np.inf], np.nan)
    tmp['dynamic_wr'] = tmp['dynamic_wr'].fillna(value=50)

    dynamic_wr_2022 = tmp

    # 2023
    tmp = df_2023[['date', 'teamid', 'gameid', 'result']].reset_index().set_index(['teamid', 'date']).sort_index()
    games_played_dynamic = pd.DataFrame()

    # Need to adapt, so that the information is as before the game
    games_played_dynamic['total_games'] = tmp.groupby('teamid')['result'].cumcount()
    games_played_dynamic['dynamic_weighting'] = np.clip(0, games_played_dynamic['total_games']/n_games, 1) # dynamic weighting factor
    games_won_dynamic = pd.DataFrame(tmp.groupby('teamid')['result'].shift()).groupby('teamid')['result'].cumsum()

    tmp = pd.merge(tmp, games_played_dynamic,  how='left', left_on=['date','teamid'], right_on = ['date','teamid'])
    tmp = pd.merge(tmp, games_won_dynamic, how='left', left_on=['date','teamid'], right_on = ['date','teamid'])
    tmp['dynamic_wr'] = tmp['result_y'] / tmp['total_games'] * 100

    # If no data available (new teams) replace with average of 50%
    tmp['dynamic_wr'] = tmp['dynamic_wr'].replace([np.inf, -np.inf], np.nan)
    tmp['dynamic_wr'] = tmp['dynamic_wr'].fillna(value=50)

    dynamic_wr_2023 = tmp

    wr_2022 = pd.merge(dynamic_wr_2022, historical_wr_2022, how='left', left_on='teamid', right_on='teamid').reset_index()
    wr_2022['mixed_wr'] = wr_2022['dynamic_wr'] * wr_2022['dynamic_weighting'] + wr_2022['result'] * (1 - wr_2022['dynamic_weighting'])


    wr_2023 = pd.merge(dynamic_wr_2023, historical_wr_2023, how='left', left_on='teamid', right_on='teamid').reset_index()
    wr_2023['mixed_wr'] = wr_2023['dynamic_wr'] * wr_2022['dynamic_weighting'] + wr_2023['result'] * (1 - wr_2022['dynamic_weighting'])

    wr = pd.concat([wr_2022, wr_2023], ignore_index=True).set_index(['gameid_x', 'teamid'])['mixed_wr']

    return wr
