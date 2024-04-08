# TomorrowIO Data Scraper

## Description
This project presents a basic scraper of weather data, using the TomorrowIO API, using Python to fetch the data, PostgreSQL to store, and Jupyter to visualize the results.

Historical weather data is saved in the table `tomorrowio.recent_weather_history`, and forecasts are saved into `tomorrowio.forecasts`.

## Table of Contents
- [Installation Instructions](#installation-instructions)
- [Usage](#usage)
- [Future Improvements](#future-improvements)

## Installation Instructions
1. Clone this repo to a local directory.
2. Go to [TomorrowIO API Documentation](https://docs.tomorrow.io/reference/welcome), grab your free API key, and add it to `app.config`.
3. Run Docker Desktop.
4. Cd into the project directory.
5. Run `docker-compose up`.

## Usage
Go into Jupyter Lab at [http://localhost:8888](http://localhost:8888), import the files `notebook.ipynb` and `notebook.config`, and run all cells to visualize the results.

## Future Improvements
1. Implement scheduling to run the script automatically every hour. Attempted using cron in the Python app Dockerfile with no success.
2. Enhance handling of environmental variables and secrets.
3. Automate the importing of necessary files to the Jupyter environment.
4. Enrich the tables with additional information such as location city, state, etc.
