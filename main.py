# main.py
from fastapi import FastAPI
from pydantic import BaseModel
from database import fetch_player_data
from data_loader import insert_player_stats, get_player_id, get_last_5_season_avgs
from model import predict_stats_from_trend

app = FastAPI()

class PlayerRequest(BaseModel):
    player_name: str

@app.post("/predict/")
def predict(request: PlayerRequest):
    player_name = request.player_name
    try:
        player_id = get_player_id(player_name)
        player_data = get_last_5_season_avgs(player_id)
        predictions = predict_stats_from_trend(player_data)
        insert_player_stats(player_id, player_name, predictions)
        return {"player_name": player_name, "predictions": predictions}
    except Exception as e:
        return {"error": str(e)}
