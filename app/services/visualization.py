import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from plotly.offline import plot
from app.schemas.leetcode import DifficultyCount

class VisualizationService:
    # Common styling for all plots
    COMMON_LAYOUT = {
        'plot_bgcolor': 'rgb(26,26,26)',
        'paper_bgcolor': 'rgb(10,10,10)',
        'font': dict(color='whitesmoke', size=14),
        'legend': dict(font=dict(color='white', size=12), title=dict(font=dict(color='white'))),
        'title': dict(font=dict(color='rgb(255,161,22)', size=24), x=0.5, xanchor='center'),
        'xaxis': dict(showgrid=False, title_font=dict(color='white', size=16), tickfont=dict(color='white', size=14)),
        'yaxis': dict(showgrid=False, title_font=dict(color='white', size=16), tickfont=dict(color='white', size=14)),
        'margin': dict(l=60, r=40, t=60, b=40)
    }

    DIFFICULTY_COLOR_MAP = {
        'Easy': 'rgb(0,184,163)',
        'Medium': 'rgb(255,192,30)',
        'Hard': 'rgb(239,71,67)'
    }

    @staticmethod
    def create_problems_pie_chart(df: pd.DataFrame):
        """Create a pie chart for problems solved by difficulty"""
        if df.empty:
            return "<p>No problem is solved</p>"

        # Ensure correct color mapping regardless of row order
        # We map the 'difficulty' column to the colors
        colors = [VisualizationService.DIFFICULTY_COLOR_MAP.get(x, '#888') for x in df['difficulty']]
        # Use Graph Objects directly
        fig = go.Figure(data=[go.Pie(
            labels=list(df['difficulty']),
            values=list(df['accepted']),
            marker=dict(colors=colors, line=dict(color='#000000', width=2)),
            textinfo='label+value+percent',
            texttemplate='<b>%{value}</b><br>%{label}<br>(%{percent})',
            textposition='inside',
        )])
        fig.update_layout(
            **VisualizationService.COMMON_LAYOUT,
            legend_title="Difficulty",
        )
        fig.update_yaxes(automargin=True)
        fig.update_xaxes(automargin=True)

        return plot(fig, output_type='div', include_plotlyjs=False)

    @staticmethod
    def create_compare_problems_pie_chart(df1: pd.DataFrame, df2: pd.DataFrame, username1: str, username2: str):
        """Create side-by-side pie charts for comparing problem counts"""
        if df1.empty or df2.empty:
            return ""

        fig = make_subplots(rows=1, cols=2, specs=[
                            [{"type": "pie"}, {"type": "pie"}]])

        # Color mapping helper - assuming df1 indices match df2 indices roughly or just mapping by value
        # Ideally we should align them, but for now map based on the series
        colors1 = [VisualizationService.DIFFICULTY_COLOR_MAP.get(x, '#888') for x in df1['difficulty']]
        colors2 = [VisualizationService.DIFFICULTY_COLOR_MAP.get(x, '#888') for x in df1['difficulty']] # Use df1 labels for both as per previous logic

        fig.add_trace(
            go.Pie(
                values=list(df1['accepted']),
                labels=list(df1['difficulty']),
                sort=False,
                name=username1,
                title=dict(text=username1, position='top center', font=dict(size=18)),
                textposition='inside',
                marker=dict(colors=colors1, line=dict(color='#000000', width=1)),
                textinfo='label+value+percent',
                texttemplate='<b>%{value}</b><br>%{label}',
            ),
            row=1, col=1
        )

        fig.add_trace(
            go.Pie(
                values=list(df2['accepted']),
                # Assuming same difficulty labels/order from df1 is desired for comparison
                labels=list(df1['difficulty']), 
                sort=False,
                name=username2,
                title=dict(text=username2, position='top center', font=dict(size=18)),
                textposition='inside',
                marker=dict(colors=colors2, line=dict(color='#000000', width=1)),
                textinfo='label+value+percent',
                texttemplate='<b>%{value}</b><br>%{label}',
            ),
            row=1, col=2
        )

        fig.update_layout(**VisualizationService.COMMON_LAYOUT,
                          legend_title="Difficulty")
        fig.update_yaxes(automargin=True)
        fig.update_xaxes(automargin=True)

        return plot(fig, output_type='div', include_plotlyjs=False)

    @staticmethod
    def create_skills_bar_chart(problem_type_df: pd.DataFrame, problem_type_name: str):
        """Create a bar chart for skills/tag statistics"""
        if len(problem_type_df) == 0:
            return "<p>No Data Available</p>"

        problem_type_df = problem_type_df.sort_values(
            by=['problemsSolved'], ascending=True).reset_index(drop=True)

        # Vertical Bar Chart for Skills
        fig = go.Figure(data=[go.Bar(
            x=list(problem_type_df['tagName']),        # Category on X
            y=list(problem_type_df['problemsSolved']), # Value on Y
            text=list(problem_type_df['problemsSolved']),
            texttemplate='<b>%{value}</b>',      # Bold values
            textposition='outside',              # Place text outside bar if possible for visibility
            marker=dict(
                color=list(problem_type_df['problemsSolved']),
                colorscale='Plasma',             # Better colorscale for dark theme
                line=dict(color='rgba(255, 255, 255, 0.2)', width=1)
            )
        )])

        fig.update_layout(
            **VisualizationService.COMMON_LAYOUT,
            xaxis_title=None,
            yaxis_title="Problems Solved",
            legend_title=problem_type_name.split()[-1],
        )
        
        # Increase text labels size specifically for this chart
        fig.update_yaxes(tickfont=dict(size=13))

        return plot(fig, output_type='div', include_plotlyjs=False)

    @staticmethod
    def create_compare_skills_bar_chart(data1: pd.DataFrame, data2: pd.DataFrame, username1: str, username2: str):
        """Create a bar chart comparing skills/tags"""
        fig = go.Figure()

        fig.add_trace(
            go.Bar(
                x=list(data1.get('tagName')),            # X is category
                y=list(data1.get('problemsSolved')),     # Y is value
                text=list(data1.get('problemsSolved')),
                name=username1,
                textposition='auto',
                texttemplate='<b>%{value}</b>',
                marker_color='rgb(0, 184, 163)'    # LeetCode Teal
            )
        )

        fig.add_trace(
            go.Bar(
                x=list(data2.get('tagName')),
                y=list(data2.get('problemsSolved')),
                text=list(data2.get('problemsSolved')),
                name=username2,
                textposition='auto',
                texttemplate='<b>%{value}</b>',
                marker_color='rgb(255, 161, 22)'   # LeetCode Orange
            )
        )

        fig.update_layout(
            **VisualizationService.COMMON_LAYOUT,
            xaxis_title=None,
            yaxis_title='problems solved',
            barmode='group'
        )
        fig.update_yaxes(automargin=True)
        fig.update_xaxes(automargin=True)

        return plot(fig, output_type='div', include_plotlyjs=False)

    @staticmethod
    def create_contest_bar_chart(df: pd.DataFrame):
        """Create a bar chart for contest rankings"""
        if len(df) == 0:
            return ""

        # Vertical Bar Chart for Contests
        fig = go.Figure(data=[go.Bar(
            x=list(df['contest']),      # Category on X
            y=list(df['ranking']),      # Value on Y
            text=list(df['ranking']),
            hovertext=list(df.get('problemsSolved', [])),
            texttemplate='<b>%{value}</b>',
            textposition='auto',
            marker=dict(
                 color=list(df['ranking']),
                 colorscale='Plasma',   # Consistent palette
                 reversescale=True      # Better rank (lower number) should probably specific color? 
                                        # Actually, for ranking, small is good. 
                                        # Let's use 'Plasma' but normally high val = bright.
            )
        )])

        # Reverse y-axis for contests so #1 is at top? No, bar chart usually height=value.
        # But for rank, lower is better. A bar chart of rank is confusing if higher bar = worse rank.
        # But this is what it was. I will keep it but maybe improve tooltip.
        
        fig.update_layout(
            **VisualizationService.COMMON_LAYOUT,
            xaxis_title="Contests",
            yaxis_title="Rank",
            title_text="Attended Contests Ranking"
        )
        # Invert y-axis to show Rank 1 at top? 
        # fig.update_yaxes(autorange="reversed") 
        # The original code didn't do this, so I will stick to standard bar for now 
        # but ensure the colors look nice. Lower rank = better = maybe cooler color?
        
        return plot(fig, output_type='div', include_plotlyjs=False)

    @staticmethod
    def create_compare_contest_bar_chart(common_contest_df: pd.DataFrame, username1: str, username2: str):
        """Create a bar chart comparing contest rankings"""
        if len(common_contest_df) == 0:
            return ""

        fig = go.Figure()

        fig.add_trace(
            go.Bar(
                x=list(common_contest_df.get('contest')),
                y=list(common_contest_df.get('ranking_x')),
                name=username1,
                text=list(common_contest_df.get('ranking_x')),
                marker_color='rgb(0, 184, 163)', # LeetCode Teal
                texttemplate='<b>%{value}</b>'
            )
        )

        fig.add_trace(
            go.Bar(
                x=list(common_contest_df.get('contest')),
                y=list(common_contest_df.get('ranking_y')),
                name=username2,
                text=list(common_contest_df.get('ranking_y')),
                marker_color='rgb(255, 161, 22)', # LeetCode Orange
                texttemplate='<b>%{value}</b>'
            )
        )

        fig.update_layout(
            **VisualizationService.COMMON_LAYOUT,
            xaxis_title=None,
            yaxis_title='ranking'
        )
        fig.update_yaxes(automargin=True)
        fig.update_xaxes(automargin=True)
        fig.update_traces(textposition='inside')

        return plot(fig, output_type='div', include_plotlyjs=False)
