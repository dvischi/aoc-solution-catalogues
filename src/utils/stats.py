"""Collection of statistical data structures."""

import numpy as np
from scipy import stats


class DifficultyLevelBinner:
    """Helper class for binning difficulty levels of an AOC year."""
    # pylint: disable=R0903
    part1_completion_counts = None
    part2_completion_counts = None

    difficulty_levels = None
    difficulty_level_bins = None
    difficulty_level_ranges = None

    def __init__(
        self, gold_stars, silver_stars,
        difficulty_levels=None,
        difficulty_weights=None,
        prediction_interval=90  # consider 10% of the values as outliers
                                # = 100% - prediction interval
    ):
        # pylint: disable=R0913
        gold_stars = np.array(gold_stars)
        silver_stars = np.array(silver_stars)

        self.difficulty_levels = difficulty_levels or [
            "Very Easy", "Easy", "Normal", "Hard"
        ]
        difficulty_weights = difficulty_weights or [1, 1, 1, 1]

        # exclude day 25 (part 2) which was not a puzzle
        gold_stars = gold_stars[:-1]

        self.part1_completion_counts = np.append(
            gold_stars + silver_stars[:-1], silver_stars[-1]
        )
        self.part2_completion_counts = gold_stars

        # array with all completion counts for every puzzle (part1 and part2)
        all_completion_counts = np.array(
            (*self.part1_completion_counts, *self.part2_completion_counts)
        )

        self.all_cleaned_completion_counts = self._remove_outliers(
            all_completion_counts, prediction_interval
        )

        self.difficulty_level_bins = self._bin_values(
            self.all_cleaned_completion_counts, difficulty_weights
        )

        self.difficulty_level_ranges = {}
        for difficulty_level, difficulty_level_bin in zip(
            self.difficulty_levels, self.difficulty_level_bins
        ):
            self.difficulty_level_ranges[difficulty_level] = (
                np.min(difficulty_level_bin), np.max(difficulty_level_bin)
            )

    def _remove_outliers(self, values, prediction_interval):
        """
        Remove values outside a prediction interval.

        ref.: https://en.wikipedia.org/wiki/68-95-99.7_rule
        prediction_interval = (1-(1-stats.norm.cdf(z, mean, std_dev)) * 2)
        with mean=0, std_dev=1

        example: (1-(1-stats.norm.cdf([1, 2, 3], 0, 1)) * 2) ==
                     [0.68268949, 0.95449974, 0.9973002]
        """
        z_score_threshold = 0
        for z_score_threshold in np.arange(0, 5, 0.01):
            if (
                (1-(1-stats.norm.cdf(z_score_threshold, 0, 1)) * 2) >
                prediction_interval / 100
            ):
                break

        zscores = stats.zscore(values)
        values = values[np.abs(zscores) < z_score_threshold]
        return values

    def _bin_values(self, values, weights):
        """Bin values with weights."""
        values = np.sort(values)[::-1]
        # bin values
        _, _, bin_indices = stats.binned_statistic(
            range(len(values)), values, 'mean', bins=sum(weights)
        )

        # apply difficulty weights
        weighted_bin_indices = np.zeros(bin_indices.shape)
        weight_sum = 0
        for difficulty_level_index, difficulty_weight in enumerate(weights):
            weighted_bin_indices[
                (weight_sum < bin_indices) &
                (bin_indices <= weight_sum + difficulty_weight)
            ] = difficulty_level_index + 1
            weight_sum += difficulty_weight

        for difficulty_level_index in range(len(weights)):
            yield values[weighted_bin_indices == difficulty_level_index + 1]

    def get_difficulty_level(self, users_completed_puzzle):
        """
        Get the difficulty level of a puzzle based on the amount of users who
        completed it.
        """
        min_range_value = 0
        for (
            difficulty_level, (min_range_value, max_range_value)
        ) in self.difficulty_level_ranges.items():
            if min_range_value <= users_completed_puzzle <= max_range_value:
                return difficulty_level
        if  min_range_value < users_completed_puzzle:
            return self.difficulty_levels[0]
        return self.difficulty_levels[-1]
