import pandas as pd
import streamlit as st
import requests

def get_player_prediction(player_name):
    url = "http://127.0.0.1:8000/predict/"
    payload = {"player_name": player_name}

    try:
        print(f"Sending request to {url} with payload: {payload}")  # Debug
        response = requests.post(url, json=payload)
        print(f"Response status code: {response.status_code}")  # Debug
        print(f"Response content: {response.text}")  # Debug
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Failed to fetch predictions. Status code: {response.status_code}"}
    except Exception as e:
        print(f"Error in get_player_prediction: {str(e)}")  # Debug
        return {"error": str(e)}

def get_shot_chart(player_name, season, season_type):
    # URL of the FastAPI backend
    url = "http://127.0.0.1:8000/shot_chart/"  # Update this if hosted elsewhere

    # Payload for the POST request
    payload = {
        "player_name": player_name,
        "season": season,
        "season_type": season_type
    }

    try:
        # Send POST request to the FastAPI endpoint
        response = requests.post(url, json=payload)

        # Check if the request was successful
        if response.status_code == 200:
            return response.json()  # Return the JSON response
        else:
            return {"error": f"Failed to fetch shot chart. Status code: {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}

def main():
    st.set_page_config(page_title="NBA Stat Predictor", layout="wide")
    st.title("🏀 NBA Player Stat Predictions and Shot Chart")

    # Input player name
    player_name = st.text_input("Enter NBA Player Name")
    season = st.text_input("Enter Season (e.g., 2021-22)")
    season_type = st.selectbox("Select Season Type", ["Regular Season", "Playoffs"])

    if player_name:
        predictions = get_player_prediction(player_name)

        if isinstance(predictions, dict) and 'error' in predictions:
            st.error(f"Error: {predictions['error']}")
        elif predictions is None or (hasattr(predictions, 'empty') and predictions.empty):
            st.error(f"No predictions found for {player_name}.")
        else:
            st.subheader(f"Predictions for {player_name.title()} (Next Season):")

            # Extract the predictions dictionary
            prediction_data = predictions.get("predictions", {})

            # Convert to DataFrame
            df = pd.DataFrame([prediction_data])

            # Clean column names
            df.columns = [col.replace("_", " ").title() for col in df.columns]

            # Round values
            df = df.round(2)

            # Display table with full width
            st.dataframe(df)

    if player_name and season and season_type:
        shot_chart_response = get_shot_chart(player_name, season, season_type)

        if "error" in shot_chart_response:
            st.error(f"Error: {shot_chart_response['error']}")
        else:
            shot_chart_url = shot_chart_response.get("shot_chart_url")
            if shot_chart_url:
                st.image(shot_chart_url, caption=f"{player_name}'s Shot Chart ({season} - {season_type})")
            else:
                st.error("No shot chart available.")
    else:
        st.warning("Please provide all inputs: Player Name, Season, and Season Type.")

if __name__ == "__main__":
    main()




