from abc import ABC, abstractmethod
from pandas import DataFrame, Series
import time


class AbstractMetric(ABC):
    @abstractmethod
    def calculate(self, result_df: DataFrame, team_id: int):
        pass

    @staticmethod
    def round(value, precision=None):
        if not precision:
            return value

        return round(value, precision)


class BasicSumMetric(AbstractMetric):
    def __init__(self, name, precision=None):
        self.name = name
        self.precision = precision

    def calculate(self, result_df: DataFrame, team_id: int):
        if team_id in result_df.index:
            return self.round(result_df.loc[team_id][self.name], self.precision)

        return 0


class ExpectedGaolsPer90MinutesMetric(AbstractMetric):
    def __init__(self, expected_goals_metric, duration_metric, precision=None):
        self.expected_goals_metric = expected_goals_metric
        self.duration_metric = duration_metric
        self.precision = precision

    def calculate(self, result_df: DataFrame, team_id: int):
        if team_id in result_df.index:
            if result_df.loc[team_id][self.duration_metric] > 0:
                return self.round(90 * result_df.loc[team_id][self.expected_goals_metric] / result_df.loc[team_id][
                    self.duration_metric], self.precision)

        return 0


class ExpectedGaolsPerShotMetric(AbstractMetric):
    def __init__(self, expected_goals_metric, count_metric, precision=None):
        self.expected_goals_metric = expected_goals_metric
        self.count_metric = count_metric
        self.precision = precision

    def calculate(self, result_df: DataFrame, team_id: int):
        if team_id in result_df.index:
            if result_df.loc[team_id][self.count_metric] > 0:
                return self.round(
                    result_df.loc[team_id][self.expected_goals_metric] / result_df.loc[team_id][self.count_metric],
                    self.precision)

        return 0


class AverageMetric(AbstractMetric):
    def __init__(self, name, precision=None):
        self.name = name
        self.precision = precision

    def calculate(self, result_df: DataFrame, team_id: int):
        value = 0
        count = 0

        for team_id in result_df.index:
            value += result_df.loc[team_id][self.name]

            if result_df.loc[team_id][self.name] > 0:
                count += 1

        return self.round(value / count, self.precision)


class ExpectedGaolsPer90IndexMinutesMetric(ExpectedGaolsPer90MinutesMetric):
    def calculate(self, result_df: DataFrame, team_id: int):
        if team_id in result_df.index:
            if result_df.loc[team_id][self.expected_goals_metric] > 0:
                mean = self.mean(result_df)

                if mean > 0:
                    return self.round(super().calculate(result_df, team_id) / mean, self.precision)

                return 0

        return 0

    def mean(self, result_df: DataFrame):
        value = 0
        count = 0

        for team_id in result_df.index:
            item = super().calculate(result_df, team_id)

            if item == 0:
                continue

            value += item

            if item > 0:
                count += 1

        if count > 0:
            return value / count

        return 0


class ExpectedGaolsPer90MinutesAverageMetric(ExpectedGaolsPer90MinutesMetric):
    def calculate(self, result_df: DataFrame, team_id: int):
        value = 0
        count = 0

        for team_id in result_df.index:
            item = super().calculate(result_df, team_id)

            if item == 0:
                continue

            value += item

            if item > 0:
                count += 1

        if count > 0:
            return self.round(value / count, self.precision)

        return 0


class SeasonAggregator:
    def __init__(self, games_df: DataFrame, game_aggregations_df: DataFrame, tour_interval: int = 4 * 24 * 3600,
                 feature_interval: int = 28 * 24 * 3600):
        self.games_df = games_df
        self.games_df = self.games_df.set_index(['id'])

        self.game_aggregations_df = game_aggregations_df
        self.game_aggregations_df = self.game_aggregations_df.set_index(['game_id', 'team_id'])

        self.tour_interval = tour_interval
        self.feature_interval = feature_interval

    def get_ordered_games(self):
        return self.games_df.sort_values(by=['start_time'])

    def aggregate(self, metrics: dict):
        games_df = self.get_ordered_games()

        round_start_time = 0
        max_time = time.time() + self.feature_interval

        result_df = self.create_result_dataframe(metrics)
        accumulator_df = self.create_accumulator()
        round_accumulator_df = self.create_accumulator()

        for game_id in games_df.index:
            if round_start_time == 0:
                round_start_time = games_df['start_time'][game_id]

            if round_start_time != 0 and games_df['start_time'][game_id] - round_start_time > self.tour_interval:
                self.complete_round(accumulator_df, round_accumulator_df)
                round_start_time = games_df['start_time'][game_id]
                round_accumulator_df = self.create_accumulator()

            if games_df.loc[game_id]['start_time'] > max_time:
                break

            home_team_id = games_df.loc[game_id]['home_team_id']
            away_team_id = games_df.loc[game_id]['away_team_id']
            home_key = (game_id, home_team_id)
            away_key = (game_id, away_team_id)

            home_team_metrics = self.game_aggregations_df.loc[home_key]
            self.populate_accumulator(home_team_id, round_accumulator_df, home_team_metrics)
            self.create_result_row(game_id, home_team_id, accumulator_df, metrics, result_df)

            away_team_metrics = self.game_aggregations_df.loc[away_key]
            self.populate_accumulator(away_team_id, round_accumulator_df, away_team_metrics)
            self.create_result_row(game_id, away_team_id, accumulator_df, metrics, result_df)

        return result_df

    def create_result_dataframe(self, metrics: dict):
        columns = self.game_aggregations_df.index.names + list(metrics.keys())
        team_metrics_accumulator_df = DataFrame(columns=columns)
        return team_metrics_accumulator_df.set_index(self.game_aggregations_df.index.names)

    def create_accumulator(self):
        columns = ['team_id'] + self.game_aggregations_df.columns.tolist()
        team_metrics_accumulator_df = DataFrame(columns=columns)
        return team_metrics_accumulator_df.set_index(['team_id'])

    @staticmethod
    def create_result_row(game_id: int, team_id: int, accumulator_df: DataFrame, metrics: dict, result_df: DataFrame):
        key = (game_id, team_id)
        if team_id in accumulator_df.index:
            row = {}
            for metric, value in metrics.items():
                row[metric] = value.calculate(accumulator_df, team_id)

            result_df.loc[key, :] = Series(row)
        else:
            result_df.loc[key, :] = None

    @staticmethod
    def populate_accumulator(team_id: int, accumulator_df: DataFrame, metrics: dict):
        if team_id in accumulator_df.index:
            for key, value in metrics.items():
                accumulator_df.loc[team_id][key] += metrics[key]
        else:
            accumulator_df.loc[team_id, :] = metrics

    def complete_round(self, accumulator_df: DataFrame, round_accumulator_df: DataFrame):
        for team_id in round_accumulator_df.index:
            self.populate_accumulator(team_id, accumulator_df, round_accumulator_df.loc[team_id])
