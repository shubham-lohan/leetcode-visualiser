class VisualizationService:

    DIFFICULTY_COLOR_MAP = {
        "Easy": "#00b8a3",
        "Medium": "#ffc01e",
        "Hard": "#ef4743",
    }

    @staticmethod
    def create_problems_chart_data(df):
        """Return JSON data for problem difficulty donut chart"""
        if df.empty:
            return None

        return {
            "labels": list(df["difficulty"]),
            "series": [int(v) for v in df["accepted"]],
            "totals": [int(v) for v in df["total"]],
            "colors": [
                VisualizationService.DIFFICULTY_COLOR_MAP.get(d, "#888")
                for d in df["difficulty"]
            ],
        }

    @staticmethod
    def create_skills_chart_data(problem_type_df, problem_type_name):
        """Return JSON data for skills bar chart"""
        if len(problem_type_df) == 0:
            return None

        problem_type_df = problem_type_df.sort_values(
            by=["problemsSolved"], ascending=False
        ).reset_index(drop=True)

        return {
            "title": problem_type_name,
            "categories": list(problem_type_df["tagName"]),
            "series": [int(v) for v in problem_type_df["problemsSolved"]],
        }

    @staticmethod
    def create_contest_chart_data(df):
        """Return JSON data for contest ranking line/bar chart"""
        if len(df) == 0:
            return None

        ratings = [int(round(v)) for v in df.get("rating", [0] * len(df))]
        # Compute rating delta (change from previous contest)
        deltas = [0]  # first contest has no previous
        for i in range(1, len(ratings)):
            deltas.append(ratings[i] - ratings[i - 1])

        return {
            "categories": list(df["contest"]),
            "rankings": [int(v) for v in df["ranking"]],
            "ratings": ratings,
            "rating_deltas": deltas,
        }

    @staticmethod
    def create_language_chart_data(languages):
        """Return JSON data for language pie chart"""
        if not languages:
            return None

        import pandas as pd
        df = pd.DataFrame(languages)

        return {
            "labels": list(df["languageName"]),
            "series": [int(v) for v in df["problemsSolved"]],
        }

    # --- Comparison chart data ---

    @staticmethod
    def create_compare_problems_data(df1, df2, username1, username2):
        """Return JSON data for comparing problem counts"""
        if df1.empty or df2.empty:
            return None

        return {
            "labels": list(df1["difficulty"]),
            "series1": [int(v) for v in df1["accepted"]],
            "series2": [int(v) for v in df2["accepted"]],
            "username1": username1,
            "username2": username2,
            "colors": [
                VisualizationService.DIFFICULTY_COLOR_MAP.get(d, "#888")
                for d in df1["difficulty"]
            ],
        }

    @staticmethod
    def create_compare_skills_data(data1, data2, username1, username2, problem_type_name=None):
        """Return JSON data for comparing skills"""
        x1 = list(data1.get("tagName", []))
        y1 = [int(v) for v in data1.get("problemsSolved", [])]
        x2 = list(data2.get("tagName", []))
        y2 = [int(v) for v in data2.get("problemsSolved", [])]

        return {
            "title": problem_type_name or "Skills Comparison",
            "categories": x1 if len(x1) >= len(x2) else x2,
            "series1": y1,
            "series2": y2,
            "username1": username1,
            "username2": username2,
        }

    @staticmethod
    def create_compare_contest_data(common_contest_df, username1, username2):
        """Return JSON data for comparing contest rankings"""
        if len(common_contest_df) == 0:
            return None

        return {
            "categories": list(common_contest_df.get("contest", [])),
            "rankings1": [int(v) for v in common_contest_df.get("ranking_x", [])],
            "rankings2": [int(v) for v in common_contest_df.get("ranking_y", [])],
            "ratings1": [int(round(v)) for v in common_contest_df.get("rating_x", [])],
            "ratings2": [int(round(v)) for v in common_contest_df.get("rating_y", [])],
            "username1": username1,
            "username2": username2,
        }
