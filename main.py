import dash
import dash_bootstrap_components as dbc
import pandas as pd

from callbacks import register_callbacks
from layout import create_app_layout

DATA_FILE_PATH = 'vaccination-coverage-by-income-in.csv'
DATA_CLEAN_FILE_PATH = 'vaccination_coverage_clean.csv'
EXTERNAL_STYLESHEETS = [dbc.themes.ZEPHYR]

app = dash.Dash(__name__, external_stylesheets=EXTERNAL_STYLESHEETS)
data = pd.read_csv(DATA_FILE_PATH)
data = data.rename(columns={
    'Entity': 'Country',
    'DTP3 (% of one-year-olds immunized)': 'DTP3',
    'GDP per capita': 'GDP',
    'Population (historical estimates)': 'Population'
})
data_clean = pd.read_csv(DATA_CLEAN_FILE_PATH)
data_clean = data_clean.rename(columns={'Entity': 'Country'})
countries = data_clean['Country'].unique()
included_years = range(1990, 2020)
app.layout = create_app_layout(countries, included_years)
register_callbacks(app, data, data_clean, included_years)


if __name__ == '__main__':
    app.run_server(debug=True)
