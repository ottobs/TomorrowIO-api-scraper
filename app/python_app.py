import logging
from datetime import datetime
import pandas as pd
import configparser
from sqlalchemy import create_engine
import requests

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

def load_config(file_path: str) -> dict:
    """
    Load configuration from file.
    """
    config = configparser.ConfigParser()
    config.read(file_path)
    logging.info(f"Fetching configs")
    return config._sections


def get_hourly_forecast(base_url, location, api_key):
    """
    Fetch hourly forecast data from the Tomorrow.io API.
    """
    url = f"{base_url}forecast?location={location}&apikey={api_key}"
    logging.info(f"Fetching hourly forecast from {url}")
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def get_hourly_history(base_url, location, api_key):
    """
    Fetch hourly historical data from the Tomorrow.io API.
    """
    url = f"{base_url}history/recent?location={location}&apikey={api_key}"
    logging.info(f"Fetching hourly history from {url}")
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def remove_values_prefix(column_name: str) -> str:
    """
    Remove 'values.' prefix from column names.
    """
    return column_name[len('values.'):].lower() if column_name.startswith('values.') else column_name.lower()


def create_data_frame(results, createdat_flag=False):
    """
    Create a DataFrame from API response.
    """
    df = pd.json_normalize(results)
    df = df[['timelines.hourly', 'location.lat', 'location.lon']]

    df_exploded = df.explode('timelines.hourly')
    df_exploded = df_exploded.reset_index(drop=True)

    df_normalized = pd.concat([df_exploded.drop('timelines.hourly', axis=1),
                               pd.json_normalize(df_exploded['timelines.hourly'])],
                              axis=1)

    df_normalized = df_normalized.rename(columns=remove_values_prefix)
    df_normalized.rename(columns={"location.lat": "lat", "location.lon": "lon"}, inplace=True)

    if createdat_flag:
        df_normalized['createdat'] = datetime.now().strftime('%Y-%m-%dT%H:%M:00Z')
        df_normalized.rename(columns={"time": "predictiontime"}, inplace=True)
    else:
        df_normalized.rename(columns={"time": "historicaltime"}, inplace=True)
    return df_normalized


def send_data(connection_url, schema_name, table_name, df):
    """
    Send DataFrame data to PostgreSQL database.
    """
    engine = create_engine(connection_url)
    return df.to_sql(name=table_name, con=engine, schema=schema_name, if_exists='append', index=False)


def main():
    """
    Main function. Fetches data from the TomorrowIO API,
    and sends it to PostgreSQL using Pandas.
    """
    file_config = load_config('app.config')
    api_key = file_config['Api_key']['key']
    geolocations = file_config['Geolocations']

    base_url = "https://api.tomorrow.io/v4/weather/"

    forecast_results = []
    recent_history_results = []

    for location in geolocations.values():
        forecast_results.append(get_hourly_forecast(base_url, location, api_key))
        recent_history_results.append(get_hourly_history(base_url, location, api_key))
        
    postgres_user = file_config['Postgresql']['postgres_user']
    postgres_password = file_config['Postgresql']['postgres_password']
    postgres_database = file_config['Postgresql']['postgres_db']

    connection_url = f"postgresql://{postgres_user}:{postgres_password}@postgres:5432/{postgres_database}"

    df_forecast = create_data_frame(forecast_results, createdat_flag=True)
    df_history = create_data_frame(recent_history_results)

    logging.info("Sending forecast data to database")
    send_data(connection_url=connection_url, schema_name='tomorrowio', table_name='forecasts', df=df_forecast)
    logging.info("Sending historical data to database")
    send_data(connection_url=connection_url, schema_name='tomorrowio', table_name='recent_weather_history', df=df_history)


if __name__ == "__main__":
    main()
