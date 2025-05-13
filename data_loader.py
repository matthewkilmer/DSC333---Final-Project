# data_loader.py
from nba_api.stats.static import players
from nba_api.stats.endpoints import PlayerCareerStats
import pandas as pd
import os
from database import insert_predicted_stats

def get_player_id(player_name):
    player_dict = players.find_players_by_full_name(player_name)
    if player_dict:
        return player_dict[0]['id']
    else:
        raise ValueError("Player not found")

def get_last_5_season_avgs(player_id):
    career = PlayerCareerStats(player_id=player_id).get_data_frames()[0]
    career = career[career['LEAGUE_ID'] == '00']  # NBA only
    career = career.sort_values('SEASON_ID', ascending=False).head(5)

    # Calculate per-game averages
    career['MIN'] = career['MIN'] / career['GP']
    career['PTS'] = career['PTS'] / career['GP']
    career['AST'] = career['AST'] / career['GP']
    career['REB'] = career['REB'] / career['GP']
    career['STL'] = career['STL'] / career['GP']
    career['BLK'] = career['BLK'] / career['GP']

    # Calculate percentages
    career['FG%'] = (career['FGM'] / career['FGA']) * 100
    career['3P%'] = (career['FG3M'] / career['FG3A']) * 100
    career['FT%'] = (career['FTM'] / career['FTA']) * 100

    career = career.round(2)

    return career[['SEASON_ID', 'MIN', 'PTS', 'AST', 'REB', 'STL', 'BLK', 'FG%', '3P%', 'FT%']]

def insert_player_stats(player_id, player_name, stats):
    insert_predicted_stats(player_id, player_name, "2025-26", stats)
