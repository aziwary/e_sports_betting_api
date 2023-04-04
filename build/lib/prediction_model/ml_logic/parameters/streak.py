import pandas as pd

def check_form(a, b, c):
    if a > b and b > c:
        return 1
    return 0

def get_streak(df_2022, df_2023):
    """
    Get the streak parameter, indicating whether a team won their last 3 games
    """
    # 2022
    tmp = df_2022[['date', 'teamid', 'gameid', 'result']].reset_index().set_index(['teamid', 'date']).sort_index()
    games_won_dynamic = pd.DataFrame(tmp.groupby('teamid')['result'].shift()).groupby('teamid')['result'].cumsum()

    tmp = pd.merge(tmp, games_won_dynamic, how='left', left_on=['date','teamid'], right_on = ['date','teamid'])

    counter_1 = -2
    counter_2 = -1
    output = []

    tmp['tmp'] = tmp['result_y']
    tmp['tmp'] = tmp['tmp'].fillna(value=0)

    for i in range(len(tmp['tmp'])):
        if i < 1:
            output.append(0)
        else:
            output.append(check_form(tmp['tmp'][i], tmp['tmp'][counter_2], tmp['tmp'][counter_1]))
            counter_1 += 1
            counter_2 += 1

    tmp['streak'] = output

    streak_2022 = tmp.reset_index()

    # 2023
    tmp = df_2023[['date', 'teamid', 'gameid', 'result']].reset_index().set_index(['teamid', 'date']).sort_index()
    games_won_dynamic = pd.DataFrame(tmp.groupby('teamid')['result'].shift()).groupby('teamid')['result'].cumsum()

    tmp = pd.merge(tmp, games_won_dynamic, how='left', left_on=['date','teamid'], right_on = ['date','teamid'])

    counter_1 = -1
    counter_2 = 0
    output = []

    tmp['tmp'] = tmp['result_y']
    tmp['tmp'] = tmp['tmp'].fillna(value=0)

    for i in range(len(tmp['tmp'])):
        if i < 1:
            output.append(0)
        else:
            output.append(check_form(tmp['tmp'][i], tmp['tmp'][counter_2], tmp['tmp'][counter_1]))
            counter_1 += 1
            counter_2 += 1

    tmp['streak'] = output

    streak_2023 = tmp.reset_index()

    streak = pd.concat([streak_2022, streak_2023], ignore_index=True).set_index(['gameid', 'teamid'])['streak']

    return streak
