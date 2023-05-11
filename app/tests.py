"""Tests for the main.py script"""
import os
import csv
import pytest
import requests
import requests_mock
from unittest.mock import Mock
from main import fetch_data,\
    ingest_comp_data, \
    insert_comp_data, \
    ingest_team_data, \
    insert_team_data, \
    output_summary_csv, \
    get_db_connection

@pytest.fixture
def mock_req():
    """pytest fixture to be used in test_ingest_comp_data and test_ingest_team_data"""
    with requests_mock.Mocker() as mock:
        yield mock

def test_fetch_data(monkeypatch):
    """Test ensure that the request is correctly formatted and that the
    function handles the response as expected."""
    url = "https://api.football-data.org/v4/competitions"
    headers = {"header_key": "header_value"}

    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"key": "value"}
    monkeypatch.setattr(requests, "get", Mock(return_value=mock_response))

    result = fetch_data(url, headers=headers)
    assert result == {"key": "value"}
    requests.get.assert_called_once_with(url, headers=headers)

def test_ingest_comp_data(mock_req):
    """The test checks that the ingest_comp_data function correctly
    processes the response data and returns the expected results."""
    url = 'https://api.football-data.org/v4/competitions'
    mock_data = {
        "competitions": [
            {"code": "TEST", "id": 1, "name": "Test Competition"}
        ]
    }
    mock_req.get(url, json=mock_data)

    codes, data = ingest_comp_data(url)
    assert codes == ["TEST"]
    assert data == mock_data


def test_ingest_team_data(mock_req):
    """ The test is to confirm that the ingest_team_data function correctly
    processes the response data and returns the expected data."""
    url = 'http://api.football-data.org/v4/competitions/TEST/teams'
    mock_data = {
        "teams": [
            {"id": 1, "name": "Test Team"}
        ]
    }
    mock_req.get(url, json=mock_data)

    data = ingest_team_data(url)
    assert data == mock_data


def test_insert_comp_data():
    """The test checks that the function correctly inserts data into the database
    and that the count of competitions in the database matches the expected number."""
    comp_data = {'competitions': [{'id': 2021, 'name': 'Premier League'},\
                                {'id': 2002, 'name': 'Bundesliga'}]}
    insert_comp_data(comp_data)
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM dim_competitions")
    result = cur.fetchone()[0]
    assert result == 13
    cur.close()
    conn.close()

def test_insert_team_data():
    """Test to check that the function correctly inserts the data into the database,
    and that the count of teams in the database is as expected. It also checks
    the count of rows in a fact table named fact_competitions."""
    team_data = {'teams': [{'id': 57, 'name': 'Arsenal'}, {'id': 61, 'name': 'Chelsea'}]}
    comp_id = 2021
    insert_team_data(team_data, comp_id)
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM dim_teams")
    result = cur.fetchone()[0]
    assert result == 303
    cur.execute("SELECT COUNT(*) FROM fact_competitions")
    result = cur.fetchone()[0]
    assert result == 336
    cur.close()
    conn.close()

def test_output_summary_csv():
    """The test checks that the function creates the CSV file as expected,
    and that the contents of the file match the expected results."""
    output_summary_csv()
    output_file = os.path.join('./output/output_csv', 'summary.csv')
    with open(output_file, 'r') as file:
        reader = csv.reader(file)
        assert next(reader) == ['Competition', 'Number of Teams']
        assert next(reader) == ['UEFA Champions League', '79']
        assert next(reader) == ['Copa Libertadores', '47']

