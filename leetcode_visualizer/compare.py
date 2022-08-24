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
        return "<br>Kindly enter valid usernames"
    label = d1['difficulty']
    fig.add_trace(go.Pie(
        values=d1['accepted'],
        labels=label,
        sort=False,
        name=username1,
        title=username1,
    ),
        row=1, col=1
    )
    fig.add_trace(go.Pie(
        values=d2['accepted'],
        labels=label,
        sort=False,
        name=username2,
        title=username2,
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
        data1.sort_values(by=['problemsSolved'], inplace=True, ascending=False)
        data1.reset_index(drop=True)
        fig = go.Figure()
        fig.add_traces(go.Bar(
            x=data1.get('tagName'),
            y=data1.get('problemsSolved'),
            name=username1
        )
        )
        fig.add_traces(go.Bar(
            x=data2.get('tagName'),
            y=data2.get('problemsSolved'),
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
        )
        fig.update_yaxes(automargin=True)
        fig.update_xaxes(automargin=True)
        plot_data += plot(fig, output_type='div', include_plotlyjs=False)
    return plot_data


def compare_profiles(request):
    if request.method == 'POST':
        username1 = request.POST['username1']
        username2 = request.POST['username2']
        status1 = requests.get(url=f'https://leetcode.com/{username1}').status_code
        status2 = requests.get(url=f'https://leetcode.com/{username2}').status_code
        print(status1, status2)
        if status1 != 200 or status2 != 200:
            return render(request, "compare.html", context={"plots": ['<h1 style="color: yellow;"> User does not exist!'], 'show_input': True})
        user1_details = get_profile_details(username1)
        user2_details = get_profile_details(username2)
        users = [user1_details, user2_details]
        topicwise_problem_count = compare_skill_stats(username1, username2)
        plots = [plot_problem_count(username1, username2), topicwise_problem_count]
        return render(request, "compare.html", context={"users": users, "plots": plots})
    return render(request, "compare.html", context={'show_input': True})
