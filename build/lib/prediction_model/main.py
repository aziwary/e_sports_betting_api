import pandas as pd
import time
import warnings

warnings.filterwarnings("ignore")

league_list = ["LEC", "LCS", "PCS", "CBLOL", "TCL", "LLA", "LJL", "UL", "LCK"]

def preprocess():
    """
    Preprocess the raw data
    """
    import ipdb; ipdb.set_trace()
    from ml_logic.filter_leagues import filter_league

    raw_df_2021 = pd.read_csv('data/2021_LoL_esports_Data.csv', parse_dates=['date'])
    raw_df_2022 = pd.read_csv('data/2022_LoL_esports_Data.csv', parse_dates=['date'])
    raw_df_2023 = pd.read_csv('data/2023_LoL_esports_Data.csv', parse_dates=['date'])

    champ_wr = pd.read_csv('data/all_patches_final.csv')

    final_df = champ_wr

    final_df["Win%"] = final_df["Win %"].str.rstrip('%')

    final_df["Win%"] = pd.to_numeric(final_df["Win%"])

    grouped_df = final_df.groupby(["patch", "Name"])["Win%"].max().reset_index()

    champions_wr_overview = grouped_df

    output = []

    for i in champions_wr_overview["Name"]:
        text = i
        output.append(text[:len(text)//2])

    champions_wr_overview["name_clean"] = output
    champions_wr_overview = champions_wr_overview.drop("Name", axis=1)

    filtered_df_2021 = filter_league(raw_df_2021, league_list)[['gameid', 'league', 'date', 'patch', 'participantid', 'side', 'position', 'playerid', 'teamname', 'teamid', 'champion', 'result', 'gspd']]
    filtered_df_2022 = filter_league(raw_df_2022, league_list)[['gameid', 'league', 'date', 'patch', 'participantid', 'side', 'position', 'playerid', 'teamname', 'teamid', 'champion', 'result', 'gspd']]
    filtered_df_2023 = filter_league(raw_df_2023, league_list)[['gameid', 'league', 'date', 'patch', 'participantid', 'side', 'position', 'playerid', 'teamname', 'teamid', 'champion', 'result', 'gspd']]

    return filtered_df_2021, filtered_df_2022, filtered_df_2023, champions_wr_overview


def features(df_2021, df_2022, df_2023_updated, champions_wr_overview):
    """
    Create the actual features
    """
    from ml_logic.parameters.winrate import get_winrates
    from ml_logic.parameters.gspd import get_gspd
    from ml_logic.parameters.streak import get_streak
    from ml_logic.parameters.chmp_wr import get_chmp_wr

    filtered_df_2021 = df_2021
    filtered_df_2022 = df_2022
    filtered_df_2023 = df_2023_updated

    full_data = pd.concat([filtered_df_2022, filtered_df_2023])

    filtered_df_2021 = filtered_df_2021.loc[filtered_df_2021['position'].isin(["team"])]
    filtered_df_2022 = filtered_df_2022.loc[filtered_df_2022['position'].isin(["team"])]
    filtered_df_2023 = filtered_df_2023.loc[filtered_df_2023['position'].isin(["team"])]

    patch_information = full_data.loc[full_data['participantid'].isin([1])].set_index('gameid')['patch']
    champion_1 = full_data.loc[full_data['participantid'].isin([1])].set_index('gameid')['champion']
    champion_2 = full_data.loc[full_data['participantid'].isin([2])].set_index('gameid')['champion']
    champion_3 = full_data.loc[full_data['participantid'].isin([3])].set_index('gameid')['champion']
    champion_4 = full_data.loc[full_data['participantid'].isin([4])].set_index('gameid')['champion']
    champion_5 = full_data.loc[full_data['participantid'].isin([5])].set_index('gameid')['champion']
    champion_6 = full_data.loc[full_data['participantid'].isin([6])].set_index('gameid')['champion']
    champion_7 = full_data.loc[full_data['participantid'].isin([7])].set_index('gameid')['champion']
    champion_8 = full_data.loc[full_data['participantid'].isin([8])].set_index('gameid')['champion']
    champion_9 = full_data.loc[full_data['participantid'].isin([9])].set_index('gameid')['champion']
    champion_10 = full_data.loc[full_data['participantid'].isin([10])].set_index('gameid')['champion']

    champions_list = [patch_information,champion_1,
                champion_2,
                champion_3,
                champion_4,
                champion_5,
                champion_6,
                champion_7,
                champion_8,
                champion_9,
                champion_10]

    for i, series in enumerate(champions_list):
        if i == 0:
            champions = pd.DataFrame(series)
            champions.columns = ["patch"]
        else:
            champions[f"player_{i}"] = series

    champions = champions.dropna(axis=0)
    champions = champions.replace(['Nunu & Willump'], 'Eskimo')

    winrate_pm = get_winrates(filtered_df_2021, filtered_df_2022, filtered_df_2023, 7)
    gspd_pm = get_gspd(filtered_df_2021, filtered_df_2022, filtered_df_2023, 7)
    streak_pm = get_streak(filtered_df_2022, filtered_df_2023)
    chmp_wr_pm = get_chmp_wr(champions, champions_wr_overview)

    only_blue_2022 = filtered_df_2022.loc[filtered_df_2022['side'].isin(["Blue"])].set_index('gameid')
    only_red_2022 = filtered_df_2022.loc[filtered_df_2022['side'].isin(["Red"])].set_index('gameid')

    only_blue_2023 = filtered_df_2023.loc[filtered_df_2023['side'].isin(["Blue"])].set_index('gameid')
    only_red_2023 = filtered_df_2023.loc[filtered_df_2023['side'].isin(["Red"])].set_index('gameid')

    blue_vs_red_2022 = pd.merge(only_blue_2022['teamid'], only_red_2022['teamid'], how='left', left_index=True, right_index=True)
    blue_vs_red_2023 = pd.merge(only_blue_2023['teamid'], only_red_2023['teamid'], how='left', left_index=True, right_index=True)

    blue_vs_red = pd.concat([blue_vs_red_2022, blue_vs_red_2023]).reset_index()
    blue_results = pd.concat([only_blue_2022[['result']], only_blue_2023[['result']]]).reset_index()

    blue_vs_red = blue_vs_red.dropna(axis=0)

    # Merge the blue side data (controlled by 'teamid_x' on the left side)
    model_df = pd.merge(blue_vs_red, winrate_pm, left_on=['gameid', 'teamid_x'], right_on=['gameid_x', 'teamid'], how="left") # wr blue side
    model_df = pd.merge(model_df, streak_pm, left_on=['gameid', 'teamid_x'], right_on=['gameid', 'teamid'], how="left") # streak blue side
    model_df = pd.merge(model_df, gspd_pm, left_on=['gameid', 'teamid_x'], right_on=['gameid_x', 'teamid'], how="left") # gspd blue side

    # Merge the red side data (controlled by 'teamid_y' on the left side)
    model_df = pd.merge(model_df, winrate_pm, left_on=['gameid', 'teamid_y'], right_on=['gameid_x', 'teamid']) # wr red side
    model_df = pd.merge(model_df, streak_pm, left_on=['gameid', 'teamid_y'], right_on=['gameid', 'teamid']) # streak red side
    model_df = pd.merge(model_df, gspd_pm, left_on=['gameid', 'teamid_y'], right_on=['gameid_x', 'teamid']) # gspd red side

    # Merge the results from blue perspective
    model_df = pd.merge(model_df, blue_results, left_on=['gameid'], right_on=['gameid'])

    # Calculate differences
    model_df['wr_diff'] = model_df['mixed_wr_x'] - model_df['mixed_wr_y']
    model_df['streak_diff'] = model_df['streak_x'] - model_df['streak_y']
    model_df['gspd_diff'] = model_df['mixed_gspd_x'] - model_df['mixed_gspd_y']

    # Merge the champion wr difference
    model_df = pd.merge(model_df, chmp_wr_pm, left_on='gameid', right_on='gameid')

    # Drop unnecessary columns
    model_df = model_df.drop(['teamid_x', 'teamid_y', 'mixed_wr_x', 'streak_x', 'mixed_gspd_x', 'mixed_wr_y', 'streak_y', 'mixed_gspd_y'], axis=1)
    model_df = model_df.set_index('gameid')

    return model_df

def train_test_split(data, percent_of_train_data = 0.95):
    train_data = data[0:(int(len(data)*percent_of_train_data))]
    test_data = data[(int(len(data)*percent_of_train_data)):]

    return train_data, test_data

def train(data):
    """
    Train model on data
    """
    from sklearn.linear_model import LogisticRegression

    X = data[['wr_diff', 'streak_diff', 'gspd_diff', 'chmp_wr_diff']]
    y = data['result']

    model = LogisticRegression()
    model.fit(X, y)

    return model

def user_entry(league, team_1, team_2, champ_1, champ_2, champ_3,
               champ_4, champ_5, champ_6, champ_7, champ_8, champ_9, champ_10):
    """
    Format user input
    """

    game_id = 'new_game'

    patch = 13.05

    date = pd.to_datetime(time.time(), unit="s")

    data = [[game_id, date, patch, 1, 'Blue', 'player', league, champ_1, team_1, 0],
        [game_id, date, patch, 2, 'Blue', 'player', league, champ_2, team_1, 0],
        [game_id, date, patch, 3, 'Blue', 'player', league, champ_3, team_1, 0],
        [game_id, date, patch, 4, 'Blue', 'player', league, champ_4, team_1, 0],
        [game_id, date, patch, 5, 'Blue', 'player', league, champ_5, team_1, 0],
        [game_id, date, patch, 6, 'Red', 'player', league, champ_6, team_2, 0],
        [game_id, date, patch, 7, 'Red', 'player', league, champ_7, team_2, 0],
        [game_id, date, patch, 8, 'Red', 'player', league, champ_8, team_2, 0],
        [game_id, date, patch, 9, 'Red', 'player', league, champ_9, team_2, 0],
        [game_id, date, patch, 10, 'Red', 'player', league, champ_10, team_2, 0],
        [game_id, date, patch, 0, 'Blue', 'team', league, 'na', team_1, 0],
        [game_id, date, patch, 0, 'Red', 'team', league, 'na', team_2, 0]]

    user_df = pd.DataFrame(data, columns=['gameid', 'date', 'patch', 'participantid', 'side', 'position', 'league', 'champion', 'teamid', 'result'])

    return user_df

if __name__ == '__main__':

    df_2021, df_2022, df_2023, champions_wr = preprocess()

    user_df = user_entry("LCS", "oe:team:2cb996a4b0ffaca3bcf66fe91450243", "oe:team:1c81857b6ce6a3c1cd9220fd97e077f",
               "Rumble", "Maokai", "K'Sante", "Tristana", "Amumu", "Rumble", "Maokai", "K'Sante", "Tristana", "Amumu")

    updated_df_2023 = pd.concat([df_2023, user_df])

    data = features(df_2021, df_2022, updated_df_2023, champions_wr)

    train_data = data.iloc[:-1]
    predict_data = pd.DataFrame(data.iloc[-1][['wr_diff', 'streak_diff', 'gspd_diff', 'chmp_wr_diff']]).transpose()
    model = train(train_data)

    #train_data, test_data = train_test_split(data)
    #model = train(train_data)
    #print(model.score(test_data[['wr_diff', 'streak_diff', 'gspd_diff', 'chmp_wr_diff']], test_data['result']))

    print(f"Odds of blue losing: {1 / model.predict_proba(predict_data)[0][0]} \n Odds of blue winning: {1 / model.predict_proba(predict_data)[0][1]}")
    #print(predict_data)
