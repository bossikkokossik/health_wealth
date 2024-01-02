from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import copy


def generate_choropleth_title(year):
    return f'Vaccination Coverage (DTP3) in {year}'


def generate_choropleth_plot(data, year):
    fig = px.choropleth(
        data_frame=data,
        locations='Code',
        locationmode='ISO-3',
        color=str(year),
        hover_data={'Country': True, str(year): ':.0f'},
        color_continuous_scale='dense'
    )
    fig.update_layout(margin=dict(l=0, r=0, t=30, b=0))
    return fig


def generate_line_plot(data, countries):
    filtered_data = data[data['Country'].isin(countries)]
    filtered_data = filtered_data.drop('Code', axis=1)
    filtered_data = filtered_data.melt(
        id_vars=['Country'], var_name='Year', value_name='Vaccination Coverage')
    try:
        fig = px.line(
            data_frame=filtered_data,
            x='Year',
            y='Vaccination Coverage',
            color='Country'
        )
    except Exception:
        fig = px.line(
            data_frame=filtered_data,
            x='Year',
            y='Vaccination Coverage',
            color='Country'
        )
    fig.update_layout(
        margin=dict(l=0, r=0, t=40, b=0),
        yaxis_title='DTP3 (%)'
    )
    return fig


def generate_scatter_title(year):
    return f'Vaccination Coverage (DTP3) vs GDP in {year}'


def generate_scatter_plot(data, year):
    filtered_data = data
    filtered_data['Year'] = pd.to_numeric(
        filtered_data['Year'],
        errors='coerce'
    )
    filtered_data.sort_values(by='Country', inplace=True)
    filtered_data['Continent'].ffill(inplace=True)
    filtered_data = filtered_data.dropna(subset=['Population', 'Continent'])
    filtered_data = filtered_data[filtered_data['Year'] == year]
    fig = px.scatter(
        filtered_data,
        x='GDP',
        y='DTP3',
        color='Continent',
        size='Population',
        hover_name='Country',
        log_x=True,
        size_max=120
    )
    fig.update_layout(
        margin=dict(l=0, r=0, t=30, b=0),
        xaxis_title='GDP per capita (USD)',
        yaxis_title='DTP3 (%)'
    )
    return fig


def generate_ridgeline_title(year):
    return f'Distribution of Vaccination Coverage (DTP3) vs GDP per Capita in {year}'


def generate_ridgeline_plot(data, year):
    cmap = px.colors.sequential.Viridis
    filtered_data = copy.deepcopy(data)
    filtered_data.loc[:, 'GDP_category'] = pd.cut(
        x=data['GDP'].astype(float),
        bins=[0, 1000, 5000, 10000, 50000, 200000],
        labels=['<1k', '1k-5k', '5k-10k', '10k-50k', '>50k']
    )
    filtered_data = filtered_data[filtered_data['DTP3'].notna()]
    filtered_data = filtered_data[filtered_data['Year'] == year]
    fig = go.Figure()
    for category, color in zip(filtered_data['GDP_category'].unique().categories, cmap):
        fig.add_trace(go.Violin(
            x=filtered_data['DTP3'][filtered_data['GDP_category'] == category],
            name=category,
            line_color=color,
            span=[0, 100],
            spanmode='manual'
        ))
    fig.update_traces(
        orientation='h',
        side='positive',
        width=1.75,
        points=False
    )
    fig.update_layout(
        margin=dict(l=0, r=0, t=40, b=0),
        xaxis_title='DTP3 (%)',
        yaxis_title='GDP per capita (USD)',
        yaxis_showgrid=True
    )
    return fig


def register_callbacks(app, data, data_clean, included_years):
    @app.callback(
        Output('choropleth-title', 'children'),
        [Input('choropleth-slider', 'value')]
    )
    def update_choropleth_title_callback(year_index):
        year = included_years[year_index]
        return generate_choropleth_title(year)

    @app.callback(
        Output('choropleth-plot', 'figure'),
        [Input('choropleth-slider', 'value')]
    )
    def update_choropleth_plot_callback(year_index):
        year = included_years[year_index]
        return generate_choropleth_plot(data_clean, year)

    @app.callback(
        Output('line-plot', 'figure'),
        [Input('country-dropdown-line', 'value')]
    )
    def update_line_plot_callback(selected_countries):
        return generate_line_plot(data_clean, selected_countries)

    @app.callback(
        Output('scatter-title', 'children'),
        [Input('scatter-slider', 'value')]
    )
    def update_scatter_title_callback(year_index):
        year = included_years[year_index]
        return generate_scatter_title(year)

    @app.callback(
        Output('scatter-plot', 'figure'),
        [Input('scatter-slider', 'value')]
    )
    def update_scatter_plot_callback(year_index):
        year = included_years[year_index]
        return generate_scatter_plot(data, year)

    @app.callback(
        Output('ridgeline-title', 'children'),
        [Input('ridgeline-slider', 'value')]
    )
    def update_ridgeline_title_callback(year_index):
        year = included_years[year_index]
        return generate_ridgeline_title(year)

    @app.callback(
        Output('ridgeline-plot', 'figure'),
        [Input('ridgeline-slider', 'value')]
    )
    def update_ridgeline_plot_callback(year_index):
        year = included_years[year_index]
        return generate_ridgeline_plot(data, year)
