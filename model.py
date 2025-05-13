# model.py
from sklearn.linear_model import LinearRegression
import numpy as np

def predict_stats_from_trend(player_data):
    # Normalize percentages to be between 0 and 1
    player_data['fg_percentage'] = player_data['fg_percentage'] / 100
    player_data['three_pt_percentage'] = player_data['three_pt_percentage'] / 100
    player_data['ft_percentage'] = player_data['ft_percentage'] / 100

    # Create a "season number" column: 0 to 4 (oldest to most recent)
    player_data = player_data.sort_values(by='season_id').reset_index(drop=True)
    X = [[i] for i in range(len(player_data))]

    stats_to_predict = [
        'minutes_per_game',
        'points_per_game',
        'assists_per_game',
        'rebounds_per_game',
        'steals_per_game',
        'blocks_per_game',
        'fg_percentage',
        'three_pt_percentage',
        'ft_percentage'
    ]

    predictions = {}

    for stat in stats_to_predict:
        y = player_data[stat].tolist()

        # Train a simple linear model for this stat
        model = LinearRegression()
        model.fit(X, y)

        # Predict the stat for the "next season" (season index 5)
        next_season = [[5]]
        predicted_value = model.predict(next_season)[0]
        predictions["predicted_" + stat] = float(round(predicted_value, 4))

    return predictions
