import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from app import app
from components import daily_stats
from components import news_feed, twitter_feed
from components import confirmed_cases_chart, infection_trajectory_chart
from components import confirmed_scatter_mapbox, drive_thru_scatter_mapbox
from components import (
    states_confirmed_stats,
    states_deaths_stats,
    states_recovered_stats,
)


########################################################################
#
# News and Twitter Tabs
#
########################################################################

tabs_styles = {"height": "44px"}
tab_style = {
    "borderBottom": "1px solid #d6d6d6",
    "padding": "6px",
    "fontWeight": "bold",
}

tab_selected_style = {
    "borderTop": "1px solid #d6d6d6",
    "borderBottom": "1px solid #d6d6d6",
    "backgroundColor": "#119DFF",
    "color": "white",
    "padding": "6px",
}

feed_tabs = dbc.Card(
    [
        # dbc.CardHeader(
        #     dbc.Tabs(
        #         [
        #             dbc.Tab(
        #                 label="Twitter Feed",
        #                 tab_id="twitter-tab",
        #                 labelClassName="twitter-feed-tab",
        #             ),
        #             dbc.Tab(
        #                 label="News Feed",
        #                 tab_id="news-tab",
        #                 labelClassName="news-feed-tab",
        #             ),
        #         ],
        #         id="feed-tabs",
        #         card=True,
        #         active_tab="twitter-tab",
        #     )
        # ),
        html.Div(
            dcc.Tabs(
                id="left-tabs-styled-with-inline",
                value="twitter-tab",
                children=[
                    dcc.Tab(
                        label="Twitter Feed",
                        value="twitter-tab",
                        className="left-twitter-tab",
                        style=tab_style,
                        selected_style=tab_selected_style,
                    ),
                    dcc.Tab(
                        label="News Feed",
                        value="news-tab",
                        className="left-news-tab",
                        style=tab_style,
                        selected_style=tab_selected_style,
                    ),
                ],
                style=tabs_styles,
            ),
            className="left-tabs",
        ),
        html.Div(id="feed-content", className="card-text"),
    ]
)


@app.callback(
    Output("feed-content", "children"), [Input("tabs-styled-with-inline", "value")]
)
def feed_tab_content(active_tab):
    """Callback to change between news and twitter feed
    """
    if active_tab == "twitter-tab":
        return twitter_feed()
    else:
        return news_feed()


########################################################################
#
# Confirmed/Deaths Tabs
#
########################################################################
stats_tabs = dbc.Card(
    [
        dbc.CardHeader(
            dbc.Tabs(
                [
                    dbc.Tab(label="Confirmed", tab_id="confirmed-tab"),
                    dbc.Tab(label="Deaths", tab_id="deaths-tab"),
                    dbc.Tab(label="Recovered", tab_id="recovered-tab"),
                ],
                id="stats-tabs",
                card=True,
                active_tab="confirmed-tab",
            )
        ),
        dbc.CardBody(html.P(id="stats-content", className="card-text")),
    ]
)


@app.callback(Output("stats-content", "children"), [Input("stats-tabs", "active_tab")])
def stats_tab_content(active_tab):
    """Callback to change between news and twitter feed
    """
    if active_tab == "deaths-tab":
        return states_deaths_stats()
    elif active_tab == "recovered-tab":
        return states_recovered_stats()
    else:
        return states_confirmed_stats()


########################################################################
#
# Us Map Confirmed / Drive-Thru testing Map
#
########################################################################

# us_maps_tabs = [
#     html.Div(
#         [
#             html.Div(html.H1("US Map"), className="top-bar-us-map-heading-txt",),
#             html.Div(
#                 dbc.Tabs(
#                     [
#                         dbc.Tab(
#                             label="Confirmed",
#                             tab_id="confirmed-us-map-tab",
#                             labelClassName="confirmed-us-map-tab",
#                         ),
#                         dbc.Tab(
#                             label="Drive-Thru Testing",
#                             tab_id="testing-us-map-tab",
#                             labelClassName="testing-us-map-tab",
#                         ),
#                     ],
#                     id="map-tabs",
#                     card=True,
#                     active_tab="confirmed-us-map-tab",
#                     className="top-bar-us-map-tabs-content",
#                 )
#             ),
#         ],
#         className="d-flex justify-content-between top-bar-us-map-heading-content",
#     ),
#     html.Div(dcc.Graph(id="us-map", style={"height": "54vh"})),
# ]

us_maps_tabs = dbc.Card(
    dbc.CardBody([
        html.Div(
            [
                html.Div("US Map", className="top-bar-us-map-heading-txt",),
                html.Div(
                    dbc.Tabs(
                        [
                            dbc.Tab(
                                label="Confirmed",
                                tab_id="confirmed-us-map-tab",
                                labelClassName="confirmed-us-map-tab",
                            ),
                            dbc.Tab(
                                label="Drive-Thru Testing",
                                tab_id="testing-us-map-tab",
                                labelClassName="testing-us-map-tab",
                            ),
                        ],
                        id="map-tabs",
                        card=True,
                        active_tab="confirmed-us-map-tab",
                        className="top-bar-us-map-tabs-content",
                    )
                ),
            ],
            className="d-flex justify-content-between top-bar-us-map-heading-content",
        ),
        html.Div(dcc.Graph(id="us-map", style={"height": "54vh"})),
    ]),
)

@app.callback(Output("us-map", "figure"), [Input("map-tabs", "active_tab")])
def map_tab_content(active_tab):
    """Callback to change between news and twitter feed
    """
    if active_tab == "testing-us-map-tab":
        return drive_thru_scatter_mapbox()
    else:
        return confirmed_scatter_mapbox()


########################################################################
#
# Desktop App Layout
#
########################################################################
desktop_body = [
    dbc.Row(daily_stats(), className="top-bar-content"),  # TOP BAR
    dbc.Row(  # MIDDLE - MAP & NEWS FEED CONTENT
        [
            # LEFT - TWITTER & NEWS FEED COL
            dbc.Col(feed_tabs, className="left-col-twitter-feed-content", width=2),
            # MIDDLE - MAPS COL
            dbc.Col(
                [
                    # big map
                    # html.Div(us_maps_tabs),
                    dbc.Row(
                        [
                            dbc.Col(
                                us_maps_tabs,
                                className="top-top-map",
                                width=12,
                            ),
                        ],
                        # no_gutters=True,
                    ),
                    # bottom two charts
                    dbc.Row(
                        [
                            dbc.Col(
                                dbc.Card(
                                    dbc.CardBody([
                                        html.Div("Confirmed Cases",
                                                className="top-bottom-left-chart-title",),
                                        dcc.Graph(figure=confirmed_cases_chart(),
                                                  config={'responsive':False},
                                                  className="top-bottom-left-chart-figure"),
                                    ])
                                ),
                                className="top-bottom-left-chart",
                                width=6,
                            ),
                            dbc.Col(
                                dbc.Card(
                                    dbc.CardBody([
                                        html.Div("Infection Trajectory Since 200 Cases",
                                                className="top-bottom-right-chart-title"),
                                        dcc.Graph(figure=infection_trajectory_chart(),
                                                  config={'responsive':False},
                                                  className="top-bottom-right-chart-figure"),
                                    ]),
                                ),
                                className="top-bottom-right-chart",
                                width=6,
                            ),
                        ],
                        no_gutters=True,
                        className="top-bottom-charts",
                    ),
                ],
                className="middle-col-map-content",
                width=8,
            ),
            # RIGHT - STATS COL
            dbc.Col(stats_tabs, className="right-col-news-feed-content", width=2),
        ],
        no_gutters=True,
        className="middle-map-news-content mt-3",
    ),
    # dbc.Row(  # MIDDLE - MAP & NEWS FEED CONTENT
    #     # html.Div(
    #         # dbc.Row(
    #             [
    #                 dbc.Col(
    #                     dcc.Graph(figure=confirmed_cases_chart(),
    #                               responsive=True,
    #                               config={
                                    
    #                                 # 'figure.layout.height'="10rem";
    #                                 'scrollZoom':False,
    #                                 },
    #                     ),
    #                     className="top-bottom-left-chart",
    #                     width=6,
    #                 ),
    #                 dbc.Col(
    #                     dcc.Graph(figure=infection_trajectory_chart()),
    #                     className="top-bottom-right-chart",
    #                     width=6,
    #                 ),
    #             ],
    #             no_gutters=True,
    #         # ),
    #         # className="top-bottom-charts",
    #     # ),
    # )
]
