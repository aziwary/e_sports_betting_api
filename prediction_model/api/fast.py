import pandas as pd

from prediction_model.main import preprocess
from prediction_model.main import features
from prediction_model.main import train
from prediction_model.main import user_entry

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Optional, good practice for dev purposes. Allow all middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

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
    Make a single course prediction.
    Assumes `pickup_datetime` is provided as string by the user in "%Y-%m-%d %H:%M:%S" format
    Assumes `pickup_datetime` implicitely refers to "US/Eastern" timezone (as any user in New York City would naturally write)
    """
    df_2021, df_2022, df_2023, champions_wr = preprocess()

    user_df = user_entry(league, team_1, team_2, champ_1, champ_2, champ_3,
               champ_4, champ_5, champ_6, champ_7, champ_8, champ_9, champ_10)

    updated_df_2023 = pd.concat([df_2023, user_df])

    data = features(df_2021, df_2022, updated_df_2023, champions_wr)

    train_data = data.iloc[:-1]
    predict_data = pd.DataFrame(data.iloc[-1][['wr_diff', 'streak_diff', 'gspd_diff', 'chmp_wr_diff']]).transpose()
    model = train(train_data)

    y_pred = model.predict(predict_data)

    # ⚠️ fastapi only accepts simple python data types as a return value
    # among which dict, list, str, int, float, bool
    # in order to be able to convert the api response to json
    return dict(expected_result=int(y_pred))
    # $CHA_END

@app.get("/")
def root():
    # $CHA_BEGIN
    return dict(greeting="Hello")
    # $CHA_END
