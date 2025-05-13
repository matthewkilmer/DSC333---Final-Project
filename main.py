# main.py
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from database import insert_predicted_stats, insert_player_stats
from data_loader import get_player_id, get_last_5_season_avgs
from model import predict_stats_from_trend
from player_shot_chart import plot_shot_chart
import matplotlib.pyplot as plt
import os

app = FastAPI()

class PlayerRequest(BaseModel):
    player_name: str
    season: str = None # Add season to the request model
    season_type: str = None # Add season type to the request model

@app.post("/predict/")
def predict(request: PlayerRequest):
    player_name = request.player_name
    try:
        print(f"Received prediction request for player: {player_name}")  # Debug: Log player name

        # Step 1: Get player ID
        player_id = get_player_id(player_name)
        print(f"Player ID for {player_name}: {player_id}")  # Debug: Log player ID

        # Step 2: Get last 5 seasons' averages
        player_data = get_last_5_season_avgs(player_id)
        print(f"Player data for {player_name}: {player_data}")  # Debug: Log player data

        # Step 3: Insert player stats into the database
        insert_player_stats(player_id, player_name, player_data)
        print(f"Player stats inserted for {player_name}")  # Debug: Confirm insertion

        # Step 4: Generate predictions
        predictions = predict_stats_from_trend(player_data)
        print(f"Predictions for {player_name}: {predictions}")  # Debug: Log predictions

        # Step 5: Insert predictions into the database
        insert_predicted_stats(player_id, player_name, '2025-26', predictions)
        print(f"Predictions inserted for {player_name} (2025-26)")  # Debug: Confirm insertion

        # Return the predictions
        return {"player_name": player_name, "predictions": predictions}

    except Exception as e:
        print(f"Error processing prediction for {player_name}: {str(e)}")  # Debug: Log the error
        return {"error": str(e)}

@app.post("/shot_chart/")
def shot_chart(request: PlayerRequest):
    player_name = request.player_name
    season = request.season
    season_type = request.season_type

    try:
        # Generate the shot chart
        fig, error = plot_shot_chart(player_name, season, season_type)
        if error:
            return {"error": error}

        # Ensure the static directory exists
        os.makedirs("static", exist_ok=True)

        # Save the figure as an image
        fig_path = f"static/{player_name}_shot_chart.png"
        fig.savefig(fig_path, bbox_inches="tight")
        plt.close(fig)

        # Return the path to the saved image
        return {"shot_chart_url": fig_path}
    except Exception as e:
        return {"error": str(e)}

