from django.shortcuts import render, redirect
import pandas as pd
from .services.leetcode_data_service import LeetCodeDataService
from .services.visualization_service import VisualizationService

# Helper functions for processing pre-fetched data
def get_accepted_problems_count_from_data(user_data):
    """Create problems count visualization from pre-fetched data"""
    plot_data = "<h1>Problems Count</h1>"

    data = user_data.get('getUserProfile', {})
    if not data or not data.get('matchedUser'):
        plot_data += "No problem is solved"
        return plot_data

    d1 = data['allQuestionsCount'][1:]
    d2 = data['matchedUser']['submitStats']['acSubmissionNum'][1:]

    if data['matchedUser']['submitStats']['acSubmissionNum'][0]['count'] == 0:
        plot_data += "No problem is solved"
        return plot_data

    difficulty = ['Easy', 'Medium', 'Hard']
    total_ques_count = [problem_count['count'] for problem_count in d1]
    accepted_ques_count = [problem_count['count'] for problem_count in d2]

    df_problem_count = pd.DataFrame({
        "difficulty": difficulty,
        "total": total_ques_count,
        "accepted": accepted_ques_count
    })

    plot_data += VisualizationService.create_problems_pie_chart(
        df_problem_count)
    return plot_data


def get_skills_stats_from_data(user_data):
    """Create skills stats visualization from pre-fetched data"""
    data = user_data.get('skillStats', {}).get(
        'matchedUser', {}).get('tagProblemCounts', {})
    plot_data = "<h1>Problems Solved</h1>"
    problem_types = ['Advanced Algorithms',
                     'Intermediate Algorithms', 'Fundamental Data-Structure']

    for i, problem_type in enumerate(['advanced', 'intermediate', 'fundamental']):
        plot_data += f"<h2>{problem_types[i]}</h2>"
        category_count = data.get(problem_type, [])

        if len(category_count) == 0:
            plot_data += "No Data Available"
            continue

        problem_count = pd.DataFrame(category_count)
        plot_data += VisualizationService.create_skills_bar_chart(
            problem_count, problem_types[i])

    return plot_data


def get_profile_details_from_data(user_data):
    """Get user profile details from pre-fetched data"""
    data = user_data.get('userProfile', {}).get('matchedUser', {})
    return {
        "username": data.get('username', ''),
        "realname": data.get('profile', {}).get('realName', ''),
        'img': data.get('profile', {}).get('userAvatar', '')
    }


def get_contest_ranking_from_data(user_data):
    """Create contest ranking visualization from pre-fetched data"""
    data = user_data.get('userContestRankingInfo', {})
    if not data or 'userContestRankingHistory' not in data:
        return "<h1>Attended Contests History</h1><p>No contest data available</p>"

    all_contest_history = pd.DataFrame(data['userContestRankingHistory'])

    if len(all_contest_history) == 0:
        return "<h1>Attended Contests History</h1><p>No contest data available</p>"

    attended_contest = all_contest_history[all_contest_history['attended'] != False]
    attended_contest.reset_index(drop=True, inplace=True)

    for i in range(len(attended_contest)):
        attended_contest.iloc[i, -1] = attended_contest.iloc[i, -1]['title']

    plot_data = "<h1>Attended Contests History</h1>"
    plot_data += f"<p>Total attended contests: {len(attended_contest)}</p>"

    if len(attended_contest):
        plot_data += f"<p>Best Rank: {min(attended_contest['ranking'])}<br>Worst Rank: {max(attended_contest['ranking'])}</p>"
        plot_data += VisualizationService.create_contest_bar_chart(
            attended_contest)

    return plot_data

def profile_detail(request, username):
    """Display detailed visualization for a specific user profile"""
    if request.method == 'POST':
        username = request.POST['username']
        return redirect('profile_detail', username=username)

    # Check if user exists
    validation = LeetCodeDataService.validate_user(username)
    if not validation['valid']:
        error_message = f'<div class="alert alert-warning" role="alert"><i class="fas fa-exclamation-triangle me-2"></i>{validation["message"]}</div>'
        return render(request, "index.html", context={"error": error_message})

    # Fetch all data in parallel
    user_data = LeetCodeDataService.fetch_all_user_data([username])[username]

    # Generate visualizations
    accepted_problem_count = get_accepted_problems_count_from_data(user_data)
    advanced_problem_count = get_skills_stats_from_data(user_data)
    user_details = get_profile_details_from_data(user_data)
    attended_contest_history = get_contest_ranking_from_data(user_data)

    context = {
        "plots": [accepted_problem_count, attended_contest_history, advanced_problem_count],
        "users": [user_details],
        "username": username
    }
    return render(request, "index.html", context=context)


def profile_form(request):
    """Display form to search for a LeetCode profile"""
    if request.method == 'POST':
        username = request.POST['username']
        return redirect('profile_detail', username=username)
    return render(request, "index.html")
