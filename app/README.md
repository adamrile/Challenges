# PostgreSQL Database Management Python Script

This `create_tables.py` Python script allows you to interact with a PostgreSQL database by providing functionality to connect to the database, create tables and drop tables. This script uses the `psycopg2` module to connect to the database.

## Installation

You will need to install the following Python packages:

- `psycopg2`: This package is a PostgreSQL database adapter for Python.
- `python-dotenv`: This package is used to read key-value pairs from a .env file and add them to environment variable.

You can install these packages using pip:

pip install psycopg2 python-dotenv

## Usage

This script is designed to be run from the command line.

Before running the script, you need to set up a `.env` file in the same directory as the script with the following environment variables:

- `DATABASE_USERNAME`: The username of the PostgreSQL database.
- `DATABASE_IP`: The IP address of the PostgreSQL database.
- `DATABASE_PORT`: The port number of the PostgreSQL database.
- `DATABASE_NAME`: The name of the PostgreSQL database.

Here is an example of what the `.env` file might look like:

```
DATABASE_USERNAME=your_username
DATABASE_IP=127.0.0.1
DATABASE_PORT=5432
DATABASE_NAME=your_database_name
```

To run the script, navigate to the directory containing the script and type:

python your_script_name.py

The script will attempt to connect to the database and create three tables:

- `dim_teams`: A table to store team data.
- `dim_competitions`: A table to store competition data.
- `fact_competitions`: A fact table that references the `dim_competitions` and `dim_teams` tables.

If you want to drop the tables, you can uncomment the `drop_table()` function call in the `if __name__ == "__main__":` block at the end of the script.

## Functions

- `get_db_connection()`: Connects to the PostgreSQL database using the credentials provided in the `.env` file. Returns a connection object if successful, otherwise prints an error message and returns `None`.

- `drop_table()`: Drops the `dim_teams`, `dim_competitions` and `fact_competitions` tables from the database if they exist.

- `create_tables()`: Creates the `dim_teams`, `dim_competitions` and `fact_competitions` tables in the database if they don't already exist.

## Troubleshooting

If you encounter an error when running the script, make sure that:

- The PostgreSQL server is running and accessible at the IP address and port number specified in the `.env` file.
- The username and database name provided in the `.env` file are correct and the user has the necessary permissions to create and drop tables in the database.
- The Python packages `psycopg2` and `python-dotenv` are installed in your Python environment.
