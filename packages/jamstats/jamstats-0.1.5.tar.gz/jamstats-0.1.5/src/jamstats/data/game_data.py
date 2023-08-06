__author__ = "Damon May"

from typing import Dict
import pandas as pd
from abc import ABC, abstractmethod


class DerbyGame:
    """Class for storing all the data related to a derby game.
    """
    def __init__(self, pdf_jams_data: pd.DataFrame, game_data_dict: Dict[str, str],
                 pdf_penalties: pd.DataFrame):
        self.pdf_jams_data = pdf_jams_data
        self.game_data_dict = game_data_dict
        self.team_1_name = game_data_dict["team_1"]
        self.team_2_name = game_data_dict["team_2"]
        self.game_summary_dict = self.extract_game_summary_dict()
        self.n_jams = self.game_summary_dict["Jams"]
        self.pdf_penalties = pdf_penalties

    def extract_game_summary(self) -> pd.DataFrame:
        """Build a gross game-summary dataframe

        Returns:
            pd.DataFrame: game summary dataframe
        """
        gross_summary_dict = self.extract_game_summary_dict()
        pdf_game_summary = pd.DataFrame({
            "Statistic": gross_summary_dict.keys(),
            "Value": gross_summary_dict.values()})

        return pdf_game_summary

    def extract_game_summary_dict(self) -> pd.DataFrame:
        """Build a gross game-summary dictionary

        Returns:
            pd.DataFrame: game summary dataframe
        """
        n_periods = len(set([x for x in self.pdf_jams_data.PeriodNumber if x > 0]))
        n_jams = len(self.pdf_jams_data.prd_jam)  # is this correct? Is jam 0 a real jam?
        period_duration_seconds = max(self.pdf_jams_data.jam_endtime_seconds)
        period_duration_minutes = period_duration_seconds / 60
        final_score_team_1 = max(self.pdf_jams_data.TotalScore_1)
        final_score_team_2 = max(self.pdf_jams_data.TotalScore_2)

        gross_summary_dict = {
            "Periods": n_periods,
            "Jams": n_jams,
            "Minutes": period_duration_minutes,
            f"{self.team_1_name} Final Score": final_score_team_1,
            f"{self.team_2_name} Final Score": final_score_team_2,
        }
        return gross_summary_dict

    def extract_game_teams_summary(self) -> pd.DataFrame:
        """Build a summary dataframe with per-team data

        Args:
            pdf_jams_data (pd.DataFrame): jams data

        Returns:
            pd.DataFrame: teams summary dataframe
        """
        cols_to_sum = ["Lead", "Lost", "Calloff", "Injury", "NoInitial",
                       "StarPass"]
        teams_summary_dict = {"Team": [self.team_1_name, self.team_2_name, "sum"]}
        for col in cols_to_sum:
            sum_1 = sum(self.pdf_jams_data[col + "_1"])
            sum_2 = sum(self.pdf_jams_data[col + "_2"])
            sum_both = sum_1 + sum_2
            teams_summary_dict[col] = [sum_1, sum_2, sum_both]
            
        pdf_game_teams_summary = pd.DataFrame(teams_summary_dict)
        return pdf_game_teams_summary

    def build_jams_dataframe_long(self) -> pd.DataFrame:
        """Transform game data into a dataframe with one row per (jam, team),
        which is more useful for some types of plots.

        Returns:
            pd.DataFrame: dataframe with one row per (jam, team)
        """
        cols_repeated_byteam = [x for x in self.pdf_jams_data.columns
                                if x.endswith("_1")]
        cols_repeated_byteam = [x[:-2] for x in cols_repeated_byteam]
        pdf_repeatedcols_team1 = (
            self.pdf_jams_data[["prd_jam", "PeriodNumber"] +
            [x + "_1" for x in cols_repeated_byteam]].copy())
        pdf_repeatedcols_team1["team"] = self.team_1_name
        pdf_repeatedcols_team1 = pdf_repeatedcols_team1.rename(
            columns={x + "_1": x for x in cols_repeated_byteam})
        pdf_repeatedcols_team2 = self.pdf_jams_data[
            ["prd_jam", "PeriodNumber"] +
            [x + "_2" for x in cols_repeated_byteam]].copy()
        pdf_repeatedcols_team2["team"] = self.team_2_name
        pdf_repeatedcols_team2 = pdf_repeatedcols_team2.rename(
            columns={x + "_2": x for x in cols_repeated_byteam})

        pdf_jam_data_long = pd.concat([pdf_repeatedcols_team1, pdf_repeatedcols_team2])
        return pdf_jam_data_long

    def build_team_jammersummary_df(self, team_number: int):
        """Build a dataframe with data on all the jammers for a team.

        Args:
            team_number (int): Team number
        """
        jammer_col = f"jammer_name_{team_number}"
        jamscore_col = f"JamScore_{team_number}"
        netpoints_col = f"net_points_{team_number}"
        lead_col = f"Lead_{team_number}"
        time_to_initial_col = f"first_scoring_pass_durations_{team_number}"

        pdf_jammer_data = self.pdf_jams_data.groupby(jammer_col).agg({
            jamscore_col: "sum",
            netpoints_col: "mean",
            'Number': "count",
            lead_col: "mean",
            time_to_initial_col: "mean"}).reset_index()

        pdf_jammer_data = pdf_jammer_data.rename(columns={
            jammer_col: "Jammer",
            jamscore_col: "Total Score",
            netpoints_col: "Mean Net Points",
            lead_col: "Proportion Lead",
            "Number": "Jams",
            time_to_initial_col: "Mean Time to Initial",
        })
        return pdf_jammer_data