import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from datetime import datetime as dt
import itertools

dataset_path = 'final_dataset.csv'
match_data = pd.read_csv(dataset_path)
colomns_req = ['Date', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'FTR']
playing_statistics_1 = match_data[colomns_req]

def get_goals_scored(playing_stat):
    teams = {}
    for i in playing_stat.groupby('Hometeam').mean().T.columns:
        teams[i]= []

    for i in range(len(playing_stat)):
        HTGS = playing_stat.iloc[i]['FTHG']
        ATGS = playing_stat.iloc[i]['FTAG']
        teams[playing_stat.iloc[i].HomeTeam].append(HTGS)
        teams[playing_stat.iloc[i].AwayTeam].append(ATGS)

    Goalscored = pd.DataFrame(data=teams, index=[i for i in range(1, 609)]).T
    Goalscored[0] = 0

    for i in range(2, 609):
        Goalscored[i] = Goalscored[i] + Goalscored[i-1]
    return Goalscored


def get_goals_conceded(playing_stat):
    teams = {}
    for i in playing_stat.groupby('HomeTeam').mean().T.columns:
        teams[i] = []


    for i in range(len(playing_stat)):
        ATGC = playing_stat.iloc[i]['FTHG'] 
        HTGC = playing_stat.iloc[i]['FTAG']
        teams[playing_stat.iloc[i].HomeTeam].append(HTGC) 
        teams[playing_stat.iloc[i].AwayTeam].append(ATGC) 

    GoalConceded = pd.DataFrame(data=teams, index= [i for i in range(1, 609)]).T
    GoalConceded[0] = 0

    for i in range(2, 609):
        GoalConceded[i] = GoalConceded[i] + GoalConceded[i-1]
    return GoalConceded

def get_gss(playing_stat):
    GC = get_goals_conceded(playing_stat)
    GS = get_goals_scored(playing_stat)

    j=0
    HTGS = []
    ATGS = []
    HTGC = []
    ATGC = []

    for i in range(380):
        ht = playing_stat.iloc[i].HomeTeam
        at = playing_stat.iloc[i].AwayTeam
        HTGS.append(GS.loc[ht][j])
        ATGS.append(GS.loc[at][j])
        HTGC.append(GS.loc[ht][j])
        ATGC.append(GS.loc[ht][j])

        if((i+1)%10) == 0:
            j = j + 1

    playing_stat['HTGS'] = HTGS
    playing_stat['ATGS'] = ATGS
    playing_stat['HTGC'] = HTGC
    playing_stat['ATGC'] = ATGC

    return playing_stat

playing_statistics_1 = get_gss(playing_statistics_1)