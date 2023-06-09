
# Copyright 2022 Cisco Systems, Inc. and its affiliates
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: Apache-2.0


import dash_bootstrap_components as dbc
from dash import html, dcc
import requests

from backend.config import DevelopmentConfig
from frontend.custom_resources import CONTENT_STYLE, CREAM, WHITE, CISCO_LOGO, CISCO_LINK, TEAL, SIDEBAR_STYLE


class PageCustom:
    def __init__(self, params):
        self.params = params

    def get_page(self):
        tasks = self.params._data_dict['function']['task'].split('/')
        model_title = "BLAZE Dashboard - Cisco Research"

        return html.Div(
            html.Div([
                self.get_title_card(model_title),
                dbc.Row([
                    dbc.Col(self.get_input_box()),
                    dbc.Col(
                        html.Div([self.get_output_box(task) for task in tasks]))
                ])
            ],
                style=CONTENT_STYLE),
            id="custom-content")

    def get_sidebar(self):
        model_checklist = self.params._data_dict['states']['model_checklist']
        sidebar = html.Div([

            html.Center(html.P(
                self.params._data_dict['Title'],
                className="lead",
                style={'color': CREAM, 'font-size': 23,
                       'font-weight': "bold", 'font-family': "Quicksand"}
            )),

            html.Br(),
            html.P(
                """Please select a model:""",
                style={'color': WHITE, 'font-family': "Quicksand"}
            ),

            dbc.Card([
                html.Div(
                    [
                        get_custom_model_checklist(model_checklist[i][0], model_checklist[i][1]) for i in range(len(model_checklist))
                    ]),
            ], color="dark", style={"padding": "1rem", 'font-family': "Quicksand"}),


            html.Br(),
            html.P(
                """Please upload a .txt or .pdf:""",
                style={'color': WHITE, 'font-family': "Quicksand", 'display': 'none' if "User" not in self.params._data_dict["datasets"] else "block"}),

            dbc.Card([
                html.Div(
                    [
                        html.Center(dcc.Upload(dbc.Button(
                            'Upload (.txt or .pdf)',
                            color="info",
                            outline=True,
                            style={'font-family': "Quicksand", }),
                            id="sidebar-file-button")),
                    ]),
            ], color="dark", style={"padding": "1rem", 'display': 'none' if "User" not in self.params._data_dict["datasets"] else "block"}),

            html.Br(),
            html.P(
                """Please choose a task.""",
                style={'color': WHITE, 'font-family': "Quicksand"}
            ),

            dbc.Card([
                html.Div(
                    [
                        get_custom_functions_checklist(
                            self.params._data_dict['function'])
                    ]
                )
            ], color="dark", style={"padding": "1rem"}),

            html.Br(),

            dbc.Card([
                html.Div(
                    [
                        html.Center(dbc.Button(
                            'Reset Dash',
                            color="info",
                            outline=True,
                            style={'font-family': "Quicksand"},
                            id='sidebar-reset-button')),
                    ]),
            ], color="dark", style={"padding": ".8rem"}),

            html.Br(),

            html.Center(dbc.Row(dbc.Col(html.Img(
                src=CISCO_LOGO,
                height="90px",
                style={"margin-bottom": "15px"})))),

            html.Center(html.B(html.A(
                "Join Cisco Research Labs",
                href=CISCO_LINK,
                target="_blank",
                style={'color': TEAL, 'font-family': "Quicksand"}))),

        ],
            style=SIDEBAR_STYLE,
        )
        return sidebar

    def get_title_card(self, model_text):
        titleCard = html.Center(dbc.Button(
            model_text,
            color="info",
            outline=True,
            style={'font-family': "Quicksand", "font-size": "40px", "padding": "1rem", "margin-bottom": "2rem"},))
        return titleCard

    def get_input_box(self):
        preview = "Kindly choose a file in order to preview it"
        file_txt = None
        placeholder = "Please choose a file:"

        if self.params._data_dict['states']['has_input_file']:
            preview, file_txt = gen_file_preview(
                self.params._data_dict['states']['chosen_data'], self.params._data_dict['states']['chosen_path'])
            placeholder = self.params._data_dict['states']['chosen_data']

        inputBox = dbc.Card([
            dbc.CardBody([
                            html.Center(html.H5("Input Text(s)", style={
                                        "font-family": "Quicksand", "color": CREAM, 'font-size': "30px", "padding": "1rem"})),

                            dbc.Row([
                                dbc.Col([
                                    html.H6
                                    (
                                        "Please choose a file:",
                                        style={"font-family": "Quicksand", "color": WHITE,
                                               'font-size': "22px", "padding": "1rem"}
                                    ),
                                ], width=6),
                                dbc.Col([
                                    dbc.Select(
                                        id="custom-choose-file",
                                        options=gen_input_options(self.params),
                                        style={
                                            "background": "#888888", "color": WHITE, "font-family": "Quicksand"},
                                        placeholder=placeholder
                                    ),
                                ])
                            ], align="center"),

                            html.H6
                            (
                                "New files can be added via \"Upload\" in the sidebar.",
                                style={"font-family": "Quicksand", "font-style": "italic",
                                       "color": WHITE, 'font-size': "22px", "padding": "1rem"}
                            ),

                            html.Br(),

                            dbc.Card([
                                html.H5(preview),
                                html.Br(),
                                html.P(file_txt, style={
                                    "color": WHITE, "overflow": "auto", "height": "12rem"}),

                            ],
                                style={"background": "#88888822", "color": WHITE,
                                       "font-family": "Quicksand", "padding": "1rem"}
                            ),

                            html.Br(),
                            ],
                         className="mb-3",
                         style={"width": "100%", "height": "42rem"},
                         ),
        ],
            outline=True,
            color="#049FD911",
            style={"color": "dark"}
        )
        return inputBox

# ==============================================================================
# ============================ OUTPUT BOXES ====================================
# ==============================================================================

    def get_output_box_search(self):
        outputBox = dbc.Card([
            dbc.CardBody([
                html.Center(
                    html.H5(
                        "Question-Answering",
                        style={"font-family": "Quicksand", "color": CREAM, 'font-size': "30px", "padding": "1rem"})),

                dbc.Card([
                    html.Div(
                        [
                            dbc.Row([

                                dbc.Col(dbc.Input(
                                    className="mb-3",
                                    placeholder=self.params._data_dict['states']['query'],
                                    id="search-custom-enter-q-box",
                                    style={"color": WHITE,
                                        "background": "#88888822"}
                                ), width=8),

                                dbc.Col(dbc.Button(
                                    'Ask Q',
                                    color="info",
                                    outline=True,
                                    id="search-custom-ask-q-button",
                                    style={'font-family': "Quicksand"})),

                                dbc.Col(dbc.Button(
                                    'Index',
                                    color="info",
                                    outline=True,
                                    id="custom-begin-index",
                                    style={'font-family': "Quicksand"}))
                            ]),

                            dbc.Alert(
                                html.H6(
                                    self.params._data_dict['states']['result_search'],
                                    style={'text-align': 'right',
                                           "color": WHITE}
                                ),
                                color="#88888822"
                            )
                        ]),

                ], color="#88888822", style={"padding": "1rem", 'font-family': "Quicksand"}),
            ],
                className="mb-3",
                style={"width": "100%", "height": "20rem"},
            ),
        ],
            outline=True,
            color="#049FD911",
            style={"color": "dark"}
        )
        return outputBox

    def get_output_box_summarization(self):

        outputBox = dbc.Card([
            dbc.CardBody([
                html.Center(html.H5(
                    "Summarization",
                    style={
                        "font-family": "Quicksand", "color": CREAM, 'font-size': "30px", "padding": "1rem"})),

                dbc.Card([
                    html.Div(
                        [
                            dbc.Alert(
                                html.H6(
                                    self.params._data_dict['states']['result_summarization'],
                                    style={'text-align': 'right',
                                           "color": WHITE}
                                ),
                                color="#88888822"
                            )
                        ]),

                ], color="#88888822", style={"padding": "1rem", 'font-family': "Quicksand"}),

                html.Br(id="custom-begin-index"),
                html.Center(dbc.Button(
                    'Summarize',
                    color="info",
                    outline=True,
                    id="custom-begin-summarization", style={'font-size': "26px", 'font-family': "Quicksand"}))
            ],
                className="mb-3",
                style={"width": "100%", "height": "20rem"},
            ),
        ],
            outline=True,
            color="#049FD911",
            style={"color": "dark"}
        )
        return outputBox

    def get_output_box(self, task):

        if task == 'search':
            return self.get_output_box_search()

        elif task == 'summarization':
            return self.get_output_box_summarization()

# ==============================================================================
# =============================== FILES ========================================
# ==============================================================================


BLAZE_API = f"{DevelopmentConfig.PREF_REST_API}{DevelopmentConfig.PORT_REST_API}"


def gen_file_preview(filename, fileclass):
    request = f"{BLAZE_API}/datasets/files/detail"
    print(f"filename: {filename}, fileclass: {fileclass}")

    # Fileclass is simply the dataset class (ex. Squad, user)
    response = requests.get(
        request, params={'filename': filename, 'fileclass': fileclass})

    file_content = response.json()['content']
    # <-- only for user files, if not then "N/A" (in KB)
    file_size = response.json()['size']

    preview = f"Preview of File: {len(file_content)} chars, {len(file_content.split())} words, {file_size} kilobytes"
    return preview, file_content


def gen_input_options(params):

    server_files = {}
    for dataset in params._data_dict['datasets']:
        request = f"{BLAZE_API}/datasets/files"
        response = requests.get(request, params={'dataset': dataset})

        server_files[dataset] = response.json()['files']

    options = []
    for entry in server_files:

        # Add an unclickable option for it to look nicer
        options.append({"label": f"-- {entry} Files --", "disabled": True})

        files_list = server_files[entry]
        for i in range(len(files_list)):
            options.append(
                {"label": files_list[i], "value": f"{entry}|{files_list[i]}"})

    return options

# ==============================================================================
# =============================== OPTIONS ======================================
# ==============================================================================


def get_custom_model_checklist(options, task):

    check_list = dcc.RadioItems(
        options=options,
        value=options[0]['value'],
        id="sidebar-models-checklist-" + task,
        inline=False,
        labelStyle={'display': 'block'},
        style={'color': WHITE, 'font-family': "Quicksand"},
    )

    element = html.Div(
        [dbc.Label(task.capitalize(), style={'color': CREAM}), check_list, html.Br()])

    return element


def get_custom_functions_checklist(functions):

    list_options = []

    for func in functions:
        if func == 'task':
            continue
        if func == 'custom':
            list_options.append(
                {"label": "Custom Demo", "value": "Custom Demo"})

        if func == 'benchmarking':
            list_options.append(
                {"label": "Solo Benchmark", "value": "Solo Benchmark"})

        if func == "comparing":
            list_options.append(
                {"label": "Model Comparison", "value": "Model Comparison"})

    if len(list_options) == 0:
        list_options.append({"label": "Custom Demo", "value": "Custom Demo"})

    return dbc.RadioItems(
        options=list_options,
        value=list_options[0]['value'],
        id="sidebar-function-radioitems",
        style={'color': WHITE, "padding": "0rem",
               'font-family': "Quicksand"}
    )


def get_object_options(params, object_type):

    object_names = []
    objects = params._data_dict['states'][object_type + '_objs']

    for object_iter in objects:
        object_name = object_iter._get_class_name()
        object_names.append(object_name)

    options = []

    for i in range(len(object_names)):
        options.append(
            {"label": object_names[i], "value": object_names[i]})

    return options
