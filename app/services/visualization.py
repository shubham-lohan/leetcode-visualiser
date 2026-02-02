import pandas as pd
import plotly.graph_objects as go
from plotly.offline import plot
from plotly.subplots import make_subplots


class VisualizationService:

    COMMON_LAYOUT = {
        "template": "plotly_dark",
        "legend": dict(font=dict(size=12)),
        "title": dict(
            font=dict(color="rgb(255,161,22)", size=24), x=0.5, xanchor="center", y=0.92
        ),
        "xaxis": dict(title_font=dict(size=16), tickfont=dict(size=14)),
        "yaxis": dict(title_font=dict(size=16), tickfont=dict(size=14)),
        "margin": dict(l=60, r=40, t=100, b=40),
    }

    DIFFICULTY_COLOR_MAP = {
        "Easy": "rgb(0,184,163)",
        "Medium": "rgb(255,192,30)",
        "Hard": "rgb(239,71,67)",
    }

    @staticmethod
    def create_problems_pie_chart(df: pd.DataFrame):
        """Create a pie chart for problems solved by difficulty"""
        if df.empty:
            return "<p>No problem is solved</p>"

        # Ensure correct color mapping regardless of row order
        colors = [
            VisualizationService.DIFFICULTY_COLOR_MAP.get(x, "#888")
            for x in df["difficulty"]
        ]

        fig = go.Figure(
            data=[
                go.Pie(
                    labels=list(df["difficulty"]),
                    values=list(df["accepted"]),
                    marker=dict(colors=colors, line=dict(color="#000000", width=2)),
                    textinfo="label+value+percent",
                    texttemplate="<b>%{value}</b><br>%{label}<br>(%{percent})",
                )
            ]
        )
        fig.update_layout(
            **VisualizationService.COMMON_LAYOUT,
            legend_title="Difficulty",
            title_text="Problems Count",
        )
        fig.update_yaxes(automargin=True)
        fig.update_xaxes(automargin=True)

        return plot(fig, output_type="div", include_plotlyjs=False)

    @staticmethod
    def create_compare_problems_pie_chart(
        df1: pd.DataFrame, df2: pd.DataFrame, username1: str, username2: str
    ):
        """Create side-by-side pie charts for comparing problem counts"""
        if df1.empty or df2.empty:
            return ""

        fig = make_subplots(rows=1, cols=2, specs=[[{"type": "pie"}, {"type": "pie"}]])

        # Color mapping helper
        colors1 = [
            VisualizationService.DIFFICULTY_COLOR_MAP.get(x, "#888")
            for x in df1["difficulty"]
        ]
        colors2 = [
            VisualizationService.DIFFICULTY_COLOR_MAP.get(x, "#888")
            for x in df1["difficulty"]
        ]

        fig.add_trace(
            go.Pie(
                values=list(df1["accepted"]),
                labels=list(df1["difficulty"]),
                sort=False,
                name=username1,
                title=dict(text=username1, position="top center", font=dict(size=18)),
                textposition="inside",
                marker=dict(colors=colors1, line=dict(color="#000000", width=1)),
                textinfo="label+value+percent",
                texttemplate="<b>%{value}</b><br>%{label}",
            ),
            row=1,
            col=1,
        )

        fig.add_trace(
            go.Pie(
                values=list(df2["accepted"]),
                labels=list(df1["difficulty"]),
                sort=False,
                name=username2,
                title=dict(text=username2, position="top center", font=dict(size=18)),
                textposition="inside",
                marker=dict(colors=colors2, line=dict(color="#000000", width=1)),
                textinfo="label+value+percent",
                texttemplate="<b>%{value}</b><br>%{label}",
            ),
            row=1,
            col=2,
        )

        fig.update_layout(
            **VisualizationService.COMMON_LAYOUT,
            legend_title="Difficulty",
            title_text="Problem Count Comparison"
        )
        fig.update_yaxes(automargin=True)
        fig.update_xaxes(automargin=True)

        return plot(fig, output_type="div", include_plotlyjs=False)

    @staticmethod
    def create_skills_bar_chart(problem_type_df: pd.DataFrame, problem_type_name: str):
        """Create a bar chart for skills/tag statistics"""
        if len(problem_type_df) == 0:
            return "<p>No Data Available</p>"

        problem_type_df = problem_type_df.sort_values(
            by=["problemsSolved"], ascending=True
        ).reset_index(drop=True)

        # Vertical Bar Chart for Skills
        fig = go.Figure(
            data=[
                go.Bar(
                    x=list(problem_type_df["tagName"]),  # Category on X
                    y=list(problem_type_df["problemsSolved"]),  # Value on Y
                    text=list(problem_type_df["problemsSolved"]),
                    texttemplate="<b>%{value}</b>",  # Bold values
                    textposition="outside",
                    marker=dict(
                        color=list(problem_type_df["problemsSolved"]),
                        colorscale="Plasma",
                        line=dict(color="rgba(255, 255, 255, 0.2)", width=1),
                    ),
                )
            ]
        )

        fig.update_layout(
            **VisualizationService.COMMON_LAYOUT,
            xaxis_title=None,
            yaxis_title="Problems Solved",
            title_text=problem_type_name,
        )

        fig.update_yaxes(tickfont=dict(size=13))

        return plot(fig, output_type="div", include_plotlyjs=False)

    @staticmethod
    def create_compare_skills_bar_chart(
        data1: pd.DataFrame, data2: pd.DataFrame, username1: str, username2: str, problem_type_name: str = None
    ):
        """Create a bar chart comparing skills/tags with winner highlighting"""
        fig = go.Figure()

        # Data preparation
        x1 = list(data1.get("tagName", []))
        y1 = list(data1.get("problemsSolved", []))
        x2 = list(data2.get("tagName", []))
        y2 = list(data2.get("problemsSolved", []))

        # Ensure alignment

        fig.add_trace(
            go.Bar(
                x=x1,
                y=y1,
                name=username1,
                text=y1,
                textposition="auto",
                marker_color="rgb(0, 184, 163)",
                texttemplate="<b>%{value}</b>",
            )
        )

        fig.add_trace(
            go.Bar(
                x=x2,
                y=y2,
                name=username2,
                text=y2,
                textposition="auto",
                marker_color="rgb(255, 161, 22)",
                texttemplate="<b>%{value}</b>",
            )
        )

        # Add annotations for winners

        for i in range(min(len(y1), len(y2))):
            val1 = y1[i]
            val2 = y2[i]
            if val1 > val2:
                fig.add_annotation(
                    x=x1[i], y=val1, text="🏆", showarrow=False, yshift=15, xshift=-15
                )
            elif val2 > val1:
                fig.add_annotation(
                    x=x2[i], y=val2, text="🏆", showarrow=False, yshift=15, xshift=15
                )

        layout_config = {
            **VisualizationService.COMMON_LAYOUT,
            "xaxis_title": None,
            "yaxis_title": "problems solved",
            "barmode": "group",
        }

        if problem_type_name:
            layout_config["title_text"] = problem_type_name

        fig.update_layout(**layout_config)
        fig.update_yaxes(automargin=True)
        fig.update_xaxes(automargin=True)

        return plot(fig, output_type="div", include_plotlyjs=False)

    @staticmethod
    def create_contest_bar_chart(df: pd.DataFrame):
        """Create a bar chart for contest rankings"""
        if len(df) == 0:
            return ""

        # Vertical Bar Chart for Contests
        fig = go.Figure(
            data=[
                go.Bar(
                    x=list(df["contest"]),
                    y=list(df["ranking"]),
                    text=list(df["ranking"]),
                    hovertext=list(df.get("problemsSolved", [])),
                    texttemplate="<b>%{value}</b>",
                    textposition="auto",
                    marker=dict(
                        color=list(df["ranking"]),
                        colorscale="Plasma",
                        reversescale=True,
                    ),
                )
            ]
        )

        fig.update_layout(
            **VisualizationService.COMMON_LAYOUT,
            xaxis_title="Contests",
            yaxis_title="Rank",
            title_text="Attended Contests Ranking",
        )

        return plot(fig, output_type="div", include_plotlyjs=False)

    @staticmethod
    def create_compare_contest_bar_chart(
        common_contest_df: pd.DataFrame, username1: str, username2: str
    ):
        """Create a bar chart comparing contest rankings with highlighting"""
        if len(common_contest_df) == 0:
            return ""

        fig = go.Figure()

        x = list(common_contest_df.get("contest", []))
        y1 = list(common_contest_df.get("ranking_x", []))
        y2 = list(common_contest_df.get("ranking_y", []))

        fig.add_trace(
            go.Bar(
                x=x,
                y=y1,
                name=username1,
                text=y1,
                marker_color="rgb(0, 184, 163)",
                texttemplate="<b>%{value}</b>",
            )
        )

        fig.add_trace(
            go.Bar(
                x=x,
                y=y2,
                name=username2,
                text=y2,
                marker_color="rgb(255, 161, 22)",
                texttemplate="<b>%{value}</b>",
            )
        )

        # Highlight winner (Lower rank is better!)
        for i in range(len(y1)):
            rank1 = y1[i]
            rank2 = y2[i]
            # Lower rank wins
            if rank1 < rank2:
                fig.add_annotation(
                    x=x[i], y=rank1, text="🏆", showarrow=False, yshift=15, xshift=-15
                )
            elif rank2 < rank1:
                fig.add_annotation(
                    x=x[i], y=rank2, text="🏆", showarrow=False, yshift=15, xshift=15
                )

        fig.update_layout(
            **VisualizationService.COMMON_LAYOUT,
            xaxis_title=None,
            yaxis_title="ranking",
            title_text="Common Contest Ranking",
        )
        fig.update_yaxes(automargin=True)
        fig.update_xaxes(automargin=True)
        fig.update_traces(textposition="inside")

        return plot(fig, output_type="div", include_plotlyjs=False)

    @staticmethod
    def create_language_pie_chart(languages: list):
        """Create a pie chart for language usage"""
        if not languages:
            return "<p>No language data available</p>"

        df = pd.DataFrame(languages)

        fig = go.Figure(
            data=[
                go.Pie(
                    labels=list(df["languageName"]),
                    values=list(df["problemsSolved"]),
                    textinfo="label+percent",
                    textposition="inside",
                )
            ]
        )

        fig.update_layout(
            **VisualizationService.COMMON_LAYOUT,
            title_text="Submissions Language",
            legend_title="Language",
        )
        return plot(fig, output_type="div", include_plotlyjs=False)
