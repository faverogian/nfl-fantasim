import pandas as pd

class DraftStrategy:
    BPA = 'BPA'
    RB_HEAVY = 'RB Heavy'
    WR_HEAVY = 'WR Heavy'
    EARLY_QB = 'Early QB'
    EARLY_TE = 'Early TE'

class FantasyRoster:
    def __init__(self, roster, strategy):
        self.roster = roster
        self.strategy = strategy
        self.players = []

    def choose_player(self, adp_data: pd.DataFrame):
        strategy_func = self._get_strategy_func()
        player, pos = strategy_func(adp_data)
        self.roster[pos] -= 1
        self.players.append(player)
        return player
    
    def get_season_points(self, half_ppr: pd.DataFrame, roster: dict) -> float:
        points = 0
        for week in range(1, 17):
            points += self._get_week_points(week, half_ppr, roster)
        return points
    
    def _get_strategy_func(self):
        strategies = {
            DraftStrategy.BPA: self._bpa_strategy,
            DraftStrategy.RB_HEAVY: self._rb_heavy_strategy,
            DraftStrategy.WR_HEAVY: self._wr_heavy_strategy,
            DraftStrategy.EARLY_QB: self._early_qb_strategy,
            DraftStrategy.EARLY_TE: self._early_te_strategy,
        }
        return strategies[self.strategy]
    
    def _bpa_strategy(self, adp_data: pd.DataFrame):
        for index, player in adp_data.iterrows():
            if self.roster[player['POS']] > 0:
                return player, player['POS']
            elif self.roster['FLEX'] > 0 and player['POS'] in ['RB', 'WR']:
                return player, 'FLEX'
            elif self.roster['BENCH'] > 0:
                return player, 'BENCH'
            
    def _rb_heavy_strategy(self, adp_data):
        for index, player in adp_data.iterrows():
            if self.roster['RB'] > 0:
                if player['POS'] == 'RB':
                    return player, 'RB'
                else:
                    continue
            elif self.roster['FLEX'] > 0:
                if player['POS'] == 'RB':
                    return player, 'FLEX'
                else:
                    continue
            else:
                if self.roster['WR'] > 0:
                    if player['POS'] == 'WR':
                        return player, 'WR'
                    else:
                        continue
                elif self.roster['FLEX'] > 0:
                    if player['POS'] == 'WR':
                        return player, 'FLEX'
                    else:
                        continue
                else:
                    return self._bpa_strategy(adp_data)
            
    def _wr_heavy_strategy(self, adp_data):
        for index, player in adp_data.iterrows():
            if self.roster['WR'] > 0:
                if player['POS'] == 'WR':
                    return player, 'WR'
                else:
                    continue
            elif self.roster['FLEX'] > 0:
                if player['POS'] == 'WR':
                    return player, 'FLEX'
                else:
                    continue
            else:
                if self.roster['RB'] > 0:
                    if player['POS'] == 'RB':
                        return player, 'RB'
                    else:
                        continue
                elif self.roster['FLEX'] > 0:
                    if player['POS'] == 'RB':
                        return player, 'FLEX'
                    else:
                        continue
                else:
                    return self._bpa_strategy(adp_data)
            
    def _early_qb_strategy(self, adp_data):
        if len(self.players) == 2 and self.roster['QB'] > 0:
            for index, player in adp_data.iterrows():
                if player['POS'] == 'QB':
                    return player, 'QB'
        else:
            return self._bpa_strategy(adp_data)
                
    def _early_te_strategy(self, adp_data):
        if len(self.players) == 2 and self.roster['TE'] > 0:
            for index, player in adp_data.iterrows():
                if player['POS'] == 'TE':
                    return player, 'TE'
        else:
            return self._bpa_strategy(adp_data)
        
    def _get_week_points(self, week: int, half_ppr: pd.DataFrame, roster: dict) -> float:
        # Get the players for the team
        players = [player['Player'] for player in self.players]
        
        # Get the points for the players for the week
        points = half_ppr[half_ppr['Player'].isin(players)][['Player', str(week), 'Pos']]

        # Replace 'BYE' and '-' with 0
        points = points.replace('BYE', 0)
        points = points.replace('-', 0)
        points[str(week)] = points[str(week)].astype(float)

        # Sort the players by points
        points = points.sort_values(by=[str(week)], ascending=False)

        # Get the optimal lineup for the week using the roster configuration
        roster = roster.copy()
        for index, row in points.iterrows():
            pos = row['Pos']
            if roster.get(pos, 0) > 0:
                roster[pos] -= 1
            elif roster.get('FLEX', 0) > 0 and (pos == 'RB' or pos == 'WR'):
                roster['FLEX'] -= 1
            else:
                # Pop from the dataframe
                points = points.drop(index)

        # Return the points for the week
        return points[str(week)].sum()