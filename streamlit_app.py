import streamlit as st
import requests

# FastAPI server URL (replace with your actual URL or local address)
API_URL = "http://127.0.0.1:8000/predict/"

def get_player_prediction(player_name):
    response = requests.post(API_URL, json={"player_name": player_name})
    return response.json()

# Streamlit app
def main():
    st.title("NBA Player Stat Prediction")

    # Input player name
    player_name = st.text_input("Enter NBA Player Name")

    if player_name:
        st.write(f"Fetching prediction for {player_name}...")

        # Get the predictions from FastAPI
        predictions = get_player_prediction(player_name)

        if 'error' in predictions:
            st.error(f"Error: {predictions['error']}")
        else:
            st.write(f"Predictions for {player_name} (Next Season):")
            st.write(predictions)

if __name__ == "__main__":
    main()
