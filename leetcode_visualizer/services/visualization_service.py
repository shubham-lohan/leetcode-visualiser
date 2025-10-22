import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from plotly.offline import plot


class VisualizationService:
    # Common styling for all plots
    COMMON_LAYOUT = {
        'plot_bgcolor': 'rgb(26,26,26)',
        'paper_bgcolor': 'rgb(10,10,10)',
        'legend_font_color': 'white',
        'font_color': 'whitesmoke',
        'title_font_color': 'rgb(255,161,22)',  # LeetCode accent color
        'xaxis': dict(showgrid=False, title_font_color='white', tickfont_color='white'),
        'yaxis': dict(showgrid=False, title_font_color='white', tickfont_color='white'),
    }

    DIFFICULTY_COLOR_MAP = {
        'Easy': 'rgb(0,184,163)',
        'Medium': 'rgb(255,192,30)',
        'Hard': 'rgb(239,71,67)'
    }

    @staticmethod
    def create_problems_pie_chart(df):
        """Create a pie chart for problems solved by difficulty"""
        if df.empty:
            return "<p>No problem is solved</p>"

        fig = px.pie(
            df,
            values='accepted',
            names='difficulty',
            color='difficulty',
            color_discrete_map=VisualizationService.DIFFICULTY_COLOR_MAP,
            labels={'difficulty': "Difficulty"}
        )

        fig.update_layout(
            **VisualizationService.COMMON_LAYOUT,
            legend_title="Difficulty",
            title_font_size=22,
            font_size=14
        )
        fig.update_traces(
            textinfo='label+value+percent',
            texttemplate='%{value} %{label}<br>(%{percent})'
        )
        fig.update_yaxes(automargin=True)
        fig.update_xaxes(automargin=True)

        return plot(fig, output_type='div', include_plotlyjs=False)

    @staticmethod
    def create_compare_problems_pie_chart(df1, df2, username1, username2):
        """Create side-by-side pie charts for comparing problem counts"""
        if df1.empty or df2.empty:
            return ""

        fig = make_subplots(rows=1, cols=2, specs=[
                            [{"type": "pie"}, {"type": "pie"}]])

        label = df1['difficulty']
        fig.add_trace(
            go.Pie(
                values=df1['accepted'],
                labels=label,
                sort=False,
                name=username1,
                title=username1,
                textposition='inside'
            ),
            row=1, col=1
        )

        fig.add_trace(
            go.Pie(
                values=df2['accepted'],
                labels=label,
                sort=False,
                name=username2,
                title=username2,
                textposition='inside'
            ),
            row=1, col=2
        )

        colors = list(VisualizationService.DIFFICULTY_COLOR_MAP.values())
        fig.update_traces(marker=dict(colors=colors))
        fig.update_layout(**VisualizationService.COMMON_LAYOUT,
                          legend_title="Difficulty")
        fig.update_traces(
            textinfo='label+value+percent',
            texttemplate='%{value} %{label}<br>(%{percent})'
        )
        fig.update_yaxes(automargin=True)
        fig.update_xaxes(automargin=True)

        return plot(fig, output_type='div', include_plotlyjs=False)

    @staticmethod
    def create_skills_bar_chart(problem_type_df, problem_type_name):
        """Create a bar chart for skills/tag statistics"""
        if len(problem_type_df) == 0:
            return "<p>No Data Available</p>"

        problem_type_df.sort_values(
            by=['problemsSolved'], inplace=True, ascending=False)
        problem_type_df.reset_index(drop=True)

        fig = px.bar(
            problem_type_df,
            y='problemsSolved',
            x='tagName',
            color='tagName',
            labels={'tagName': problem_type_name.split()[-1]},
            text='problemsSolved'
        )

        fig.update_layout(
            **VisualizationService.COMMON_LAYOUT,
            xaxis_title=None,
            legend_title=problem_type_name.split()[-1]
        )

        return plot(fig, output_type='div', include_plotlyjs=False)

    @staticmethod
    def create_compare_skills_bar_chart(data1, data2, username1, username2):
        """Create a bar chart comparing skills/tags"""
        fig = go.Figure()

        fig.add_trace(
            go.Bar(
                x=data1.get('tagName'),
                y=data1.get('problemsSolved'),
                text=data1.get('problemsSolved'),
                name=username1
            )
        )

        fig.add_trace(
            go.Bar(
                x=data2.get('tagName'),
                y=data2.get('problemsSolved'),
                text=data2.get('problemsSolved'),
                name=username2,
            )
        )

        fig.update_layout(
            **VisualizationService.COMMON_LAYOUT,
            xaxis_title=None,
            yaxis_title='problems solved',
        )
        fig.update_yaxes(automargin=True)
        fig.update_xaxes(automargin=True)
        fig.update_traces(texttemplate='%{text}', textposition='inside')

        return plot(fig, output_type='div', include_plotlyjs=False)

    @staticmethod
    def create_contest_bar_chart(df):
        """Create a bar chart for contest rankings"""
        if len(df) == 0:
            return ""

        fig = px.bar(
            df,
            y='ranking',
            x='contest',
            color='contest',
            text='ranking',
            hover_data=["problemsSolved"]
        )

        fig.update_layout(
            **VisualizationService.COMMON_LAYOUT,
            xaxis_title="Contests",
            yaxis_title="Rank",
            legend_title="Attended Contest",
        )

        return plot(fig, output_type='div', include_plotlyjs=False)

    @staticmethod
    def create_compare_contest_bar_chart(common_contest_df, username1, username2):
        """Create a bar chart comparing contest rankings"""
        if len(common_contest_df) == 0:
            return ""

        fig = go.Figure()

        fig.add_trace(
            go.Bar(
                x=common_contest_df.get('contest'),
                y=common_contest_df.get('ranking_x'),
                name=username1,
                text=common_contest_df.get('ranking_x')
            )
        )

        fig.add_trace(
            go.Bar(
                x=common_contest_df.get('contest'),
                y=common_contest_df.get('ranking_y'),
                name=username2,
                text=common_contest_df.get('ranking_y')
            )
        )

        fig.update_layout(
            **VisualizationService.COMMON_LAYOUT,
            xaxis_title=None,
            yaxis_title='ranking'
        )
        fig.update_yaxes(automargin=True)
        fig.update_xaxes(automargin=True)
        fig.update_traces(texttemplate='%{text}', textposition='inside')

        return plot(fig, output_type='div', include_plotlyjs=False)
