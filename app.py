
import streamlit as st
import numpy as np
import pandas as pd
import requests
from PIL import Image
from io import BytesIO


st.markdown("<h1 style='text-align: center; color: white;'>League of Legends E-Sports Prediction Model</h1>", unsafe_allow_html=True)
# Create a dropdown menu for selecting the league
invest = st.number_input('Amount of money invested')
league = st.selectbox("Select the league", ["LEC", "LCS", "PCS", "CBLOL", "TCL", "LLA", "LJL"])
col1, col2 = st.columns(2)
col3, col4, col5 = st.columns(3)
col6, col7, col8 =st.columns(3)

teams = {
    "LEC": ["Astralis","Excel Esports","Fnatic","G2 Esports","KOI","SK Gaming","MAD Lions", "Team BDS","Team Heretics","Team Vitality"],
    "LCS": ["100 Thieves","Cloud0","Dignitas","Evil Geniuses","FlyQuest","Golden Guardians","Immortals","Team Liquid","TSM"],
    "PCS": ["Beyond Gaming","Chiefs Esports Club","CTBC Flying Oyster","Deep Cross Gaming","Dewish Team","Frank Esports","HELL PIGS","Impunity","J Team","PSG Talon","SEM9 WPE","Team Bliss"],
    "CBLOL": ["FURIA", "Fluxo", "INTZ", "KaBuM! Esports", "Liberty", "Los Grandes", "Loud", "PaiN Gaming", "RED Canids", "Vivo Keyd Stars"],
    "TCL": ["5 Ronin","Ä°stanbul Wildcats","BeÅŸiktaÅŸ Esports","Dark Passage","FUT Esports","Galakticos","NASR eSports Turkey","Papara SuperMassive"],
    "LLA": ["All Knights","Estral Esports","INFINITY","Isurus","Movistar R7","Six Karma","Team Aze","The Kings"],
    "LJL": ["DetonatioN FocusMe","Sengoku Gaming","AXIZ","Burning Core","Crest Gaming Act","FENNEL", "Fukuoka SoftBank HAWKS gaming","V3 Esports"]
}

blue_team = col3.selectbox("Blue team", teams[league])
red_team = col5.selectbox("Red team", teams[league])

champions = ['Aatrox', 'Ahri', 'Akali', 'Akshan', 'Alistar', 'Amumu', 'Anivia', 'Annie', 'Aphelios', 'Ashe',
             'Aurelion Sol', 'Azir', 'Bard', "Bel'Veth", 'Blitzcrank', 'Brand', 'Braum', 'Caitlyn', 'Camille',
             'Cassiopeia', "Cho'Gath", 'Corki', 'Darius', 'Diana', 'Dr. Mundo', 'Draven', 'Ekko', 'Elise', 'Evelynn',
             'Ezreal', 'Fiddlesticks', 'Fiora', 'Fizz', 'Galio', 'Gangplank', 'Garen', 'Gnar', 'Gragas', 'Graves', 'Gwen',
             'Hecarim', 'Heimerdinger', 'Illaoi', 'Irelia', 'Ivern', 'Janna', 'Jarvan IV', 'Jax', 'Jayce', 'Jhin', 'Jinx',
             "K'Sante", "Kai'Sa", 'Kalista', 'Karma', 'Karthus', 'Kassadin', 'Katarina', 'Kayle', 'Kayn', 'Kennen', "Kha'Zix",
             'Kindred', 'Kled', "Kog'Maw", 'LeBlanc', 'Lee Sin', 'Leona', 'Lillia', 'Lissandra', 'Lucian', 'Lulu', 'Lux', 'Malphite',
             'Malzahar', 'Maokai', 'Master Yi', 'Milio', 'Miss Fortune', 'Mordekaiser', 'Morgana', 'Nami', 'Nasus', 'Nautilus', 'Neeko',
             'Nidalee', 'Nilah', 'Nocturne', 'Nunu', 'Olaf', 'Orianna', 'Ornn', 'Pantheon', 'Poppy', 'Pyke', 'Qiyana', 'Quinn', 'Rakan',
             'Rammus', "Rek'Sai", 'Rell', 'Renata Glasc', 'Renekton', 'Rengar', 'Riven', 'Rumble', 'Ryze', 'Samira', 'Sejuani', 'Senna',
             'Seraphine', 'Sett', 'Shaco', 'Shen', 'Shyvana', 'Singed', 'Sion', 'Sivir', 'Skarner', 'Sona', 'Soraka', 'Swain', 'Sylas',
             'Syndra', 'Tahm Kench', 'Taliyah', 'Talon', 'Taric', 'Teemo', 'Thresh', 'Tristana', 'Trundle', 'Tryndamere', 'Twisted Fate',
             'Twitch', 'Udyr', 'Urgot', 'Varus', 'Vayne', 'Veigar', "Vel'Koz", 'Vex', 'Vi', 'Viego', 'Viktor', 'Vladimir', 'Volibear', 'Warwick',
             'Wukong', 'Xayah', 'Xerath', 'Xin Zhao', 'Yasuo', 'Yone', 'Yorick', 'Yuumi', 'Zac', 'Zed', 'Zeri', 'Ziggs', 'Zilean', 'Zoe', 'Zyra']

# Create input fields for the five champions for each team
blue_champs = []
red_champs = []

for i in range(5):
    blue_champs.append(col3.selectbox(f"Blue team champion {i+1}", champions))
    red_champs.append(col5.selectbox(f"Red team champion {i+1}", champions))

bookmaker_blue = col3.number_input('Bookmaker odds for blue side', min_value=0.01)
bookmaker_red = col5.number_input('Bookmaker odds for red side', min_value=0.01)

bookmaker_blue_prob = 1 / bookmaker_blue
bookmaker_red_prob = 1 / bookmaker_red

# Add a button to submit the form
if col7.button("Estimate winning probabilities and implied odds"):
    import time

    progress = col7.empty()
    bar = col7.progress(0)

    for i in range(100):
        progress.text(f"Matchup assessment {i+1}%")
        bar.progress(i+1)
        time.sleep(0.08)

    url = "https://e-sports-final-cm5wuo7s2a-uc.a.run.app/predict"
    params = dict(
        league=league,
        team_1=blue_team,
        team_2=red_team,
        champ_1=blue_champs[0],
        champ_2=blue_champs[1],
        champ_3=blue_champs[2],
        champ_4=blue_champs[3],
        champ_5=blue_champs[4],
        champ_6=red_champs[0],
        champ_7=red_champs[1],
        champ_8=red_champs[2],
        champ_9=red_champs[3],
        champ_10=red_champs[4]
    )
    response = requests.get(url, params=params)
    prediction = response.json()
    prob_red_team = round(prediction["prob_blue_losing"] * 100, 2)
    prob_blue_team = round(prediction["prob_blue_winning"] * 100, 2)
    odd_red_team = round(prediction["odd_blue_losing"],2)
    odd_blue_team = round(prediction["odd_red_losing"],2)
    expected_value = round(bookmaker_blue * invest * prob_blue_team/100 - bookmaker_red * invest * prob_red_team/100 - invest, 2)

    if expected_value > 0:
        color = "green"
    else:
        color = "red"

    st.markdown(f"<h2 style='text-align: center; color: white;'>{blue_team} will win with a probability of {prob_blue_team}%, representing implied odds of {odd_blue_team}.</h2>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='text-align: center; color: {color};'>$ The expected profit of the bet is {expected_value} $</h2>", unsafe_allow_html=True)
else:
    col7.write("Analysis not started")



#champion_imgs = {}
#for champion in champions:
#    champion_imgs[champion] = f'https://ddragon.leagueoflegends.com/cdn/11.23.1/img/champion/{champion}.png'


#num_cols = 6
#col_width = int(12/num_cols)

#cols = [st.columns(num_cols) for _ in range(int(len(champion_imgs)/num_cols)+1)]
#for i, row in enumerate(cols):
#    for j, col in enumerate(row):
#        idx = i*num_cols+j
#        if idx < len(champion_imgs):
#            champion = list(champion_imgs.keys())[idx]
#            img_url = champion_imgs[champion]
#            response = requests.get(img_url)
#            img_data = response.content
#            img = Image.open(BytesIO(img_data))
#            img = img.resize((100, 100))
#            col.image(img, caption=champion, width=100)
