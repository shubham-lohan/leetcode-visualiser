from http.client import HTTPResponse
import requests
from django.shortcuts import render
from plotly.offline import plot
import pandas as pd
import plotly.express as px
pd.options.plotting.backend = "plotly"


def get_result(username, operationName, query):
    payload = {
        "operationName": operationName,
        "variables": {
            "username": username,
        },
        "query": query
    }
    header = {
        "Referer": f"https://leetcode.com/{username}",
        'Content-type': 'application/json'

    }
    data = requests.post(url='https://leetcode.com/graphql', json=payload, headers=header)
    data.raise_for_status()
    return data.json()['data']


def get_accepted_problems_count(username):
    query = """query getUserProfile($username: String!) {
                # allQuestionsCount {difficulty    count}
                matchedUser(username: $username){
                    # contributions {points      questionCount      testcaseCount}
                    # profile {reputation      ranking}
                    submitStats {acSubmissionNum {difficulty        count        submissions}
                    # totalSubmissionNum {difficulty        count        submissions}
                    }
                }
            }
            """
    plot_data = "<h1>Problems Count</h1>"
    data = get_result(username, operationName='getUserProfile', query=query)
    data = data['matchedUser']['submitStats']['acSubmissionNum']
    accepted_problem_count = pd.DataFrame(data[1:])
    color_map = {
        'Easy': 'rgb(0 ,184 ,163)',
        'Medium': 'rgb(255 ,192 ,30)',
        'Hard': 'rgb(239 ,71 ,67)'
    }
    fig = px.bar(accepted_problem_count, x='count', y='difficulty', orientation='h', color='difficulty', color_discrete_map=color_map)
    fig.update_layout(
        plot_bgcolor='rgb(26,26,26)',
        paper_bgcolor='rgb(10,10,10)',
        legend_font_color='white',
        font_color='whitesmoke',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False)
    )
    fig2 = px.pie(accepted_problem_count, values='count', names='difficulty', color='difficulty', color_discrete_map=color_map)
    fig2.update_layout(
        plot_bgcolor='rgb(26,26,26)',
        paper_bgcolor='rgb(10,10,10)',
        legend_font_color='white',
        font_color='whitesmoke',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False),
        xaxis_title=None
    )
    fig2.update_traces(
        textinfo='label+percent',
    )
    fig2.update_yaxes(automargin=True)
    fig2.update_xaxes(automargin=True)
    plot_data += plot(fig, output_type='div', include_plotlyjs=False)
    plot_data += plot(fig2, output_type='div', include_plotlyjs=False)
    return plot_data


def get_skills_stats(username):
    query = """query skillStats($username: String!) {
        matchedUser(username: $username) {
            tagProblemCounts {
                advanced {
                    tagName
                    problemsSolved
                }
                intermediate {
                    tagName
                    problemsSolved
                }
                fundamental {
                    tagName
                    problemsSolved
                }
            }
        }
    }"""
    data = get_result(username, operationName='skillStats', query=query)
    data = data['matchedUser']['tagProblemCounts']
    plot_data = "<h1>Problems Solved</h1>"
    problem_types = ['Advanced Algorithms', 'Intermediate Algorithms', 'Fundamental Data-Structure']
    for i, problem_type in enumerate(data):
        category_count = data[problem_type]
        problem_count = pd.DataFrame(category_count)
        problem_count.sort_values(by=['problemsSolved'], inplace=True, ascending=False)
        problem_count.reset_index(drop=True)
        fig = problem_count.plot(y='problemsSolved', x='tagName', kind='bar', color='tagName')
        fig.update_layout(
            plot_bgcolor='rgb(26,26,26)',
            paper_bgcolor='rgb(10,10,10)',
            legend_font_color='white',
            font_color='whitesmoke',
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=False),
            xaxis_title=None
        )
        plot_data += f"<h2>{problem_types[i]}</h2>"
        plot_data += plot(fig, output_type='div', include_plotlyjs=False)
    return plot_data


def get_profile_details(username):
    query = """
    query userProfile($username: String!) {
      matchedUser(username: $username) {
        username
        profile {
          ranking
          userAvatar
          realName
        }
      }
    }
    """
    data = get_result(username, operationName='userProfile', query=query)
    data = data['matchedUser']
    user_details = {
        "username": data['username'],
        "realname": data['profile']['realName'],
        'img': data['profile']['userAvatar']
    }
    return user_details


def index(request):
    context = {}
    if request.method == 'POST':
        username = request.POST['username']
        status = requests.get(url=f'https://leetcode.com/{username}').status_code
        if status != 200:
            return render(request, "index.html", context={"plots": ['<h1 style="color: yellow;"> User does not exists']})
        accepted_problem_count = get_accepted_problems_count(username)
        advanced_problem_count = get_skills_stats(username)
        user_details = get_profile_details(username)
        context = {"plots": [accepted_problem_count, advanced_problem_count], "user": user_details}
    return render(request, "index.html", context=context)
