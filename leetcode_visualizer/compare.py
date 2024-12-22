from .views import *
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def solved_problem_count(username):
    data = get_result(username, operationName='getUserProfile', query=get_query('getUserProfile'))
    d1 = data['allQuestionsCount'][1:]
    d2 = data['matchedUser']['submitStats']['acSubmissionNum'][1:]
    if data['matchedUser']['submitStats']['acSubmissionNum'][0]['count'] == 0:  # all count of the no of ques solved by the user
        return pd.DataFrame()
    difficulty = ['Easy', 'Medium', 'Hard']
    total_ques_count = []
    for problem_count in d1:
        total_ques_count.append(problem_count['count'])
    accepted_ques_count = []
    for problem_count in d2:
        accepted_ques_count.append(problem_count['count'])

    final_data = {
        "difficulty": difficulty,
        "total": total_ques_count,
        "accepted": accepted_ques_count
    }

    df_problem_count = pd.DataFrame(final_data)
    return df_problem_count


def plot_problem_count(username1, username2):
    fig = make_subplots(rows=1, cols=2, specs=[[{"type": "pie"}, {"type": "pie"}]])
    d1 = solved_problem_count(username1)
    d2 = solved_problem_count(username2)
    if len(d1) == 0 or len(d2) == 0:
        return ""
    label = d1['difficulty']
    fig.add_trace(go.Pie(
        values=d1['accepted'],
        labels=label,
        sort=False,
        name=username1,
        title=username1,
        textposition='inside'
    ),
        row=1, col=1
    )
    fig.add_trace(go.Pie(
        values=d2['accepted'],
        labels=label,
        sort=False,
        name=username2,
        title=username2,
        textposition='inside'
    ),
        row=1, col=2)
    fig.update_traces(marker=dict(colors=['rgb(0 ,184 ,163)', 'rgb(255 ,192 ,30)', 'rgb(239 ,71 ,67)']))
    fig.update_layout(
        plot_bgcolor='rgb(26,26,26)',
        paper_bgcolor='rgb(10,10,10)',
        legend_font_color='white',
        font_color='whitesmoke',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False),
        legend_title="Difficulty"
    )
    fig.update_traces(
        textinfo='label+value+percent',
        texttemplate='%{value} %{label}<br>(%{percent})'
    )
    fig.update_yaxes(automargin=True)
    fig.update_xaxes(automargin=True)

    plot_data = plot(fig, output_type='div', include_plotlyjs=False)
    return plot_data


def get_attending_contest(username):
    data = get_result(username, "userContestRankingInfo", get_query("userContestRankingInfo"))
    all_contest_history = pd.DataFrame(data['userContestRankingHistory'])
    attended_contest = all_contest_history[all_contest_history['attended'] != False]
    attended_contest.reset_index(drop=True, inplace=True)
    for i in range(len(attended_contest)):
        attended_contest.iloc[i, -1] = attended_contest.iloc[i, -1]['title']
    return attended_contest[['ranking', 'contest']]


def compare_contest_ranking(username1, username2):
    d1 = get_attending_contest(username1)
    d2 = get_attending_contest(username2)
    plot_data = "<h1>Common Contest Ranking</h1>"
    common_contest = pd.merge(d1, d2, on=['contest'], how='inner')
    if len(common_contest) == 0:
        return ""
    fig = go.Figure()
    fig.add_traces(go.Bar(
        x=common_contest.get('contest'),
        y=common_contest.get('ranking_x'),
        name=username1,
        text=common_contest.get('ranking_x')
    )
    )
    fig.add_traces(go.Bar(
        x=common_contest.get('contest'),
        y=common_contest.get('ranking_y'),
        name=username2,
        text=common_contest.get('ranking_y')
    )
    )
    fig.update_layout(
        plot_bgcolor='rgb(26,26,26)',
        paper_bgcolor='rgb(10,10,10)',
        legend_font_color='white',
        font_color='whitesmoke',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False),
        xaxis_title=None,
        yaxis_title='ranking'
    )
    fig.update_yaxes(automargin=True)
    fig.update_xaxes(automargin=True)
    fig.update_traces(texttemplate='%{text}', textposition='inside')
    plot_data += plot(fig, output_type='div', include_plotlyjs=False)
    return plot_data


def compare_skill_stats(username1, username2):
    d1 = get_result(username1, operationName='skillStats', query=get_query('skillStats'))
    d1 = d1['matchedUser']['tagProblemCounts']
    d2 = get_result(username2, operationName='skillStats', query=get_query('skillStats'))
    d2 = d2['matchedUser']['tagProblemCounts']
    problem_types = ['Advanced Algorithms', 'Intermediate Algorithms', 'Fundamental Data-Structure']
    plot_data = "<h1>Problems Solved</h1>"
    for i, problem_type in enumerate(d1):
        plot_data += f"<h2>{problem_types[i]}</h2>"
        data1 = d1[problem_type]
        data2 = d2[problem_type]
        data1 = pd.DataFrame(data1)
        data2 = pd.DataFrame(data2)
        if len(data1):
            data1.sort_values(by=['problemsSolved'], inplace=True, ascending=False)
            data1.reset_index(drop=True)
        fig = go.Figure()
        fig.add_traces(go.Bar(
            x=data1.get('tagName'),
            y=data1.get('problemsSolved'),
            text=data1.get('problemsSolved'),
            name=username1
        )
        )
        fig.add_traces(go.Bar(
            x=data2.get('tagName'),
            y=data2.get('problemsSolved'),
            text=data2.get('problemsSolved'),
            name=username2,
        )
        )
        fig.update_layout(
            plot_bgcolor='rgb(26,26,26)',
            paper_bgcolor='rgb(10,10,10)',
            legend_font_color='white',
            font_color='whitesmoke',
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=False),
            xaxis_title=None,
            yaxis_title='problems solved',
        )
        fig.update_yaxes(automargin=True)
        fig.update_xaxes(automargin=True)
        fig.update_traces(texttemplate='%{text}', textposition='inside')
        plot_data += plot(fig, output_type='div', include_plotlyjs=False)
    return plot_data


def compare_profiles(request):
    if request.method == 'POST':
        username1 = request.POST['username1']
        username2 = request.POST['username2']
        userPublicProfile1 = get_result(
            username1, operationName='userPublicProfile', query=get_query('userPublicProfile'))
        userPublicProfile2 = get_result(
            username2, operationName='userPublicProfile', query=get_query('userPublicProfile'))
        if userPublicProfile1['matchedUser'] is None or userPublicProfile2['matchedUser'] is None:
            a = username1 if userPublicProfile1['matchedUser'] is None else ""
            b = username2 if userPublicProfile2['matchedUser'] is None else ""
            return render(request, "compare.html", context={"plots": [f'<h1 style="color: yellow;"> {a} {b} does not exist!']})
        user1_details = get_profile_details(username1)
        user2_details = get_profile_details(username2)
        users = [user1_details, user2_details]
        problem_type_count = plot_problem_count(username1, username2)
        topicwise_problem_count = compare_skill_stats(username1, username2)
        common_contests = compare_contest_ranking(username1, username2)
        plots = [problem_type_count, topicwise_problem_count, common_contests]
        return render(request, "compare.html", context={"users": users, "plots": plots})
    return render(request, "compare.html")
