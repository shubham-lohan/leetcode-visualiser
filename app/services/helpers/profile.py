import pandas as pd

from app.services.visualization import VisualizationService


def get_accepted_problems_count_from_data(user_data):
    """Return chart data dict for problems by difficulty"""
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

    return VisualizationService.create_problems_chart_data(df_problem_count)


def get_skills_stats_from_data(user_data):
    """Return list of chart data dicts for skill categories"""
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

        chart_data = VisualizationService.create_skills_chart_data(
            problem_count, problem_types[i]
        )
        if chart_data:
            charts.append(chart_data)

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
    """Return contest ranking chart data + summary stats"""
    default_response = {
        "total": 0,
        "best": "N/A",
        "worst": "N/A",
        "chart": None,
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

    chart_data = VisualizationService.create_contest_chart_data(attended_contest)

    return {
        "total": len(attended_contest),
        "best": int(min(attended_contest["ranking"])),
        "worst": int(max(attended_contest["ranking"])),
        "chart": chart_data,
        "message": "",
    }


def get_language_stats_from_data(user_data):
    """Return chart data dict for language breakdown"""
    data = user_data.get("getUserProfile", {})
    if not data or not data.get("matchedUser"):
        return None

    languages = data["matchedUser"].get("languageProblemCount", [])
    if not languages:
        return None
    return VisualizationService.create_language_chart_data(languages)


def get_stat_cards_from_data(user_data):
    """Extract stat card data: total solved, contest rating, global rank, acceptance rate"""
    stats = {}

    # Total solved
    profile_data = user_data.get("getUserProfile", {})
    if profile_data and profile_data.get("matchedUser"):
        ac_stats = profile_data["matchedUser"]["submitStats"]["acSubmissionNum"]
        stats["total_solved"] = ac_stats[0]["count"]

        # Acceptance rate
        total_submissions = sum(
            s.get("submissions", 0) for s in ac_stats
        )
        total_accepted = sum(s.get("count", 0) for s in ac_stats)
        if total_submissions > 0:
            stats["acceptance_rate"] = round(
                (total_accepted / total_submissions) * 100, 1
            )
        else:
            stats["acceptance_rate"] = 0

        # Submission calendar for streak (optional extra stat)
        stats["submission_calendar"] = profile_data["matchedUser"].get(
            "submissionCalendar", "{}"
        )
    else:
        stats["total_solved"] = 0
        stats["acceptance_rate"] = 0
        stats["submission_calendar"] = "{}"

    # Contest stats
    contest_data = user_data.get("userContestRankingInfo", {})
    ranking_info = contest_data.get("userContestRanking") if contest_data else None

    if ranking_info:
        stats["contest_rating"] = round(ranking_info.get("rating", 0))
        stats["global_ranking"] = ranking_info.get("globalRanking", "N/A")
        stats["top_percentage"] = round(ranking_info.get("topPercentage", 0), 1)
        stats["contests_attended"] = ranking_info.get("attendedContestsCount", 0)
    else:
        stats["contest_rating"] = 0
        stats["global_ranking"] = "N/A"
        stats["top_percentage"] = 0
        stats["contests_attended"] = 0

    return stats


def get_badges_from_data(user_data):
    """Return list of badge dicts from user data"""
    data = user_data.get("userBadges", {})
    if not data or not data.get("matchedUser"):
        return []

    badges_raw = data["matchedUser"].get("badges", [])
    badges = []
    for b in badges_raw:
        badge = {
            "id": b.get("id"),
            "name": b.get("displayName", b.get("name", "")),
            "icon": b.get("icon", ""),
            "hover_text": b.get("hoverText", ""),
            "creation_date": b.get("creationDate", ""),
        }
        # Prefer animated GIF if available
        medal = b.get("medal")
        if medal and medal.get("config"):
            gif = medal["config"].get("iconGif")
            if gif:
                badge["icon_gif"] = gif
        badges.append(badge)
    return badges
