from .utils import get_result
from django.shortcuts import render, redirect
from plotly.offline import plot
import pandas as pd
import plotly.express as px
from django.http import HttpResponse
pd.options.plotting.backend = "plotly"

def get_accepted_problems_count(username):
    plot_data = "<h1>Problems Count</h1>"
    data = get_result(username, operation_name='getUserProfile')
    d1 = data['allQuestionsCount'][1:]
    d2 = data['matchedUser']['submitStats']['acSubmissionNum'][1:]
    if data['matchedUser']['submitStats']['acSubmissionNum'][0]['count'] == 0:  # all count of the no of ques solved by the user
        plot_data += "No problem is solved"
        return plot_data
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
    color_map = {
        'Easy': 'rgb(0 ,184 ,163)',
        'Medium': 'rgb(255 ,192 ,30)',
        'Hard': 'rgb(239 ,71 ,67)'
    }
    fig = px.pie(df_problem_count,
                 values='accepted',
                 names='difficulty',
                 color='difficulty',
                 color_discrete_map=color_map,
                 labels={'difficulty': "Difficulty"}
                 )
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
    plot_data += plot(fig, output_type='div', include_plotlyjs=False)
    return plot_data


def get_skills_stats(username):
    data = get_result(username, operation_name='skillStats')
    data = data['matchedUser']['tagProblemCounts']
    plot_data = "<h1>Problems Solved</h1>"
    problem_types = ['Advanced Algorithms', 'Intermediate Algorithms', 'Fundamental Data-Structure']
    for i, problem_type in enumerate(data):
        plot_data += f"<h2>{problem_types[i]}</h2>"
        category_count = data[problem_type]
        if len(category_count) == 0:
            plot_data += "No Data Available"
            continue
        problem_count = pd.DataFrame(category_count)
        problem_count.sort_values(by=['problemsSolved'], inplace=True, ascending=False)
        problem_count.reset_index(drop=True)
        fig = px.bar(problem_count,
                     y='problemsSolved',
                     x='tagName', color='tagName',
                     labels={'tagName': problem_types[i].split()[-1]},
                     text='problemsSolved'
                     )
        fig.update_layout(
            plot_bgcolor='rgb(26,26,26)',
            paper_bgcolor='rgb(10,10,10)',
            legend_font_color='white',
            font_color='whitesmoke',
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=False),
            xaxis_title=None,
            legend_title=problem_types[i].split()[-1]
        )
        plot_data += plot(fig, output_type='div', include_plotlyjs=False)
    return plot_data


def get_profile_details(username):
    data = get_result(username, operation_name='userProfile')
    data = data['matchedUser']
    user_details = {
        "username": data['username'],
        "realname": data['profile']['realName'],
        'img': data['profile']['userAvatar']
    }
    return user_details


def get_contest_ranking(username):
    data = get_result(username, "userContestRankingInfo")
    all_contest_history = pd.DataFrame(data['userContestRankingHistory'])
    attended_contest = all_contest_history[all_contest_history['attended'] != False]
    # attended_contest['contest'] = attended_contest['contest'].apply(lambda x: x['title'])
    attended_contest.reset_index(drop=True, inplace=True)
    for i in range(len(attended_contest)):
        attended_contest.iloc[i, -1] = attended_contest.iloc[i, -1]['title']
    fig = px.bar(attended_contest, y='ranking', x='contest', color='contest', text='ranking', hover_data=["problemsSolved"])
    fig.update_layout(
        plot_bgcolor='rgb(26,26,26)',
        paper_bgcolor='rgb(10,10,10)',
        legend_font_color='white',
        font_color='whitesmoke',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False),
        xaxis_title="Contests",
        yaxis_title="Rank",
        legend_title="Attended Contest",
    )
    plot_data = "<h1>Attended Contests History</h1>"
    plot_data += f"<p>Total attended contests: {len(attended_contest)}</p>"
    if len(attended_contest):
        plot_data += f"<p>Best Rank: {min(attended_contest['ranking'])}<br>Worst Rank: {max(attended_contest['ranking'])}</p>"
        plot_data += plot(fig, output_type='div', include_plotlyjs=False)
    return plot_data

def visualize(request, username):
    if request.method == 'POST':
        username = request.POST['username']
        return redirect(visualize, username)

    userPublicProfile = get_result(username, "userPublicProfile")

    if userPublicProfile['matchedUser'] is None:
        return render(request, "index.html", context={"plots": ['<h1 style="color: yellow;"> User does not exist!']})
    accepted_problem_count = get_accepted_problems_count(username)
    advanced_problem_count = get_skills_stats(username)
    user_details = get_profile_details(username)
    attended_contest_history = get_contest_ranking(username)
    context = {"plots": [accepted_problem_count, attended_contest_history, advanced_problem_count], "users": [user_details]}
    return render(request, "index.html", context=context)


def index(request):
    if request.method == 'POST':
        username = request.POST['username']
        # return visualize(request, username)
        return redirect(visualize, username)
    return render(request, "index.html")
