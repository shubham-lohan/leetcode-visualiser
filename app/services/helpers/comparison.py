import pandas as pd

from app.services.visualization import VisualizationService


def compare_problem_counts_from_data(user1_data, user2_data, username1, username2):
    """Return JSON data for comparing problem counts"""
    data1 = user1_data.get("getUserProfile", {})
    if not data1 or not data1.get("matchedUser"):
        return None

    data2 = user2_data.get("getUserProfile", {})
    if not data2 or not data2.get("matchedUser"):
        return None

    d1_solved = data1["matchedUser"]["submitStats"]["acSubmissionNum"][1:]
    d2_solved = data2["matchedUser"]["submitStats"]["acSubmissionNum"][1:]
    difficulty = ["Easy", "Medium", "Hard"]

    user1_solved = [problem_count["count"] for problem_count in d1_solved]
    user2_solved = [problem_count["count"] for problem_count in d2_solved]

    df1 = pd.DataFrame({"difficulty": difficulty, "accepted": user1_solved})
    df2 = pd.DataFrame({"difficulty": difficulty, "accepted": user2_solved})

    return VisualizationService.create_compare_problems_data(
        df1, df2, username1, username2
    )


def compare_skills_from_data(user1_data, user2_data, username1, username2):
    """Return list of JSON data for comparing skills by category"""
    data1 = (
        user1_data.get("skillStats", {})
        .get("matchedUser", {})
        .get("tagProblemCounts", {})
    )
    data2 = (
        user2_data.get("skillStats", {})
        .get("matchedUser", {})
        .get("tagProblemCounts", {})
    )

    charts = []
    problem_types = [
        "Advanced Algorithms",
        "Intermediate Algorithms",
        "Fundamental Data-Structure",
    ]

    for i, problem_type in enumerate(["advanced", "intermediate", "fundamental"]):
        df1 = pd.DataFrame(data1.get(problem_type, []))
        df2 = pd.DataFrame(data2.get(problem_type, []))

        if not df1.empty:
            df1.sort_values(by=["problemsSolved"], inplace=True, ascending=False)
            df1.reset_index(drop=True, inplace=True)

        if not df2.empty:
            df2.sort_values(by=["problemsSolved"], inplace=True, ascending=False)
            df2.reset_index(drop=True, inplace=True)

        chart_data = VisualizationService.create_compare_skills_data(
            df1, df2, username1, username2, problem_types[i]
        )
        if chart_data:
            charts.append(chart_data)

    return charts if charts else None


def compare_contests_from_data(user1_data, user2_data, username1, username2):
    """Return JSON data for comparing contest rankings"""
    data1 = user1_data.get("userContestRankingInfo", {})
    data2 = user2_data.get("userContestRankingInfo", {})

    if (
        not data1
        or "userContestRankingHistory" not in data1
        or not data2
        or "userContestRankingHistory" not in data2
    ):
        return None

    df1 = pd.DataFrame(data1["userContestRankingHistory"])
    df2 = pd.DataFrame(data2["userContestRankingHistory"])

    if df1.empty or df2.empty:
        return None

    attended1 = df1[df1["attended"] != False].copy()
    attended2 = df2[df2["attended"] != False].copy()

    if attended1.empty or attended2.empty:
        return None

    for i in range(len(attended1)):
        attended1.iloc[i, -1] = attended1.iloc[i]["contest"]["title"]

    for i in range(len(attended2)):
        attended2.iloc[i, -1] = attended2.iloc[i]["contest"]["title"]

    attended1["contest"] = attended1.iloc[:, -1]
    attended2["contest"] = attended2.iloc[:, -1]

    common_contests = pd.merge(
        attended1[["ranking", "rating", "contest"]],
        attended2[["ranking", "rating", "contest"]],
        on=["contest"],
        how="inner",
    )

    if len(common_contests) == 0:
        return None

    return VisualizationService.create_compare_contest_data(
        common_contests, username1, username2
    )
