import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import helper

year_list=[2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022]

def preprocessor(match,balls,year_list):
    match_year=match[['ID','Year']]
    df=balls.copy()    
    grp=df.set_index("ID").join(match_year.set_index("ID")).reset_index()
    grp_id_year=grp.groupby(['Year','ID'])
    year_match_d={}
    for i in year_list:
        id_list_year=grp[grp['Year']==i]['ID'].unique().tolist()
        year_match_d[i]=id_list_year

    return year_match_d,grp_id_year


balls=pd.read_csv('Dataset//IPL_Ball_by_Ball_2008_2022.csv')
match=pd.read_csv('Dataset//IPL_Matches_2008_2022.csv')
player_list=pd.read_csv('Dataset//IPL_Player_List')
match['Year'] = pd.DatetimeIndex(match['Date']).year
match['City'].fillna('Dubai',inplace=True)

year_match_d,grp_id_year=preprocessor(match,balls,year_list)
year_highest_score=helper.year_highest_score_dict('s',year_match_d,grp_id_year,year_list)
year_highest_century=helper.year_highest_score_dict('c',year_match_d,grp_id_year,year_list)
year_highest_fifty=helper.year_highest_score_dict('f',year_match_d,grp_id_year,year_list)



st.set_page_config(
    page_title='IPL Analysis',
    page_icon=':mag:',
    
)

st.sidebar.title("IPL Analysis")
sidebar_button=st.sidebar.radio(
    'Select an option',
    ('Overall Analysis','Player-Wise Analysis')
)

if sidebar_button=='Overall Analysis':
    st.title("Overall Analysis of IPL")

    st.text('')
    st.text('')

    # colulmns

    total_matches=len(pd.unique(match['ID']))
    total_years=len(match['Year'].unique())
    start_year=min(match['Year'].unique())
    end_year=max(match['Year'].unique())
    total_teams=len(match['Team2'].unique())
    total_runs=balls['total_run'].sum()
    total_sixes=balls['batsman_run'][balls['batsman_run']==6].value_counts().tolist()[0]
    total_fours=balls['batsman_run'][balls['batsman_run']==4].value_counts().tolist()[0]

    col1,col2,col3=st.columns(3)

    with col1:
        col1_title='<strong style="font-family:sans-serif;font-size: 30px;">Total Years</strong>'
        col1_value=f'<p style="font-family:sans-serif;font-size: 25px;">{total_years} ({start_year}-{end_year})</p>'
        st.markdown(col1_title,unsafe_allow_html=True)
        st.markdown(col1_value,unsafe_allow_html=True)

    with col2:
        col2_title='<strong style="font-family:sans-serif;font-size: 30px;">Total Matches</strong>'
        col2_value=f'<p style="font-family:sans-serif;font-size: 25px;">{total_matches}</p>'
        st.markdown(col2_title,unsafe_allow_html=True)
        st.markdown(col2_value,unsafe_allow_html=True)

    with col3:
        col3_title='<strong style="font-family:sans-serif;font-size: 30px;">Total Teams</strong>'
        col3_value=f'<p style="font-family:sans-serif;font-size: 25px;">{total_teams}</p>'
        st.markdown(col3_title,unsafe_allow_html=True)
        st.markdown(col3_value,unsafe_allow_html=True)

    col4,col5,col6=st.columns(3)

    with col4:
        col4_title='<strong style="font-family:sans-serif;font-size: 30px;">Total Runs</strong>'
        col4_value=f'<p style="font-family:sans-serif;font-size: 25px;">{total_runs}</p>'
        st.markdown(col4_title,unsafe_allow_html=True)
        st.markdown(col4_value,unsafe_allow_html=True)
    with col5:
        col5_title='<strong style="font-family:sans-serif;font-size: 30px;">Total Sixes</strong>'
        col5_value=f'<p style="font-family:sans-serif;font-size: 25px;">{total_sixes}</p>'
        st.markdown(col5_title,unsafe_allow_html=True)
        st.markdown(col5_value,unsafe_allow_html=True)

    with col6:
        col6_title='<strong style="font-family:sans-serif;font-size: 30px;">Total Fours</strong>'
        col6_value=f'<p style="font-family:sans-serif;font-size: 25px;">{total_fours}</p>'
        st.markdown(col6_title,unsafe_allow_html=True)
        st.markdown(col6_value,unsafe_allow_html=True)
    
    st.text('')
    st.text('')

    # IPL Winners List from 2008 to 2022

    winning_teams_title='<strong style="font-family:sans-serif;font-size: 30px;">IPL Winners List from 2008 to 2022</strong>'
    st.markdown(winning_teams_title,unsafe_allow_html=True)

    winning_team=helper.winningteam(match)
    st.table(winning_team)

    st.text('')
    st.text('')
    
    # Most IPL Winner

    most_winner_title='<strong style="font-family:sans-serif;font-size: 30px;">Most IPL Winner</strong>'
    st.markdown(most_winner_title,unsafe_allow_html=True)

    most_winner=helper.mostwinner(winning_team)
    st.table(most_winner)

    most_winner=most_winner.sort_values(by='Total Wins')
    fig = px.bar(most_winner, x="Total Wins", y="WinningTeam", orientation='h',title="Most IPL Winner chart",width=1000,height=550)
    st.plotly_chart(fig)
    

if sidebar_button=='Player-Wise Analysis':
    
    
    total_player_list=helper.player_list(player_list)
    player=st.sidebar.selectbox('Select Player',total_player_list)

    st.title(f'Overall Analysis of "{player}"')
    st.text('')
    st.text('')

    total_match_player_played=helper.total_match(match)
    total_player_runs=helper.total_run(player,balls)
    total_player_wicket=helper.total_wicket(balls,player)
    total_player_six=helper.total_player_six(balls,player)
    total_player_four=helper.total_player_four(balls,player)
    total_player_of_match=helper.total_player_of_match(match,player)
    player_centuries_dict=helper.scores(balls,100,1000)
    total_player_centuries=player_centuries_dict[player] if player in player_centuries_dict else 0
    player_fifty_dict=helper.scores(balls,50,99)
    total_player_fifty=player_fifty_dict[player] if player in player_fifty_dict else 0
    player_thirty_dict=helper.scores(balls,30,1000)
    total_player_thirty=player_thirty_dict[player] if player in player_thirty_dict else 0

    col1,col2,col3=st.columns(3)

    with col1:
        col1_title='<strong style="font-family:sans-serif;font-size: 30px;">Total Match</strong>'
        col1_value=f'<p style="font-family:sans-serif;font-size: 25px;">{total_match_player_played[player]}</p>'
        st.markdown(col1_title,unsafe_allow_html=True)
        st.markdown(col1_value,unsafe_allow_html=True)
    with col2:
        col2_title='<strong style="font-family:sans-serif;font-size: 30px;">Total Runs</strong>'
        col2_value=f'<p style="font-family:sans-serif;font-size: 25px;">{total_player_runs}</p>'
        st.markdown(col2_title,unsafe_allow_html=True)
        st.markdown(col2_value,unsafe_allow_html=True)

    with col3:
        col3_title='<strong style="font-family:sans-serif;font-size: 30px;">Total Wickets</strong>'
        col3_value=f'<p style="font-family:sans-serif;font-size: 25px;">{total_player_wicket}</p>'
        st.markdown(col3_title,unsafe_allow_html=True)
        st.markdown(col3_value,unsafe_allow_html=True)

    col4,col5,col6=st.columns(3)

    with col4:
        col4_title='<strong style="font-family:sans-serif;font-size: 30px;">Total Sixes</strong>'
        col4_value=f'<p style="font-family:sans-serif;font-size: 25px;">{total_player_six}</p>'
        st.markdown(col4_title,unsafe_allow_html=True)
        st.markdown(col4_value,unsafe_allow_html=True)

    with col5:
        col5_title='<strong style="font-family:sans-serif;font-size: 30px;">Total Fours</strong>'
        col5_value=f'<p style="font-family:sans-serif;font-size: 25px;">{total_player_four}</p>'
        st.markdown(col5_title,unsafe_allow_html=True)
        st.markdown(col5_value,unsafe_allow_html=True)

    with col6:
        col6_title='<strong style="font-family:sans-serif;font-size: 30px;">Player Of Match</strong>'
        col6_value=f'<p style="font-family:sans-serif;font-size: 25px;">{total_player_of_match} Times</p>'
        st.markdown(col6_title,unsafe_allow_html=True)
        st.markdown(col6_value,unsafe_allow_html=True)

    col7,col8,col9=st.columns(3)

    with col7:
        col7_title='<strong style="font-family:sans-serif;font-size: 30px;">Centuries</strong>'
        col7_value=f'<p style="font-family:sans-serif;font-size: 25px;">{total_player_centuries} Times</p>'
        st.markdown(col7_title,unsafe_allow_html=True)
        st.markdown(col7_value,unsafe_allow_html=True)

    with col8:
        col8_title='<strong style="font-family:sans-serif;font-size: 30px;">Fifties</strong>'
        col8_value=f'<p style="font-family:sans-serif;font-size: 25px;">{total_player_fifty} Times</p>'
        st.markdown(col8_title,unsafe_allow_html=True)
        st.markdown(col8_value,unsafe_allow_html=True)

    with col9:
        col9_title='<strong style="font-family:sans-serif;font-size: 30px;">Total 30+</strong>'
        col9_value=f'<p style="font-family:sans-serif;font-size: 25px;">{total_player_thirty} Times</p>'
        st.markdown(col9_title,unsafe_allow_html=True)
        st.markdown(col9_value,unsafe_allow_html=True)

    st.text('')
    st.text('')

    
    # year_highest_score_player=year_highest_score[2008].get(player) if year_highest_score[2008].get(player) else 0
    # st.header(year_highest_score_player)
    runs_per_year=helper.runs_dataframe(player,match,balls)
    wicket_per_year=helper.wicket_dataframe(player,match,balls)
    
    st.header('Year-Wise Data')
    player_data_dataframe=helper.player_data_dataframe(year_highest_score,year_highest_century,year_highest_fifty,year_list,player)
    player_data_dataframe=runs_per_year.set_index('Year').join(player_data_dataframe.set_index('Year'))
    player_data_dataframe=player_data_dataframe.join(wicket_per_year.set_index('Year')).reset_index()
    st.table(player_data_dataframe)

    # st.header("Runs per Year")
    
    fig=px.bar(runs_per_year,x='Year',y='Runs',width=1000,height=450,title="Runs per Year")
    st.plotly_chart(fig)

    if total_player_centuries!=0:
        # st.header("Centuries per Year")
        
        fig=px.bar(player_data_dataframe,x='Year',y='No. of Centuries',width=1000,height=450,title="Centuries per Year")
        st.plotly_chart(fig)
    if total_player_fifty!=0:
        # st.header("Fifties per Year")
        
        fig=px.bar(player_data_dataframe,x='Year',y='No. of Fifties',width=1000,height=450,title="Fifties per Year")
        st.plotly_chart(fig)
    if total_player_wicket!=0:
        # st.header("Wickets per Year")
        
        fig=px.bar(wicket_per_year,x='Year',y='Wickets',width=1000,height=450,title="Wickets per Year")
        st.plotly_chart(fig)

    
    # st.table(player_data_dataframe)

    



    

    
