# NFL FantaSIM: A Data Driven Look at Common Drafting Strategies

An in-depth analysis of draft strategy for optimal fantasy football performance, using data-driven approaches and simulations. 

This project is licensed under the MIT License.

Author
--------
Gian Favero, 2024

## Usage

## Requirements
- Python 3.x

### Jupyter Notebook Tutorial
Take a look at the notebook included for an annotated look at the assumptions and development of the simulation environment.

### Command-line Usage:
```bash
python nfl_fantasy_simulator.py <num_simulations> <order_system> <strategy> <num_teams>
```
- **num_simulations**: Number of simulations to run (e.g., 1000)
- **order_system**: Draft order system ('snake' or 'linear')
- **strategy**: Draft strategy ('BPA', 'WR_HEAVY', 'RB_HEAVY', 'EARLY_QB', 'EARLY_TE')
- **num_teams**: Number of teams in the fantasy league (e.g., 12)

## Description
Here we are using a consensus ADP 2023 ranking from FantasyPros according to 3 different sources: ESPN, Yahoo, and Sleeper for a 12 team league with half PPR scoring. 
We assume the number of draft rounds is equal to the number of roster spots including a bench. Teams managers can employ a 'BPA', 'Robust RB', 'WR Heavy', 'Early TE', 
or 'Early QB' draft strategy. To examine a particular draft strategy, we set our team to the one in question and all others to BPA. 

By comparing total points for across the entire season, we can approximate how well such a team would have done. 
This obviously grossly underestimates the notion of trades, waiver pickups, and the use of a bench.
However, it is an assumption that follows the claim that with modern information at our disposal such transactions provide parallel success at best. 
The optimal line-up is provided on a weekly basis - however this does not account for season ending injuries at positions with no substitute. 
Monte Carlo simulations should aid in fixing this issue (e.g., drafting Anthony Richardson in 2023).

## Sample Results
| **Strategy** | **Total Points** |
| --- | --- |
| BPA | 1687.00 |
| WR_HEAVY | 1635.66 |
| RB_HEAVY | 1740.78 |
| EARLY_QB | 1713.70 |
| EARLY_TE | 1682.98 |

**Simulation Details**

* Number of teams: 12
* Number of simulations: 1000
* Draft order: Snake
* Points: Half-PPR

##  Analysis
The common consensus among many on the platform is that zero RB or WR heavy drafting strategies reign supreme in 2024. In half-PPR or standard leagues, perhaps there is still time to zig while the majority begin to zag.
Top running backs still provide high reward to fantasy owners that are willing to stick it out at the top of the draft and choose dual-threat, high volume options (Christian McCaffrey, Bijan Robinson, Breece Hall) 
over the young stock of receivers who are receiving ever more acclaim in 2024.

## Data
The simulator uses two CSV files:
FantasyPros_2023_Overall_ADP_Rankings.csv: ADP data for the 2023 season
FantasyPros_Fantasy_Football_Points_HALF.csv: Half PPR data for the 2023 season
These files should be placed in a data directory within the project root.
