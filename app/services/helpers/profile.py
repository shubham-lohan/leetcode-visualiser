import pandas as pd

from app.services.visualization import VisualizationService


def get_accepted_problems_count_from_data(user_data):
    """Create problems count visualization from pre-fetched data"""

    data = user_data.get("getUserProfile", {})
    if not data or not data.get("matchedUser"):
        return None

    d1 = data["allQuestionsCount"][1:]
    d2 = data["matchedUser"]["submitStats"]["acSubmissionNum"][1:]

    if data["matchedUser"]["submitStats"]["acSubmissionNum"][0]["count"] == 0:
        return None

    difficulty = ["Easy", "Medium", "Hard"]
    total_ques_count = [problem_count["count"] for problem_count in d1]
    accepted_ques_count = [problem_count["count"] for problem_count in d2]

    df_problem_count = pd.DataFrame(
        {
            "difficulty": difficulty,
            "total": total_ques_count,
            "accepted": accepted_ques_count,
        }
    )

    df_problem_count["total"] = pd.to_numeric(df_problem_count["total"])
    df_problem_count["accepted"] = pd.to_numeric(df_problem_count["accepted"])

    return VisualizationService.create_problems_pie_chart(df_problem_count)


def get_skills_stats_from_data(user_data):
    """Create skills stats visualization from pre-fetched data"""
    data = (
        user_data.get("skillStats", {})
        .get("matchedUser", {})
        .get("tagProblemCounts", {})
    )

    charts = []
    problem_types = [
        "Advanced Algorithms",
        "Intermediate Algorithms",
        "Fundamental Data-Structure",
    ]
    keys = ["advanced", "intermediate", "fundamental"]

    for i, key in enumerate(keys):
        category_count = data.get(key, [])

        if len(category_count) == 0:
            continue

        problem_count = pd.DataFrame(category_count)
        if "problemsSolved" in problem_count.columns:
            problem_count["problemsSolved"] = pd.to_numeric(
                problem_count["problemsSolved"]
            )

        chart_html = VisualizationService.create_skills_bar_chart(
            problem_count, problem_types[i]
        )
        charts.append({"title": problem_types[i], "chart": chart_html})

    return charts if charts else None


def get_profile_details_from_data(user_data):
    """Get user profile details from pre-fetched data"""
    data = user_data.get("userProfile", {}).get("matchedUser", {})
    return {
        "username": data.get("username", ""),
        "realname": data.get("profile", {}).get("realName", ""),
        "img": data.get("profile", {}).get("userAvatar", ""),
    }


def get_contest_ranking_from_data(user_data):
    """Create contest ranking visualization from pre-fetched data"""
    default_response = {
        "total": 0,
        "best": "N/A",
        "worst": "N/A",
        "chart": "",
        "message": "No contest data available",
    }

    data = user_data.get("userContestRankingInfo", {})
    if not data or "userContestRankingHistory" not in data:
        return default_response

    all_contest_history = pd.DataFrame(data["userContestRankingHistory"])

    if len(all_contest_history) == 0:
        return default_response

    attended_contest = all_contest_history[
        all_contest_history["attended"] != False
    ].copy()
    attended_contest.reset_index(drop=True, inplace=True)

    for i in range(len(attended_contest)):
        contest_val = attended_contest.iloc[i]["contest"]
        if isinstance(contest_val, dict):
            attended_contest.at[i, "contest"] = contest_val["title"]
        else:
            attended_contest.at[i, "contest"] = str(contest_val)

    attended_contest["ranking"] = pd.to_numeric(attended_contest["ranking"])

    if len(attended_contest) == 0:
        return default_response

    chart_html = VisualizationService.create_contest_bar_chart(attended_contest)

    return {
        "total": len(attended_contest),
        "best": min(attended_contest["ranking"]),
        "worst": max(attended_contest["ranking"]),
        "chart": chart_html,
        "message": "",
    }


def get_language_stats_from_data(user_data):
    """Create language breakdown visualization"""
    data = user_data.get("getUserProfile", {})
    if not data or not data.get("matchedUser"):
        return None

    languages = data["matchedUser"].get("languageProblemCount", [])
    if not languages:
        return None
    return VisualizationService.create_language_pie_chart(languages)
