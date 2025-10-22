from django.shortcuts import render, redirect
import pandas as pd
from .services.leetcode_data_service import LeetCodeDataService
from .services.visualization_service import VisualizationService
from .views import get_profile_details_from_data


def compare_problem_counts_from_data(user1_data, user2_data, username1, username2):
    """Compare problem counts between two users using pre-fetched data"""
    # Extract data for first user
    data1 = user1_data.get('getUserProfile', {})
    if not data1 or not data1.get('matchedUser'):
        return "<h1>Problem Count Comparison</h1><p>No data available for one or both users</p>"

    # Extract data for second user
    data2 = user2_data.get('getUserProfile', {})
    if not data2 or not data2.get('matchedUser'):
        return "<h1>Problem Count Comparison</h1><p>No data available for one or both users</p>"

    # Process first user's data
    d1_total = data1['allQuestionsCount'][1:]
    d1_solved = data1['matchedUser']['submitStats']['acSubmissionNum'][1:]
    difficulty = ['Easy', 'Medium', 'Hard']

    user1_total = [problem_count['count'] for problem_count in d1_total]
    user1_solved = [problem_count['count'] for problem_count in d1_solved]

    # Process second user's data
    d2_total = data2['allQuestionsCount'][1:]
    d2_solved = data2['matchedUser']['submitStats']['acSubmissionNum'][1:]

    user2_total = [problem_count['count'] for problem_count in d2_total]
    user2_solved = [problem_count['count'] for problem_count in d2_solved]

    # Create dataframes
    df1 = pd.DataFrame({
        "difficulty": difficulty,
        "total": user1_total,
        "accepted": user1_solved
    })

    df2 = pd.DataFrame({
        "difficulty": difficulty,
        "total": user2_total,
        "accepted": user2_solved
    })

    # Generate visualization
    return VisualizationService.create_compare_problems_pie_chart(df1, df2, username1, username2)


def compare_skills_from_data(user1_data, user2_data, username1, username2):
    """Compare skills between two users using pre-fetched data"""
    # Extract data
    data1 = user1_data.get('skillStats', {}).get(
        'matchedUser', {}).get('tagProblemCounts', {})
    data2 = user2_data.get('skillStats', {}).get(
        'matchedUser', {}).get('tagProblemCounts', {})

    problem_types = ['Advanced Algorithms', 'Intermediate Algorithms', 'Fundamental Data-Structure']
    plot_data = "<h1>Problems Solved Comparison</h1>"

    for i, problem_type in enumerate(['advanced', 'intermediate', 'fundamental']):
        plot_data += f"<h2>{problem_types[i]}</h2>"

        # Create dataframes
        df1 = pd.DataFrame(data1.get(problem_type, []))
        df2 = pd.DataFrame(data2.get(problem_type, []))

        if not df1.empty:
            df1.sort_values(by=['problemsSolved'],
                            inplace=True, ascending=False)
            df1.reset_index(drop=True, inplace=True)

        if not df2.empty:
            df2.sort_values(by=['problemsSolved'],
                            inplace=True, ascending=False)
            df2.reset_index(drop=True, inplace=True)

        # Generate visualization
        plot_data += VisualizationService.create_compare_skills_bar_chart(
            df1, df2, username1, username2)

    return plot_data


def compare_contests_from_data(user1_data, user2_data, username1, username2):
    """Compare contest rankings between two users using pre-fetched data"""
    # Extract data
    data1 = user1_data.get('userContestRankingInfo', {})
    data2 = user2_data.get('userContestRankingInfo', {})

    if not data1 or 'userContestRankingHistory' not in data1 or \
       not data2 or 'userContestRankingHistory' not in data2:
        return "<h1>Common Contest Ranking</h1><p>No contest data available for one or both users</p>"

    # Create dataframes
    df1 = pd.DataFrame(data1['userContestRankingHistory'])
    df2 = pd.DataFrame(data2['userContestRankingHistory'])

    if df1.empty or df2.empty:
        return "<h1>Common Contest Ranking</h1><p>No contest history available for one or both users</p>"

    # Filter to attended contests only
    attended1 = df1[df1['attended'] != False].copy()
    attended2 = df2[df2['attended'] != False].copy()

    if attended1.empty or attended2.empty:
        return "<h1>Common Contest Ranking</h1><p>No attended contests found for one or both users</p>"

    # Extract contest titles
    for i in range(len(attended1)):
        attended1.loc[attended1.index[i],
                      'contest'] = attended1.iloc[i]['contest']['title']

    for i in range(len(attended2)):
        attended2.loc[attended2.index[i],
                      'contest'] = attended2.iloc[i]['contest']['title']

    # Find common contests
    common_contests = pd.merge(
        attended1[['ranking', 'contest']],
        attended2[['ranking', 'contest']],
        on=['contest'],
        how='inner'
    )

    if len(common_contests) == 0:
        return "<h1>Common Contest Ranking</h1><p>No common contests found between the users</p>"

    # Generate visualization
    plot_data = "<h1>Common Contest Ranking</h1>"
    plot_data += VisualizationService.create_compare_contest_bar_chart(
        common_contests, username1, username2)

    return plot_data


def comparison_form(request):
    """Display form to compare two LeetCode profiles"""
    if request.method == 'POST':
        username1 = request.POST['username1']
        username2 = request.POST['username2']
        return redirect('comparison_detail', username1=username1, username2=username2)
    return render(request, "compare.html")


def comparison_detail(request, username1, username2):
    """Display detailed comparison between two specific LeetCode profiles"""
    # Check if users exist
    validation1 = LeetCodeDataService.validate_user(username1)
    validation2 = LeetCodeDataService.validate_user(username2)

    if not validation1['valid'] or not validation2['valid']:
        error_messages = []
        if not validation1['valid']:
            error_messages.append(validation1['message'])
        if not validation2['valid']:
            error_messages.append(validation2['message'])

        error_html = '<div class="alert alert-warning" role="alert"><i class="fas fa-exclamation-triangle me-2"></i>'
        error_html += '<br>'.join(error_messages)
        error_html += '</div>'

        return render(request, "compare.html", context={"error": error_html})

    # Fetch all data for both users in a single call
    user_data = LeetCodeDataService.fetch_all_user_data([username1, username2])
    user1_data = user_data[username1]
    user2_data = user_data[username2]

    # Generate user profiles
    user1_details = get_profile_details_from_data(user1_data)
    user2_details = get_profile_details_from_data(user2_data)
    users = [user1_details, user2_details]

    # Generate comparison visualizations
    problem_type_count = compare_problem_counts_from_data(
        user1_data, user2_data, username1, username2)
    skills_comparison = compare_skills_from_data(
        user1_data, user2_data, username1, username2)
    contest_comparison = compare_contests_from_data(
        user1_data, user2_data, username1, username2)

    plots = [problem_type_count, skills_comparison, contest_comparison]

    context = {
        "users": users,
        "plots": plots,
        "username1": username1,
        "username2": username2
    }
    return render(request, "compare.html", context=context)
