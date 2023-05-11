"""
Programme to connect to football API and return a summary of the
number of teams in each competition
"""
import time
import os
import csv
import json
import requests
from create_tables import get_db_connection

COMP_DATA = './output/competition_data'
TEAMS_DATA = './output/teams'
OUTPUT_CSV = './output/output_csv'

def fetch_data(url: str, headers: str = None) -> dict:
    """Fetches data from the given URL with the given headers and
    returns the response JSON"""
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data
    return f"Error: {response.status_code}"

def ingest_comp_data(url: str, headers: str = None) -> tuple:
    """Ingests the competition data from the API and returns the data
    in JSON format and list of competition codes"""
    data = fetch_data(url, headers)
    competition_code = [comp["code"] for comp in data["competitions"]]
    return competition_code, data

def ingest_team_data(url: str, headers: str = None) -> dict:
    """Ingests team data using the team_url in the main function and
    returns the data in JSON format"""
    return fetch_data(url, headers)


def insert_comp_data(comp_data: list) -> str:
    """This function collects the comp_ids and comp_names for all
    football competitions extracted from the API then inserts it into
    the dims_competition table"""
    conn = get_db_connection()
    cur = conn.cursor()
    # Insert data into dim_teams table
    for comp in comp_data["competitions"]:
        comp_id = comp["id"]
        comp_name = comp["name"]

        # Check if the team already exists in the dim_teams table
        # query = "SELECT id FROM dim_competitions WHERE id = %s"
        table = "SELECT * FROM dim_competitions"

        query = "SELECT id FROM dim_competitions WHERE id = %s"
        cur.execute(query, (comp_id,))
        result = cur.fetchone()
        if result is not None:
            print(f"Competition {comp_name} (id {comp_id}) already exists in table")
        else:
            cur.execute("INSERT INTO dim_competitions (id, name) VALUES \
                    (%s, %s)", (comp_id, comp_name))
            print(f"{comp_name} (id {comp_id}) inserted into dim_competitions table")

    conn.commit()
    cur.close()
    conn.close()

def insert_team_data(team_data: list, comp_id: list) -> str:
    """This function collects team names and team IDs from the API data
    then performs an SQL execute to insert the respective data into
    dim_teams table as well as the fact_competitions table by inserting
    the comp_id that is assigned to a particular team"""

    conn = get_db_connection()
    cur = conn.cursor()

    # Insert data into dim_teams table
    for team in team_data["teams"]:
        team_id = team["id"]
        team_name = team["name"]

        # Check if the team already exists in the dim_teams table
        cur.execute("SELECT id FROM dim_teams WHERE id = %s", (team_id,))
        result = cur.fetchone()
        # print(result)
        if result is not None:
            print(f"Team {team_name} (id {team_id}) already exists in dim_teams table")
        else:
            cur.execute("INSERT INTO dim_teams (id, name) VALUES (%s, %s)", (team_id, team_name))
            print(f"Team {team_name} (id {team_id}) inserted into dim_teams table")

        # Insert data into fact_competitions table
        cur.execute("SELECT id FROM dim_competitions WHERE id = %s", (comp_id,))
        result = cur.fetchone()

        if result is not None:
            cur.execute("SELECT 1 FROM fact_competitions WHERE competition_id = %s AND team_id = %s", (comp_id, team_id))
            result = cur.fetchone()
            if result is not None:
                print(f"Team {team_name} (id {team_id}) already exists for competition id {comp_id} in fact_competitions")
            else:
                cur.execute("INSERT INTO fact_competitions (competition_id, team_id) VALUES (%s, %s)", (comp_id, team_id))
                print(f"{team_name} (id {team_id}) inserted into fact_competitions table")
        else:
            print(f"Competition id {comp_id} not found in dim_competitions table. Skipping team {team_name} (id {team_id})")

    conn.commit()
    cur.close()
    conn.close()


def output_summary_csv():
    """This function executes a SQL query to count the teams that play
    in particular football competitions"""
    conn = get_db_connection()
    cur = conn.cursor()
    query = '''
            SELECT d.name AS competition, COUNT(*) AS num_teams
            FROM fact_competitions f
            JOIN dim_competitions d ON f.competition_id = d.id
            GROUP BY d.name
            ORDER BY num_teams DESC
            '''
    cur.execute(query)

    if not os.path.exists(OUTPUT_CSV):
        os.makedirs(OUTPUT_CSV)

    output_file = os.path.join(OUTPUT_CSV, 'summary.csv')
    with open(output_file, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows([['Competition', 'Number of Teams']])
        for row in cur.fetchall():
            writer.writerow(row)

    conn.commit()
    cur.close()
    conn.close()

def main():
    """Main function that performs the objective of the programme"""
    pause_time = 6
    comp_url = 'https://api.football-data.org/v4/competitions'
    headers = {'X-Auth-Token': '041904737e094e1f9b765fb9ba79d905'}
    codes, comp_data = ingest_comp_data(comp_url, headers=headers)
    insert_comp_data(comp_data)

    if not os.path.exists(COMP_DATA):
        os.makedirs(COMP_DATA)

    competition_file = os.path.join(COMP_DATA, 'competitions.json')
    with open(competition_file, 'w') as file:
        json.dump(comp_data, file)

    #using the competition code to locate respective team API data
    for code in codes:
        team_url = f"http://api.football-data.org/v4/competitions/{code}/teams"
        team_data = ingest_team_data(team_url, headers=headers)
        if team_data:
            insert_team_data(team_data, comp_id=comp_data["competitions"][codes.index(code)]["id"])

            # Create a directory for the competition if it doesn't exist
            competition_dir = os.path.join(TEAMS_DATA, code)
            if not os.path.isdir(competition_dir):
                os.makedirs(competition_dir)

            # Create a new file for the team data if it doesn't exist
            teams_file = os.path.join(competition_dir, 'teams.json')
            if not os.path.isfile(teams_file):
                with open(teams_file, 'w') as file:
                    file.write(str(team_data))

            # API Throttle control: 6 second pause
            time.sleep(pause_time)

    output_summary_csv()

if __name__ == "__main__":
    main()
