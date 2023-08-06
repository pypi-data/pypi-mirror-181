from enum import Enum
import numpy
import pandas as pd
from pandas import DataFrame


class CalculateType(Enum):
    DURATION = 1
    EXPECTED_GOALS = 2
    SHOTS_COUNT = 3
    GOALS = 4
    GAMES_COUNT = 5


class CalculateLocation(Enum):
    TOTAL = 1
    HOME = 2
    AWAY = 3


class CalculateContext:
    def __init__(
            self,
            calculate_type: CalculateType = CalculateType.EXPECTED_GOALS,
            calculate_location: CalculateLocation = CalculateLocation.TOTAL,
            first_half: bool = True,
            second_half: bool = True,
            own_shots: bool = True,
            skip_penalties: bool = False,
            finish_on_red_card: bool = False,
            home_team_goals: int = None,
            difference_from: int = None,
            difference_to: int = None,
            minute_from: int = None,
            minute_to: int = None,
            max_value: float = 1,
            precision: int = None
    ):
        self.calculate_type = calculate_type
        self.calculate_location = calculate_location
        self.first_half = first_half
        self.second_half = second_half
        self.own_shots = own_shots
        self.skip_penalties = skip_penalties
        self.finish_on_red_card = finish_on_red_card
        self.home_team_goals = home_team_goals
        self.difference_from = difference_from
        self.difference_to = difference_to
        self.minute_from = minute_from
        self.minute_to = minute_to
        self.max_value = max_value
        self.precision = precision


class GamesEventsAggregator:
    GAME_DURATION = 90
    HALF_DURATION = 45

    def __init__(
            self, games_df: DataFrame, events_df: DataFrame
    ):
        self.games_df = games_df
        self.games_df = self.games_df.set_index('id')

        self.events_df = events_df

    def get_unique_games(self):
        return self.games_df.index

    def get_events(self, game_id: int):
        return self.events_df.loc[self.events_df['game_id'] == game_id].copy()

    def get_home_team_id(self, game_id: int):
        return self.games_df['home_team_id'][game_id]

    def get_away_team_id(self, game_id: int):
        return self.games_df['away_team_id'][game_id]

    def aggregate(self, metrics_definition: dict, print_progress: bool = True):
        unique_games = self.get_unique_games()

        result = []
        index = 0
        for game_id in unique_games:
            if print_progress:
                index += 1
                print(index, '/', len(unique_games))

            game_events_df = self.get_events(game_id)
            home_team_id = self.get_home_team_id(game_id)
            away_team_id = self.get_away_team_id(game_id)

            if home_team_id == away_team_id:
                print("Home team and away team equals for fixture", game_id)
                continue

            result.append(self.aggregate_team_statistics(game_events_df, game_id, home_team_id, metrics_definition))
            result.append(self.aggregate_team_statistics(game_events_df, game_id, away_team_id, metrics_definition))

        result_df = DataFrame(result)
        result_df.set_index(['game_id', 'team_id'], inplace=True)

        return result_df

    def aggregate_team_statistics(
            self,
            events_df: DataFrame,
            game_id: int,
            team_id: int,
            metrics_definition: dict
    ) -> dict:
        data = {
            'game_id': game_id,
            'team_id': team_id,
        }

        for key, value in metrics_definition.items():
            data[key] = self.calculate(events_df, game_id, team_id, value)

        return data

    def calculate(self, events_df: DataFrame, game_id: int, team_id: int, calculate_context: CalculateContext):
        if not self.check_location(calculate_context, game_id, team_id):
            return 0

        home_team_id = self.games_df['home_team_id'][game_id]
        home = home_team_id == team_id

        if calculate_context.calculate_type == CalculateType.DURATION:
            return self.calculate_duration(calculate_context, events_df, game_id, home_team_id, home)

        if calculate_context.calculate_type == CalculateType.GAMES_COUNT:
            return 1

        return self.calculate_shots(calculate_context, events_df, home, team_id)

    @staticmethod
    def is_penalty_shot(event_type):
        return event_type == 'penalty-goal' or event_type == 'penalty-miss'

    @staticmethod
    def is_red_card_event(event_type):
        return event_type == 'red-card'

    @staticmethod
    def is_own_goal_event(event_type):
        return event_type == 'own-goal'

    @staticmethod
    def is_goal_event(event_type):
        return event_type == 'goal' or event_type == 'penalty-goal' or event_type == 'own-goal'

    def calculate_duration(self, calculate_context: CalculateContext, events_df: DataFrame, game_id: int,
                           home_team_id: int, home: bool):
        result = 0

        first_half_duration = self.games_df['duration_first_half'][game_id]
        second_half_duration = self.games_df['duration_second_half'][game_id]

        first_half_events_df = events_df.loc[events_df['minute'] <= self.HALF_DURATION].copy().reset_index()
        second_half_events_df = events_df.loc[events_df['minute'] > self.HALF_DURATION].copy().reset_index()

        first_half_events_df = self.append_last_evnet_for_duration(first_half_events_df, home_team_id,
                                                                   self.HALF_DURATION, first_half_duration)

        second_half_events_df = self.append_last_evnet_for_duration(second_half_events_df, home_team_id,
                                                                    self.GAME_DURATION, second_half_duration)

        duration, finish = self.calculate_partial_duration(calculate_context, first_half_events_df, home, 0)

        if calculate_context.first_half:
            result += duration

        duration, finish = self.calculate_partial_duration(calculate_context, second_half_events_df, home,
                                                           self.HALF_DURATION, finish)

        if calculate_context.second_half:
            result += duration

        return result

    def calculate_shots(self, calculate_context: CalculateContext, events_df: DataFrame, home: bool, team_id: int):
        result = 0

        for index in events_df.index:
            if calculate_context.finish_on_red_card and self.is_red_card_event(events_df['type'][index]):
                break

            if calculate_context.skip_penalties and self.is_penalty_shot(events_df['type'][index]):
                continue

            if not self.check_home_team_goals(calculate_context, events_df['home_score'][index]):
                continue

            if calculate_context.minute_from is not None or calculate_context.minute_to is not None:
                minute = events_df['minute'][index]

                if calculate_context.minute_from is not None and minute < calculate_context.minute_from:
                    continue

                if calculate_context.minute_to is not None and minute > calculate_context.minute_to:
                    continue

            if calculate_context.difference_from is not None or calculate_context.difference_to is not None:
                difference = self.calculate_difference(events_df['home_score'][index], events_df['away_score'][index],
                                                       home)

                if not self.check_difference(calculate_context, difference):
                    continue

            if (events_df['team_id'][index] == team_id and calculate_context.own_shots) or (
                    events_df['team_id'][index] != team_id and not calculate_context.own_shots):
                if calculate_context.calculate_type == CalculateType.EXPECTED_GOALS:
                    if self.is_own_goal_event(events_df['type'][index]):
                        continue

                    if self.is_red_card_event(events_df['type'][index]):
                        continue

                    result += min(events_df['xg'][index], calculate_context.max_value)
                elif calculate_context.calculate_type == CalculateType.GOALS:
                    if not self.is_goal_event(events_df['type'][index]):
                        continue

                    result += 1

                elif calculate_context.calculate_type == CalculateType.SHOTS_COUNT:
                    if self.is_own_goal_event(events_df['type'][index]):
                        continue

                    result += 1

        return self.round(result, calculate_context.precision)

    def calculate_partial_duration(self, calculate_context: CalculateContext, events_df: DataFrame, home: bool,
                                   start: int, finish: bool = False):
        result = 0
        for index in events_df.index:
            if finish:
                return result, True

            current_minute = events_df['minute'][index] + numpy.nan_to_num(events_df['additional_minute'][index])

            if calculate_context.finish_on_red_card and self.is_red_card_event(events_df['type'][index]):
                finish = True

            if calculate_context.minute_from is not None or calculate_context.minute_to is not None:
                minute = events_df['minute'][index]

                if calculate_context.minute_from is not None and minute < calculate_context.minute_from:
                    start = current_minute
                    continue

                if calculate_context.minute_to is not None and minute > calculate_context.minute_to:
                    result += max(0, calculate_context.minute_to - start)
                    break

                if calculate_context.minute_from is not None and start < calculate_context.minute_from:
                    start = calculate_context.minute_from

            if calculate_context.difference_from is not None or calculate_context.difference_to is not None:
                if not self.check_home_team_goals(calculate_context, events_df['home_score'][index]):
                    start = current_minute
                    continue

                difference = self.calculate_difference(events_df['home_score'][index], events_df['away_score'][index],
                                                       home)

                if not self.check_difference(calculate_context, difference):
                    start = current_minute
                    continue

            result += max(0, current_minute - start)
            start = current_minute

        return result, finish

    def append_last_evnet_for_duration(self, events_df, home_team_id, minute, real_duration):
        if len(events_df) == 0:
            return events_df

        last_index = len(events_df) - 1
        home_score = events_df['home_score'][last_index]
        away_score = events_df['away_score'][last_index]

        if self.is_goal_event(events_df['type'][last_index]):
            if events_df['team_id'][last_index] == home_team_id:
                home_score += 1
            else:
                away_score += 1

        return pd.concat([
            events_df,
            DataFrame(
                {
                    'game_id': events_df['game_id'][last_index],
                    'minute': minute,
                    'additional_minute': real_duration - self.HALF_DURATION,
                    'team_id': events_df['team_id'][last_index],
                    'home_score': home_score,
                    'away_score': away_score,
                },
                index=[len(events_df)]
            )
        ])

    def check_location(self, calculate_context: CalculateContext, game_id: int, team_id: int) -> bool:
        if calculate_context.calculate_location == CalculateLocation.HOME:
            return self.games_df['home_team_id'][game_id] == team_id

        if calculate_context.calculate_location == CalculateLocation.AWAY:
            return self.games_df['away_team_id'][game_id] == team_id

        return True

    @staticmethod
    def calculate_difference(home_goals: int, away_goals: int, home_position: bool, addition_difference: int = 0):
        if home_position:
            return home_goals - away_goals + addition_difference

        return away_goals - home_goals - addition_difference

    @staticmethod
    def check_home_team_goals(calculate_context: CalculateContext, home_score):
        if calculate_context.home_team_goals is None:
            return True

        return home_score == calculate_context.home_team_goals

    @staticmethod
    def check_difference(calculate_context: CalculateContext, difference) -> bool:
        if calculate_context.difference_from is not None:
            if difference < calculate_context.difference_from:
                return False

        if calculate_context.difference_to is not None:
            if difference > calculate_context.difference_to:
                return False

        return True

    @staticmethod
    def round(value, precision=None):
        if not precision:
            return value

        return round(value, precision)