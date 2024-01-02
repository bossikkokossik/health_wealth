from dash import dcc, html
import dash_bootstrap_components as dbc


def create_slider(slider_id, min_value, max_value, value, mark_values, step, class_name):
    marks = {i: str(year) for i, year in enumerate(mark_values)}
    return dcc.Slider(
        id=slider_id,
        min=min_value,
        max=max_value,
        value=value,
        marks=marks,
        step=step,
        className=class_name
    )


def create_graph(graph_id):
    return dcc.Graph(
        id=graph_id
    )


def create_dropdown(dropdown_id, options, value, multi):
    return dcc.Dropdown(
        id=dropdown_id,
        options=[{'label': option, 'value': option} for option in options],
        value=value,
        multi=multi
    )


def create_container(children, className=''):
    return dbc.Container(children, className=className, fluid=True)


def create_row(children, class_name='', padded=False):
    if padded:
        style = {'padding-top': 50}
    else:
        style = {}
    return dbc.Row(children, className=class_name,
                   justify='center', style=style)


def create_col(children, width='auto', class_name='', align='center'):
    return dbc.Col(children, className=class_name, width=width, align=align)


def create_app_layout(countries, included_years):
    return dbc.Container(
        style={'font-family': 'Arial, sans-serif', 'padding': '30px'},
        fluid=True,
        children=[
            create_row([
                create_col([
                    html.H2(
                        'World Vaccination Coverage Dashboard',
                        style={'text-align': 'center'}
                    ),
                    html.H4(
                        'Visualizing Global Vaccination Coverage from 1990 to 2020',
                        style={'text-align': 'center'}
                    ),
                    create_row([
                        create_col([
                            html.H3(
                                id='choropleth-title',
                                style={'text-align': 'center'}
                            ),
                            create_container([
                                create_slider(
                                    slider_id='choropleth-slider',
                                    min_value=0,
                                    max_value=len(included_years) - 1,
                                    value=0,
                                    mark_values=included_years,
                                    step=1,
                                    class_name='slider'
                                )
                            ]),
                            create_graph('choropleth-plot')
                        ], width=10)
                    ], padded=True),
                    create_row([
                        create_col([
                            html.H4(
                                'Vaccination Coverage (DTP3) Over Time',
                                style={'text-align': 'center'}
                            ),
                            create_dropdown(
                                'country-dropdown-line',
                                countries,
                                ['Germany', 'United States', 'China'],
                                True
                            ),
                            create_graph('line-plot')
                        ], width=10)
                    ], padded=True),
                    create_row([
                        create_col([
                            html.H4(
                                id='scatter-title',
                                style={'text-align': 'center'}
                            ),
                            create_container([
                                create_slider(
                                    slider_id='scatter-slider',
                                    min_value=0,
                                    max_value=len(included_years) - 1,
                                    value=0,
                                    mark_values=included_years,
                                    step=1,
                                    class_name='slider'
                                )
                            ]),
                            create_graph('scatter-plot')
                        ], width=10)
                    ], padded=True),
                    create_row([
                        create_col([
                            html.H4(
                                id='ridgeline-title',
                                style={'text-align': 'center'}
                            ),
                            create_container([
                                create_slider(
                                    slider_id='ridgeline-slider',
                                    min_value=0,
                                    max_value=len(included_years) - 1,
                                    value=0,
                                    mark_values=included_years,
                                    step=1,
                                    class_name='slider'
                                )
                            ]),
                            create_graph('ridgeline-plot')
                        ], width=10)
                    ], padded=True),
                    html.P([
                        'Data Source: ',
                        html.A(
                            'Our World in Data',
                            href='https://ourworldindata.org/vaccination',
                            target='_blank'
                        )
                    ], style={'margin-top': 50})
                ], width=12)
            ])
        ]
    )
