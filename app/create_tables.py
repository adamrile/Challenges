import psycopg2
import sys
import os
from os import environ
from dotenv import load_dotenv
import psycopg2.extras

load_dotenv()  # Load the environment variables from .env file

config = {
    "DATABASE_USERNAME": os.environ.get("DATABASE_USERNAME"),
    "DATABASE_IP": os.environ.get("DATABASE_IP"),
    "DATABASE_PORT": os.environ.get("DATABASE_PORT"),
    "DATABASE_NAME": os.environ.get("DATABASE_NAME")
}

def get_db_connection():
    """connects to the sql database using the psycopg import"""
    try:
        conn = psycopg2.connect(
            user=environ.get("DATABASE_USERNAME"),
            host=environ.get("DATABASE_IP"),
            port=environ.get("DATABASE_PORT"),
            database=environ.get("DATABASE_NAME"),
        )
        return conn
    except ConnectionError as err:
        print("Error connecting to database:", err)
        return None


def drop_table():
    # Connect to the database
    conn = get_db_connection()

    # Open a cursor to perform database operations
    cur = conn.cursor()

    # Drop the dim_teams table
    cur.execute("DROP TABLE IF EXISTS dim_teams cascade")
    # Drop the dim_competitions table
    cur.execute("DROP TABLE IF EXISTS dim_competitions cascade")
    # Drop the fact_competitions table
    cur.execute("DROP TABLE IF EXISTS fact_competitions cascade")

    # Commit the changes
    conn.commit()

    # Close the cursor and database connection
    cur.close()
    conn.close()



def create_tables():
    # Connect to the database
    conn = get_db_connection()

    # Open a cursor to perform database operations
    cur = conn.cursor()

    # SQL commands to create tables
    create_dim_teams = """
    CREATE TABLE IF NOT EXISTS dim_teams (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL
    )
    """

    create_dim_competitions = """
    CREATE TABLE IF NOT EXISTS dim_competitions (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL
    )
    """

    create_fact_competitions = """
    CREATE TABLE IF NOT EXISTS fact_competitions (
        competition_id INTEGER REFERENCES dim_competitions (id),
        team_id INTEGER REFERENCES dim_teams (id),
        PRIMARY KEY (competition_id, team_id)
    )
    """
    # Execute the SQL commands to create tables
    cur.execute(create_dim_teams)
    cur.execute(create_dim_competitions)
    cur.execute(create_fact_competitions)

    # Commit the changes
    conn.commit()

    # Close the cursor and database connection
    cur.close()
    conn.close()


if __name__ == "__main__":
    create_tables()
    #drop_table()

