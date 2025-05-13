# database.py
import mysql.connector
import pandas as pd
import os

def get_db_connection():
    pw = os.getenv("DB_PASSWORD")
    if not pw:
        raise ValueError("Database password not set in environment variables.")
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password=pw,
        database="nba_project"
    )

def fetch_player_data(player_name):
    conn = get_db_connection()
    query = f"""
        SELECT * FROM player_past_stats 
        WHERE player_name = '{player_name}'
        ORDER BY season_id DESC LIMIT 5
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Insert player's last 5 seasons' stats into MySQL
def insert_player_stats(player_id, player_name, stats):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        for _, row in stats.iterrows():
            cursor.execute("""
                INSERT INTO player_past_stats (
                    player_id, season_id, player_name, minutes_per_game,
                    points_per_game, assists_per_game, rebounds_per_game,
                    steals_per_game, blocks_per_game, fg_percentage,
                    three_pt_percentage, ft_percentage
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    minutes_per_game = VALUES(minutes_per_game),
                    points_per_game = VALUES(points_per_game),
                    assists_per_game = VALUES(assists_per_game),
                    rebounds_per_game = VALUES(rebounds_per_game),
                    steals_per_game = VALUES(steals_per_game),
                    blocks_per_game = VALUES(blocks_per_game),
                    fg_percentage = VALUES(fg_percentage),
                    three_pt_percentage = VALUES(three_pt_percentage),
                    ft_percentage = VALUES(ft_percentage)
            """, (
                player_id,
                row['season_id'],
                player_name,
                row['minutes_per_game'],
                row['points_per_game'],
                row['assists_per_game'],
                row['rebounds_per_game'],
                row['steals_per_game'],
                row['blocks_per_game'],
                row['fg_percentage'],
                row['three_pt_percentage'],
                row['ft_percentage']
            ))
        conn.commit()
        print(f"Stats inserted/updated for {player_name}")
    except Exception as e:
        print(f"Error inserting/updating stats for {player_name}: {str(e)}")
    finally:
        cursor.close()
        conn.close()

def insert_predicted_stats(player_id, player_name, season_id, predictions):
    conn = get_db_connection()
    cursor = conn.cursor()

    player_id = int(player_id)
    predictions = {key: float(value) for key, value in predictions.items()}

    cursor.execute("""
        INSERT INTO player_predicted_stats (
            player_id, season_id, player_name, predicted_minutes_per_game,
            predicted_points_per_game, predicted_assists_per_game,
            predicted_rebounds_per_game, predicted_steals_per_game, predicted_blocks_per_game,
            predicted_fg_percentage, predicted_three_pt_percentage, predicted_ft_percentage
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE       
            predicted_minutes_per_game = VALUES(predicted_minutes_per_game),
            predicted_points_per_game = VALUES(predicted_points_per_game),
            predicted_assists_per_game = VALUES(predicted_assists_per_game),
            predicted_rebounds_per_game = VALUES(predicted_rebounds_per_game),
            predicted_steals_per_game = VALUES(predicted_steals_per_game),
            predicted_blocks_per_game = VALUES(predicted_blocks_per_game),
            predicted_fg_percentage = VALUES(predicted_fg_percentage),
            predicted_three_pt_percentage = VALUES(predicted_three_pt_percentage),
            predicted_ft_percentage = VALUES(predicted_ft_percentage)
    """, (
        player_id,
        season_id,
        player_name,
        predictions['minutes_per_game'],
        predictions['points_per_game'],
        predictions['assists_per_game'],
        predictions['rebounds_per_game'],
        predictions['steals_per_game'],
        predictions['blocks_per_game'],
        predictions['fg_percentage'],
        predictions['three_pt_percentage'],
        predictions['ft_percentage']
    ))

    conn.commit()
    cursor.close()
    conn.close()
    print(f"Prediction inserted/updated for {player_name} ({season_id})")

# Retrieve predicted stats for a player
def fetch_predicted_stats(player_name, season_id='2025-26'):
    conn = get_db_connection()
    query = f"""
        SELECT * FROM player_predicted_stats 
        WHERE player_name = '{player_name}' AND season_id = '{season_id}'
    """
    df = pd.read_sql(query, conn)
    conn.close()

    if df.empty:
        return None  # If no predictions are found
    return df.iloc[0]
