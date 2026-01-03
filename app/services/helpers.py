import pandas as pd
from app.services.visualization import VisualizationService

# --- Profile Helpers ---

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
    
    # Ensure numeric types
    df_problem_count['total'] = pd.to_numeric(df_problem_count['total'])
    df_problem_count['accepted'] = pd.to_numeric(df_problem_count['accepted'])

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
        # Ensure numeric types
        if 'problemsSolved' in problem_count.columns:
            problem_count['problemsSolved'] = pd.to_numeric(problem_count['problemsSolved'])
            
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

    attended_contest = all_contest_history[all_contest_history['attended'] != False].copy()
    attended_contest.reset_index(drop=True, inplace=True)

    for i in range(len(attended_contest)):
        contest_val = attended_contest.iloc[i]['contest']
        if isinstance(contest_val, dict):
            attended_contest.at[i, 'contest'] = contest_val['title']
        else:
             attended_contest.at[i, 'contest'] = str(contest_val)

    # Ensure numeric types for ranking
    attended_contest['ranking'] = pd.to_numeric(attended_contest['ranking'])

    plot_data = "<h1>Attended Contests History</h1>"
    plot_data += f"<p>Total attended contests: {len(attended_contest)}</p>"

    if len(attended_contest):
        plot_data += f"<p>Best Rank: {min(attended_contest['ranking'])}<br>Worst Rank: {max(attended_contest['ranking'])}</p>"
        plot_data += VisualizationService.create_contest_bar_chart(
            attended_contest)

    return plot_data


# --- Comparison Helpers ---

def compare_problem_counts_from_data(user1_data, user2_data, username1, username2):
    """Compare problem counts between two users using pre-fetched data"""
    data1 = user1_data.get('getUserProfile', {})
    if not data1 or not data1.get('matchedUser'):
        return "<h1>Problem Count Comparison</h1><p>No data available for one or both users</p>"

    data2 = user2_data.get('getUserProfile', {})
    if not data2 or not data2.get('matchedUser'):
        return "<h1>Problem Count Comparison</h1><p>No data available for one or both users</p>"

    d1_solved = data1['matchedUser']['submitStats']['acSubmissionNum'][1:]
    d2_solved = data2['matchedUser']['submitStats']['acSubmissionNum'][1:]
    difficulty = ['Easy', 'Medium', 'Hard']

    user1_solved = [problem_count['count'] for problem_count in d1_solved]
    user2_solved = [problem_count['count'] for problem_count in d2_solved]

    df1 = pd.DataFrame({
        "difficulty": difficulty,
        "accepted": user1_solved
    })

    df2 = pd.DataFrame({
        "difficulty": difficulty,
        "accepted": user2_solved
    })

    return VisualizationService.create_compare_problems_pie_chart(df1, df2, username1, username2)


def compare_skills_from_data(user1_data, user2_data, username1, username2):
    """Compare skills between two users using pre-fetched data"""
    data1 = user1_data.get('skillStats', {}).get(
        'matchedUser', {}).get('tagProblemCounts', {})
    data2 = user2_data.get('skillStats', {}).get(
        'matchedUser', {}).get('tagProblemCounts', {})

    problem_types = ['Advanced Algorithms', 'Intermediate Algorithms', 'Fundamental Data-Structure']
    plot_data = "<h1>Problems Solved Comparison</h1>"

    for i, problem_type in enumerate(['advanced', 'intermediate', 'fundamental']):
        plot_data += f"<h2>{problem_types[i]}</h2>"

        df1 = pd.DataFrame(data1.get(problem_type, []))
        df2 = pd.DataFrame(data2.get(problem_type, []))

        if not df1.empty:
            df1.sort_values(by=['problemsSolved'], inplace=True, ascending=False)
            df1.reset_index(drop=True, inplace=True)

        if not df2.empty:
            df2.sort_values(by=['problemsSolved'], inplace=True, ascending=False)
            df2.reset_index(drop=True, inplace=True)

        plot_data += VisualizationService.create_compare_skills_bar_chart(
            df1, df2, username1, username2)

    return plot_data


def compare_contests_from_data(user1_data, user2_data, username1, username2):
    """Compare contest rankings between two users using pre-fetched data"""
    data1 = user1_data.get('userContestRankingInfo', {})
    data2 = user2_data.get('userContestRankingInfo', {})

    if not data1 or 'userContestRankingHistory' not in data1 or \
       not data2 or 'userContestRankingHistory' not in data2:
        return "<h1>Common Contest Ranking</h1><p>No contest data available for one or both users</p>"

    df1 = pd.DataFrame(data1['userContestRankingHistory'])
    df2 = pd.DataFrame(data2['userContestRankingHistory'])

    if df1.empty or df2.empty:
        return "<h1>Common Contest Ranking</h1><p>No contest history available for one or both users</p>"

    attended1 = df1[df1['attended'] != False].copy()
    attended2 = df2[df2['attended'] != False].copy()

    if attended1.empty or attended2.empty:
        return "<h1>Common Contest Ranking</h1><p>No attended contests found for one or both users</p>"

    for i in range(len(attended1)):
        attended1.iloc[i, -1] = attended1.iloc[i]['contest']['title']

    for i in range(len(attended2)):
        attended2.iloc[i, -1] = attended2.iloc[i]['contest']['title']
    
    # Rename for merge
    attended1['contest'] = attended1.iloc[:, -1]
    attended2['contest'] = attended2.iloc[:, -1]

    common_contests = pd.merge(
        attended1[['ranking', 'contest']],
        attended2[['ranking', 'contest']],
        on=['contest'],
        how='inner'
    )

    if len(common_contests) == 0:
        return "<h1>Common Contest Ranking</h1><p>No common contests found between the users</p>"

    plot_data = "<h1>Common Contest Ranking</h1>"
    plot_data += VisualizationService.create_compare_contest_bar_chart(
        common_contests, username1, username2)

    return plot_data
