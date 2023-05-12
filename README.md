## Football API Data Ingestion

This repository contains a Python script that simulates a data pipeline where your application will ingest data from an API, store the files, transform the data into tabular form, and load the data into a relational database. Finally, you will export a summary of the data into a CSV file.

# Features

Connects to the football API and fetches competition and team data
Inserts competition and team data into a database
Generates a summary CSV file containing the number of teams in each competition

# Requirements

- Python 3.6 or later
- requests library
- time library
- os library 
- csv
- json
- PostgreSQL database

# Setup

1. Clone the repository.
2. Obtain an API key from the Football-Data API website.
3. Create a .env file in the root directory of the project, and add the following lines:

-`DATABASE_USERNAME`=<your-username>
-`DATABASE_IP`=<your-IP>
-`DATABASE_HOST`=<your-db>
-`DATABASE_PORT`=<your-port>
-`DATABASE_NAME`=<your-db-name>
-`DATABASE_PASSWORD`=<your-db-password>

4. Install the required Python packages by running pip install -r requirements.txt
5. Create the tables in the Postgres database by running python create_tables.py

# Installation

1. Clone the repository:

git clone https://github.com/yourusername/football-api-data-ingestion.git
cd football-api-data-ingestion

2. Install the required packages:

pip install -r requirements.txt

3. Set up the PostgreSQL database 'football' and configure the connection details in create_tables.py file.

# Usage

1. Run the application by running python main.py.
2. The application will ingest data from the API endpoints, store the files, transform the data into tabular form, and load the data into a relational database.
3. A summary of the data is exported into a CSV file named summary.csv and is stored in the output/output_csv folder.

To run the tests, execute the following command in your terminal:

- pytest tests.py

# Files

main.py: The main script that connects to the football API, fetches competition and team data, and processes it.

create_tables.py: Contains the get_db_connection() function to set up a connection to the PostgreSQL database.

# Explanation

The main.py script is the entry point for the application.
The create_tables.py script is used to create the tables in the Postgres database.
The fetch_data function in main.py is used to fetch data from the given URL with the given headers and returns the response JSON.
The ingest_comp_data function in main.py is used to ingest the competition data from the API and returns the data in JSON format and list of competition codes.
The ingest_team_data function in main.py is used to ingest team data using the team_url in the main function and returns the data in JSON format.
The insert_comp_data function in main.py is used to collect the comp_ids and comp_names for all football competitions extracted from the API then inserts it into the dims_competition table.
The insert_team_data function in main.py is used to collect team names and team IDs from the API data then performs an SQL execute to insert the respective data into dim_teams table as well as the fact_competitions table by inserting the comp_id that is assigned to a particular team.
The output_summary_csv function in main.py is used to execute a SQL query to count the teams that play in particular football competitions.
