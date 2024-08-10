"""
NFL Fantasy Simulator

This script runs a Monte Carlo simulation of an NFL fantasy season, using a specified draft order and strategy.
It calculates the average season points over a specified number of simulations.

Usage:
    python nfl_fantasy_simulator.py <num_simulations> <order_system> <strategy> <num_teams>

Arguments:
    num_simulations (int): Number of simulations to run
    order_system (str): Draft order system ('snake' or 'linear')
    strategy (str): Draft strategy ('BPA', 'WR_HEAVY', 'RB_HEAVY', 'EARLY_QB', 'EARLY_TE')
    num_teams (int): Number of teams in the fantasy league

Returns:
    Average season points over the specified number of simulations
"""

import sys
import pandas as pd
from tqdm import tqdm
import random
from nfl_fantasy.roster import FantasyRoster, DraftStrategy

class DraftConfiguration:
    def __init__(self, order_system, strategy, number_of_teams, roster):
        self.order_system = order_system
        self.strategy = strategy
        self.number_of_teams = number_of_teams
        self.roster = roster

def run_simulation(config, ADP_data, half_ppr_data):
    # Generate team with a strategy under study
    team = FantasyRoster(config.roster.copy(), config.strategy)

    # Generate league
    fantasy_league = [team] + [FantasyRoster(config.roster.copy(), DraftStrategy.BPA) for i in range(config.number_of_teams-1)]

    # Generate draft order
    if config.order_system == 'snake':
        forward_draft_order = list(range(config.number_of_teams))
        random.shuffle(forward_draft_order)
        draft_order = forward_draft_order + forward_draft_order[::-1]
        rounds = sum(config.roster.values()) // 2
        draft_order *= rounds
        draft_order += forward_draft_order
    else:
        draft_order = list(range(config.number_of_teams))
        rounds = sum(config.roster.values())
        draft_order *= rounds

    # Make version of the ADP data for the draft
    ADP_data_draft = ADP_data.copy()

    # Start the draft
    for i, pick in enumerate(draft_order):
        team = fantasy_league[pick]
        player = team.choose_player(ADP_data_draft)
        ADP_data_draft = ADP_data_draft[ADP_data_draft['Player'] != player['Player']]

    team = fantasy_league[0]

    # Calculate season points
    season_points = team.get_season_points(half_ppr_data, config.roster)

    return season_points

def run_monte_carlo_simulations(num_simulations, config, ADP_data, half_ppr_data):
    season_points = []
    for i in tqdm(range(num_simulations), desc="Running simulations"):
        season_points.append(run_simulation(config, ADP_data, half_ppr_data))
    return season_points

def main(num_simulations, order_system, strategy_name, num_teams):

    strategy_map = {
        'BPA': DraftStrategy.BPA,
        'WR_HEAVY': DraftStrategy.WR_HEAVY,
        'RB_HEAVY': DraftStrategy.RB_HEAVY,
        'EARLY_QB': DraftStrategy.EARLY_QB,
        'EARLY_TE': DraftStrategy.EARLY_TE
    }

    if strategy_name not in strategy_map:
        print(f"Invalid strategy: {strategy_name}")
        sys.exit(1)

    strategy = strategy_map[strategy_name]

    config = DraftConfiguration(order_system, strategy, num_teams, {
        'QB': 1,
        'RB': 2,
        'WR': 2,
        'TE': 1,
        'FLEX': 1,
        'K': 1,
        'DST': 1,
        'BENCH': 6,
        'nan': 0
    })

    # Load ADP data
    ADP_23 = pd.read_csv('data\FantasyPros_2023_Overall_ADP_Rankings.csv')
    ADP_23['POS'] = ADP_23['POS'].str.translate(str.maketrans('', '', '1234567890'))

    # Load Half PPR data
    HALF_PPR_23 = pd.read_csv('data\FantasyPros_Fantasy_Football_Points_HALF.csv')

    season_points = run_monte_carlo_simulations(num_simulations, config, ADP_23, HALF_PPR_23)

    print(f"Average season points over {num_simulations} simulations: {sum(season_points) / num_simulations}")

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python nfl_fantasy_simulator.py <num_simulations> <order_system> <strategy> <num_teams>")
        sys.exit(1)

    num_simulations = int(sys.argv[1])
    order_system = sys.argv[2]
    strategy_name = sys.argv[3]
    num_teams = int(sys.argv[4])

    main(num_simulations, order_system, strategy_name, num_teams)