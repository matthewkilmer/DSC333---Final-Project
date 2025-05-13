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
