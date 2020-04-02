# Dash application about losing streaks
# G. Jan - 12/18

# Libraries
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import pandas as pd
import requests, zipfile, io, os

pd.options.mode.chained_assignment = None  # default='warn'

##################################################################################################################################################################################################

# CSS design
external_stylesheets = [
    "https://codepen.io/chriddyp/pen/bWLwgP.css",
    dbc.themes.BOOTSTRAP,
]

# Dash server
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.layout = html.Div(
    [
        dbc.Navbar(
            [
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.NavbarBrand(
                                "Losing streaks",
                                className="mb-0 h1",
                                style={"font-size": "30px"},
                            )
                        ),
                        # SUPER UGLY
                        dbc.Col(),
                        dbc.Col(),
                        dbc.Col(),
                        dbc.Col(),
                        dbc.Col(),
                        dbc.Col(),
                        dbc.Col(),
                        dbc.Col(),
                        dbc.Col(),
                        dbc.Col(
                            [
                                html.Div(
                                    children="by Gregoire Jan",
                                    style={
                                        "color": "white",
                                        # "font-weight": "bold",
                                        "font-size": "10px",
                                        "textAlign": "center",
                                    },
                                ),
                                html.A(
                                    "https://gregoirejan.github.io/",
                                    href="https://gregoirejan.github.io/",
                                    target="_blank",
                                ),
                            ]
                        ),
                    ],
                    align="center",
                    no_gutters=True,
                    className="col-12",
                ),
            ],
            color="dark",
            dark=True,
        ),
        dbc.Row(
            [
                html.Div(
                    children="Ever wondered if your football team was always losing against a team with a losing streak?",
                    style={"textAlign": "left", "color": "black", "font-size": "20px",},
                ),
                html.Div(
                    children='Here you can check which team are "best" at stopping opponent losing streaks (2 previously lost games) by selecting the country/season/league you are interested in (it can take few seconds to pop up):',
                    style={"textAlign": "left", "color": "black", "font-size": "20px",},
                ),
            ],
            style={"border": "50px solid", "color": "white"},
        ),
        dbc.Row(
            [
                dbc.Col(className="col-2"),
                dbc.Col(
                    [
                        dcc.Dropdown(
                            id="country",
                            options=[
                                {"label": "Belgium", "value": "B"},
                                {"label": "Germany", "value": "D"},
                                {"label": "England", "value": "E"},
                                {"label": "France", "value": "F"},
                                {"label": "Greece", "value": "G"},
                                {"label": "Italy", "value": "I"},
                                {"label": "Netherland", "value": "N"},
                                {"label": "Portugal", "value": "P"},
                                {"label": "Scotland", "value": "SC"},
                                {"label": "Spain", "value": "SP"},
                                {"label": "Turquey", "value": "T"},
                            ],
                            placeholder="Select a country",
                            style={"font-size": "15px"}
                        ),
                    ],
                ),
                dbc.Col(
                    [
                        dcc.Dropdown(
                            id="season",
                            options=[
                                {"label": "2018/2019", "value": "1819"},
                                {"label": "2017/2018", "value": "1718"},
                                {"label": "2016/2017", "value": "1617"},
                                {"label": "2015/2016", "value": "1516"},
                                {"label": "2014/2015", "value": "1415"},
                                {"label": "2013/2014", "value": "1314"},
                                {"label": "2012/2013", "value": "1213"},
                                {"label": "2011/2012", "value": "1112"},
                                {"label": "2010/2011", "value": "1011"},
                                {"label": "2009/2010", "value": "0910"},
                                {"label": "2008/2009", "value": "0809"},
                                {"label": "2007/2008", "value": "0708"},
                                {"label": "2006/2007", "value": "0607"},
                                {"label": "2005/2006", "value": "0506"},
                                {"label": "2004/2005", "value": "0405"},
                                {"label": "2003/2004", "value": "0304"},
                                {"label": "2002/2003", "value": "0203"},
                                {"label": "2001/2002", "value": "0102"},
                                {"label": "2000/2001", "value": "0001"},
                                {"label": "1999/2000", "value": "9900"},
                                {"label": "1998/1999", "value": "9899"},
                                {"label": "1997/1998", "value": "9798"},
                                {"label": "1996/1997", "value": "9697"},
                                {"label": "1995/1996", "value": "9596"},
                                {"label": "1994/1995", "value": "9495"},
                                {"label": "1993/1994", "value": "9394"},
                            ],
                            placeholder="Select a season",
                            style={"font-size": "15px"}
                        ),
                    ],
                ),
                dbc.Col(
                    [
                        dcc.Dropdown(
                            id="league",
                            options=[
                                {"label": "1.", "value": "1"},
                                {"label": "2.", "value": "2"},
                                {"label": "3.", "value": "3"},
                                {"label": "4.", "value": "4"},
                            ],
                            placeholder="Select a league",
                            style={"font-size": "15px"}
                        ),
                    ],
                ),
                dbc.Col(
                    [
                        html.Button(
                            id="submit-button",
                            n_clicks=0,
                            children="Submit",
                            style={
                                "font-size": "15px",
                                "color": "white",
                                "background-color": "blue",
                            },
                        )
                    ],
                ),
                dbc.Col(
                    [
                        html.Div(
                            id="fail",
                            style={
                                "color": "red",
                                "font-weight": "bold",
                                "margin": "15px 0px",
                                "width": "150px",
                            },
                        ),
                    ]
                ),
                dbc.Col(className="col-2"),
            ]
        ),
        dbc.Row(
            dbc.Col([dcc.Graph(id="bar-graph", figure={"data": []})], align="center"),
        ),
    ]
)
# Callback to check for avaibility of input data after clicking the submit button
@app.callback(
    dash.dependencies.Output("fail", "children"),
    [dash.dependencies.Input("submit-button", "n_clicks")],
    [
        dash.dependencies.State("season", "value"),
        dash.dependencies.State("country", "value"),
        dash.dependencies.State("league", "value"),
    ],
)

# Display error message if not available
def available(n_clicks, season, country, league):
    try:
        r = requests.get(
            "http://www.football-data.co.uk/mmz4281/" + season + "/data.zip"
        )
        z = zipfile.ZipFile(io.BytesIO(r.content))
        zip_filepath = "."
        if country in ["E", "SC"]:
            league = str(int(league) - 1)
        z.extract(country + league + ".csv", zip_filepath)
        z.close()
    except KeyError:
        return """Not available"""


# Callback to update bar plot after clicking the submit button
@app.callback(
    dash.dependencies.Output("bar-graph", "figure"),
    [dash.dependencies.Input("submit-button", "n_clicks")],
    [
        dash.dependencies.State("season", "value"),
        dash.dependencies.State("country", "value"),
        dash.dependencies.State("league", "value"),
    ],
)

####################################################################################################################################################################################################

# Update bar plot with computed number of games lost when the opponent was on 2 games losing streak
def update_graph(n_clicks, season, country, league):
    if season is None:
        return go.Figure(
            data=[
                go.Bar(
                    x=["Team 1","Team 2", "Team 3","Team 4","Team 5","Team 6","Team 7","Team 8"],
                    y=[4,2,2,2,2,1,0,0],
                    marker={"color": "IndianRed"},
                )
            ],
            layout=go.Layout(
                xaxis={"title": "Teams"},
                yaxis={"title": "Number of games"},
                plot_bgcolor="rgb(255,255,255)",
                height=500,
            ),
        )
    else:
        # Download data from football-data.co.uk
        r = requests.get("http://www.football-data.co.uk/mmz4281/" + season + "/data.zip")
        z = zipfile.ZipFile(io.BytesIO(r.content))
        zip_filepath = "."
        if country in ["E", "SC"]:
            league = str(int(league) - 1)
        z.extract(country + league + ".csv", zip_filepath)
        z.close()
        df = pd.read_csv(country + league + ".csv", usecols=["HomeTeam", "AwayTeam", "FTR"])
        os.remove(country + league + ".csv")

        teams = {}
        for team in df["HomeTeam"].unique():
            if not pd.isnull(team):
                teams[team] = df[(df["HomeTeam"] == team) | (df["AwayTeam"] == team)]

        for team in teams:
            # Initilize resulsts with -1 for a defeat
            teams[team]["results"] = -1
            j = 1
            for i in teams[team].index:
                teams[team].loc[i, "matchday"] = j
                # Results = 1 for a victory (home or away)
                if (teams[team].loc[i, "FTR"] == "H") & (
                    teams[team].loc[i, "HomeTeam"] == team
                ):
                    teams[team].loc[i, "results"] = 1
                if (teams[team].loc[i, "FTR"] == "A") & (
                    teams[team].loc[i, "AwayTeam"] == team
                ):
                    teams[team].loc[i, "results"] = 1
                # Results = 0 for a draw
                if teams[team].loc[i, "FTR"] == "D":
                    teams[team].loc[i, "results"] = 0
                # Set flag whether team is at home or away
                if teams[team].loc[i, "HomeTeam"] == team:
                    teams[team].loc[i, "homeaway"] = "home"
                else:
                    teams[team].loc[i, "homeaway"] = "away"
                j += 1

        for team in teams:
            teams[team] = teams[team].reset_index(drop=True)
            # After the 3rd match day sum the previous results of the 2 games from the opponent
            for i in teams[team].index:
                if teams[team].loc[i, "matchday"] > 3:
                    if teams[team].loc[i, "homeaway"] == "home":
                        teams[team].loc[i, "resultsop"] = sum(
                            teams[teams[team].loc[i, "AwayTeam"]]["results"][
                                int(teams[team].loc[i, "matchday"])
                                - 3 : int(teams[team].loc[i, "matchday"])
                                - 1
                            ]
                        )
                    if teams[team].loc[i, "homeaway"] == "away":
                        teams[team].loc[i, "resultsop"] = sum(
                            teams[teams[team].loc[i, "HomeTeam"]]["results"][
                                int(teams[team].loc[i, "matchday"])
                                - 3 : int(teams[team].loc[i, "matchday"])
                                - 1
                            ]
                        )
                    # if the game is lost and the opponent has at least lost its 2 previous games hen the flag is 1 - otherwise 0
                    if (teams[team].loc[i, "resultsop"] < -1) & (
                        teams[team].loc[i, "results"] == -1
                    ):
                        teams[team].loc[i, "relance"] = 1
                    else:
                        teams[team].loc[i, "relance"] = 0

        relancesum = {}
        # For each team sum the flags = number of games lost when the opponent was on a 2 games losing streak
        for team in teams:
            relancesum[team] = teams[team]["relance"].sum()
        relancesum = pd.DataFrame(
            sorted(relancesum.items(), key=lambda kv: kv[1], reverse=True)
        )
        relancesum.columns = ["Team", "Relance games"]

        # Plot bar plot
        return go.Figure(
            data=[
                go.Bar(
                    x=list(relancesum["Team"]),
                    y=list(relancesum["Relance games"]),
                    marker={"color": "IndianRed"},
                )
            ],
            layout=go.Layout(
                xaxis={"title": "Teams"},
                yaxis={"title": "Number of games"},
                plot_bgcolor="rgb(255,255,255)",
                height=500,
            ),
        )


#################################################################################################################################################################################################

# Run dash server
if __name__ == "__main__":
    app.run_server(debug=True)
