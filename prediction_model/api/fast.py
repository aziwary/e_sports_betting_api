import pandas as pd
import numpy as np

from prediction_model.main import preprocess
from prediction_model.main import features
from prediction_model.main import train
from prediction_model.main import user_entry

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from google.cloud import storage

app = FastAPI()
df_2021, df_2022, df_2023, champions_wr = preprocess()

storage_client = storage.Client(project='wagon-bootcamp-377018')
teamids = pd.read_csv('gs://esports_betting/2023_TeamIDs.csv')

# Optional, good practice for dev purposes. Allow all middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)
#http://127.0.0.1:8000/predict?league=LEC&team_1=Astralis&team_2=Fnatic&champ_1=Rumble&champ_2=Maokai&champ_3=Maokai&champ_4=Tristana&champ_5=Amumu&champ_6=Rumble&champ_7=Maokai&champ_8=Maokai&champ_9=Tristana&champ_10=Amumu
@app.get("/predict")
def predict(league: str,
            team_1: str,
            team_2: str,
            champ_1: str,
            champ_2: str,
            champ_3: str,
            champ_4: str,
            champ_5: str,
            champ_6: str,
            champ_7: str,
            champ_8: str,
            champ_9: str,
            champ_10: str):
    """
    Give out winning probabilities depending on the user input
    """

    team_1_id = teamids[teamids['teamname'] == team_1]['teamid'].to_list()[0]
    team_2_id = teamids[teamids['teamname'] == team_2]['teamid'].to_list()[0]

    user_df = user_entry(league, team_1_id, team_2_id, champ_1, champ_2, champ_3,
               champ_4, champ_5, champ_6, champ_7, champ_8, champ_9, champ_10)

    updated_df_2023 = pd.concat([df_2023, user_df])

    data = features(df_2021, df_2022, updated_df_2023, champions_wr)

    train_data = data.iloc[:-1]
    predict_data = pd.DataFrame(data.iloc[-1][['wr_diff', 'streak_diff', 'gspd_diff', 'chmp_wr_diff']]).transpose()
    model = train(train_data)

    y_prob = model.predict_proba(predict_data)

    # ⚠️ fastapi only accepts simple python data types as a return value
    # among which dict, list, str, int, float, bool
    # in order to be able to convert the api response to json
    return dict(prob_blue_losing=(y_prob[0][0]),
                prob_blue_winning=(y_prob[0][1]),
                odd_blue_losing=(1/y_prob[0][0]),
                odd_red_losing=(1/y_prob[0][1]))
    # $CHA_END

@app.get("/")
def root():
    # $CHA_BEGIN
    return dict(greeting="Hello")
    # $CHA_END
