import pandas as pd


def winningteam(match):
    winning_team = match[match['MatchNumber'] == 'Final'][[
        'Year', 'WinningTeam', 'Player_of_Match', 'City']].reset_index().drop(['index'], axis=1)

    return winning_team


def mostwinner(winning_team):

    most_winner = winning_team.groupby('WinningTeam').agg(lambda x: list(x))
    most_winner = most_winner.reset_index()
    most_winner['Total Wins'] = most_winner['Year'].apply(lambda x: len(x))
    most_winner = most_winner.sort_values(by=['Total Wins'], ascending=False)[
        ['WinningTeam', 'Year', 'Total Wins']].reset_index().drop(['index'], axis=1)

    return most_winner


def bar_data(df):
    df = df.set_index('WinningTeam')
    df = df['Total Wins']
    df = df.sort_values(ascending=False)
    return df


def player_list(df):

    df = df.drop(['Unnamed: 0'], axis=1)
    df = df['0'].tolist()
    return df


def total_run(player, balls):
    total_run = balls[balls['batter'] == player]['batsman_run'].sum()
    return total_run


def total_match(match):
    player_list1 = match['Team1Players'].tolist()
    ipl_player_list1 = []
    for i in range(len(player_list1)):
        player_list1[i] = player_list1[i].replace(
            '[', '').replace(']', '').replace("'", '').split(',')

    for i in player_list1:
        for j in range(len(i)):
            i[j] = i[j].strip()
    d = {}
    for i in player_list1:
        for j in i:
            if j in d:
                d[j] = d[j]+1
            else:
                d[j] = 1

    player_list2 = match['Team2Players'].tolist()
    ipl_player_list2 = []
    for i in range(len(player_list2)):
        player_list2[i] = player_list2[i].replace(
            '[', '').replace(']', '').replace("'", '').split(',')

    for i in player_list2:
        for j in range(len(i)):
            i[j] = i[j].strip()

    for i in player_list2:
        for j in i:
            if j in d:
                d[j] = d[j]+1
            else:
                d[j] = 1
    return d


def total_wicket(balls, player):
    total_wicket = balls[(balls['bowler'] == player) & ((balls['kind'] == 'caught') | (balls['kind'] == 'bowled') | (balls['kind'] == 'stumped') |
                                                        (balls['kind'] == 'lbw') | (balls['kind'] == 'caught and bowled'))].shape[0]
    return total_wicket


def total_player_six(balls, player):
    total_six = balls[(balls['batter'] == player) &
                    (balls['batsman_run'] == 6)].shape[0]
    return total_six


def total_player_four(balls, player):
    total_four = balls[(balls['batter'] == player) & (
        balls['batsman_run'] == 4) & (balls['non_boundary'] == 0)].shape[0]
    return total_four


def total_player_of_match(match, player):
    player_of_match = match[match['Player_of_Match'] == player].shape[0]
    return player_of_match


def scores(balls, lrun,hrun):
    g = balls.groupby(['ID', 'batter'])
    gr = g.sum('batsman_run')
    list_of_centuries = gr[(gr['batsman_run'] >= lrun) & (gr['batsman_run'] <= hrun)].index.tolist()
    d = {}
    for i in list_of_centuries:
        if i[1] in d:
            d[i[1]] = d[i[1]]+1
        else:
            d[i[1]] = 1
    return d


def runs_dataframe(player, match, balls):
    match_year = match[['ID', 'Year']]
    df = balls.copy()
    grp = df.set_index("ID").join(match_year.set_index("ID")).reset_index()
    grp_year = grp.groupby('Year')
    years = grp_year.first().index.tolist()
    lst1 = []
    lst2=[]
    for i in years:
        tempgrp = grp_year.get_group(i)
        lst1.append(int(tempgrp[tempgrp['batter'] ==
                        player].sum(numeric_only=True)[4]))
        lst2.append(tempgrp[tempgrp['batter']==player].drop_duplicates(subset='ID').count()[1])
    runs_per_year_d = {
        'Year': years,
        'Innings':lst2,
        'Runs': lst1,
    }
    runs_per_year = pd.DataFrame(runs_per_year_d)
    return runs_per_year


def wicket_dataframe(player, match, balls):
    match_year = match[['ID', 'Year']]
    df = balls.copy()
    grp = df.set_index("ID").join(match_year.set_index("ID")).reset_index()
    grp_year = grp.groupby('Year')
    years = grp_year.first().index.tolist()
    lst = []
    for i in years:
        tempgrp = grp_year.get_group(i)
        lst.append(int(tempgrp[(tempgrp['bowler'] == player) & ((tempgrp['kind'] == 'caught') | (tempgrp['kind'] == 'bowled') | (tempgrp['kind'] == 'stumped') |
                                                (tempgrp['kind'] == 'lbw') | (tempgrp['kind'] == 'caught and bowled'))].sum(numeric_only=True)[8]))
    wicket_per_year_d = {
        'Year': years,

        'Wickets': lst
    }
    wicket_per_year = pd.DataFrame(wicket_per_year_d)
    return wicket_per_year

def year_highest_score_dict(flag,year_match_d,grp_id_year,year_list):
    
    dic={}
    for i in year_list:
        d={}
        for j in year_match_d[i]:
            
            player_grp=grp_id_year.get_group((i,j))[['batter','batsman_run']].groupby('batter')
            player_grp_match=player_grp.sum().reset_index()
            player_grp_match_lst=player_grp_match.values.tolist()
            if flag=='s':
                for k in player_grp_match_lst:
                    if k[0] in d:
                        d[k[0]]=max(d[k[0]],k[1])
                    else:
                        d[k[0]]=k[1]
            elif flag=='c':
                for k in player_grp_match_lst:
                    if k[0] in d:
                        if k[1]>99:
                            d[k[0]]=d[k[0]]+1
                    else:
                        if k[1]>99:
                            d[k[0]]=1
            elif flag=='f':
                for k in player_grp_match_lst:
                    if k[0] in d:
                        if k[1]>49 and k[1]<100:
                            d[k[0]]=d[k[0]]+1
                    else:
                        if k[1]>49 and k[1]<100:
                            d[k[0]]=1
                    
        dic[i]=d
    return dic

def player_data_dataframe(year_highest_score,year_highest_century,year_highest_fifty,year_list,player):

    lst1=[]
    lst2=[]
    lst3=[]

    for i in year_list:
        lst1.append(year_highest_score[i].get(player) if year_highest_score[i].get(player) else 0)
        lst2.append(year_highest_century[i].get(player) if year_highest_century[i].get(player) else 0)
        lst3.append(year_highest_fifty[i].get(player) if year_highest_fifty[i].get(player) else 0)

    dictt={
        'Year':year_list,
        'No. of Centuries':lst2,
        'No. of Fifties':lst3,
        'Highest Score': lst1


    }
    player_data=pd.DataFrame(dictt).sort_values('Year',ascending=False).reset_index().drop('index',axis=1)
    return player_data


