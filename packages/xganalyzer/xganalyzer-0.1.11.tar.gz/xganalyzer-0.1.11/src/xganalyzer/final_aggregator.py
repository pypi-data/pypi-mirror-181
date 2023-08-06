from pandas import DataFrame


class FinalAggregator:
    def __init__(self, games_df: DataFrame, metrics_df: DataFrame):
        self.games_df = games_df
        self.metrics_df = metrics_df

    def aggregate(self):
        home_metrics_df = self.metrics_df.add_prefix('home_team_')
        away_metrics_df = self.metrics_df.add_prefix('away_team_')

        result_df = self.games_df.merge(home_metrics_df, left_on=['id', 'home_team_id'],
                                        right_on=['home_team_game_id', 'home_team_team_id'])

        result_df = result_df.merge(away_metrics_df, left_on=['id', 'away_team_id'],
                                    right_on=['away_team_game_id', 'away_team_team_id'])

        result_df = result_df.drop(columns=['home_team_game_id', 'home_team_team_id', 'away_team_game_id', 'away_team_team_id'])

        return result_df.set_index(['id'])
