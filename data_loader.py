# data_loader.py
from nba_api.stats.static import players
from nba_api.stats.endpoints import PlayerCareerStats
import pandas as pd
import os
from database import insert_predicted_stats
from model import predict_stats_from_trend

def get_player_id(player_name):
    player_dict = players.find_players_by_full_name(player_name)
    if player_dict:
        return player_dict[0]['id']
    else:
        raise ValueError("Player not found")

def get_last_5_season_avgs(player_id):
    # Fetch career stats for the player
    try:
        print(f"Fetching career stats for player_id: {player_id} (Type: {type(player_id)})")
        career = PlayerCareerStats(player_id=player_id)
        career = career.get_data_frames()[0]
    except Exception as e:
        print(f"Error fetching career stats: {str(e)}")
        raise

    career = career[career['LEAGUE_ID'] == '00']  # NBA only
    career = career.sort_values('SEASON_ID', ascending=False).head(5)

    # Rename SEASON_ID to season_id for consistency
    career.rename(columns={'SEASON_ID': 'season_id'}, inplace=True)

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

    # Rename columns to match the expected names
    career.rename(columns={
        'MIN': 'minutes_per_game',
        'PTS': 'points_per_game',
        'AST': 'assists_per_game',
        'REB': 'rebounds_per_game',
        'STL': 'steals_per_game',
        'BLK': 'blocks_per_game',
        'FG%': 'fg_percentage',
        '3P%': 'three_pt_percentage',
        'FT%': 'ft_percentage'
    }, inplace=True)

    # Round all numerical values to 2 decimal places
    career = career.round(2)

    # Return only the relevant columns
    return career[['season_id', 'minutes_per_game', 'points_per_game', 'assists_per_game',
                   'rebounds_per_game', 'steals_per_game', 'blocks_per_game',
                   'fg_percentage', 'three_pt_percentage', 'ft_percentage']
