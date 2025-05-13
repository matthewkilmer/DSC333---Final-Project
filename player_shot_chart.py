# shot_chart.py (Helper functions)

import matplotlib.pyplot as plt
from matplotlib.patches import Arc
import pandas as pd
from nba_api.stats.static import players
from nba_api.stats.endpoints import shotchartdetail

# Draw the court
def draw_court(ax=None):
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 9))

    # Court lines and arcs
    ax.plot([-250, 250], [-47.5, -47.5], 'k-')
    ax.plot([-250, 250], [422.5, 422.5], 'k-')
    ax.plot([-250, -250], [-47.5, 422.5], 'k-')
    ax.plot([250, 250], [-47.5, 422.5], 'k-')
    ax.plot([-30, 30], [-7.5, -7.5], 'k-', lw=2)
    ax.plot([-80, -80], [-47.5, 142.5], 'k-')
    ax.plot([80, 80], [-47.5, 142.5], 'k-')
    ax.plot([-60, -60], [-47.5, 142.5], 'k-')
    ax.plot([60, 60], [-47.5, 142.5], 'k-')
    ax.plot([-80, 80], [142.5, 142.5], 'k-')
    ax.plot([220, 220], [-47.5, 92.5], 'k-')
    ax.plot([-220, -220], [-47.5, 92.5], 'k-')

    arcs = [
        Arc((0, 0), 475, 475, theta1=22, theta2=158, linewidth=1.5),
        Arc((0, 142.5), 120, 120, theta1=0, theta2=180, linewidth=1.5),
        Arc((0, 142.5), 120, 120, theta1=180, theta2=360, linestyle='dashed', linewidth=1.5),
        Arc((0, 0), 15, 15, theta1=0, theta2=360, linewidth=1.5),
        Arc((0, 0), 80, 80, theta1=0, theta2=180, linewidth=1.5),
        Arc((0, 422.5), 120, 120, theta1=180, theta2=360, linewidth=1.5),
    ]

    for arc in arcs:
        ax.add_patch(arc)

    ax.set_xlim(-250, 250)
    ax.set_ylim(-47.5, 470)
    ax.set_aspect('equal')
    ax.axis('off')

    return ax

# Get player ID from NBA API
def get_player_id(player_name):
    players_list = players.find_players_by_full_name(player_name)
    if players_list:
        return players_list[0]["id"]
    return None

# Plot shot chart based on player, season, and season type
def plot_shot_chart(player_name, season, season_type):
    player_id = get_player_id(player_name)
    if player_id is None:
        return None, "Player not found."

    try:
        shots = shotchartdetail.ShotChartDetail(
            team_id=0,
            player_id=player_id,
            season_nullable=season,
            season_type_all_star=season_type,
            context_measure_simple='FGA'
        )
    except Exception as e:
        return None, f"API error: {e}"

    df = shots.get_data_frames()[0]
    if df.empty:
        return None, "No shot data found for the player in the given season and season type."

    made = df[df['SHOT_MADE_FLAG'] == 1]
    missed = df[df['SHOT_MADE_FLAG'] == 0]

    fig, ax = plt.subplots(figsize=(10, 9))
    draw_court(ax)
    ax.scatter(made['LOC_X'], made['LOC_Y'], c='green', label='Made', alpha=0.3, edgecolors='w', s=100)
    ax.scatter(missed['LOC_X'], missed['LOC_Y'], c='red', label='Missed', alpha=0.3, edgecolors='w', s=100)
    ax.set_title(f"{player_name} Shot Chart ({season} - {season_type})", fontsize=18)
    ax.legend(loc='upper right')

    return fig, None


