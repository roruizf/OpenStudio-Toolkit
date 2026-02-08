import logging
import os
import sqlite3
from collections import namedtuple
from datetime import datetime, timedelta
from typing import Any

import pandas as pd

# Configure logger
logger = logging.getLogger(__name__)

# --- Internal Data Structures and Constants ---
Variable = namedtuple("Variable", "key type units")

# Frequency constants
TS = "timestep"
H = "hourly"
D = "daily"
M = "monthly"
A = "annual"
RP = "runperiod"

# --- Internal Helper Functions ---

def _to_sql_frequency(eso_frequency: str) -> str | None:
    """
    Convert short frequency names to SQL-compatible reporting names.

    Parameters:
    - eso_frequency (str): Short frequency name (e.g., 'hourly').

    Returns:
    - Optional[str]: SQL string for reporting frequency, or None if invalid.
    """
    frequencies = {
        TS: "Zone Timestep", H: "Hourly", D: "Daily",
        M: "Monthly", RP: "Run Period", A: "Annual"
    }
    return frequencies.get(eso_frequency.lower())

def _eso_to_sql_variable(variable: Variable) -> dict[str, str]:
    """
    Convert a Variable namedtuple to a dictionary for SQL queries.

    Parameters:
    - variable (Variable): The variable request.

    Returns:
    - Dict[str, str]: Dictionary mapping SQL column names to request values.
    """
    sql_columns = ["KeyValue", "Name", "Units"]
    return {col: val for val, col in zip(variable, sql_columns) if val is not None}

def _data_dict_statement(columns: list[str], alike: bool) -> str:
    """
    Construct the SELECT statement for the ReportDataDictionary table.

    Parameters:
    - columns (List[str]): Columns to include in WHERE clause.
    - alike (bool): Whether to use LIKE for partial matches.

    Returns:
    - str: SQL statement string.
    """
    statement = "SELECT ReportDataDictionaryIndex, KeyValue, Name, Units FROM ReportDataDictionary WHERE ReportingFrequency = ?"
    eq_operator = " LIKE ?" if alike else " = ?"
    if columns:
        statement += " AND " + " AND ".join([f"{col}{eq_operator}" for col in columns])
    return statement

def _fetch_data_dict_rows(conn: sqlite3.Connection, variable: Variable, sql_frequency: str, alike: bool):
    """
    Execute SQL query to find matching time series in the ReportDataDictionary.

    Parameters:
    - conn (sqlite3.Connection): SQLite connection.
    - variable (Variable): Search criteria.
    - sql_frequency (str): Target reporting frequency.
    - alike (bool): Whether to use LIKE.

    Returns:
    - sqlite3.Cursor: Result cursor.
    """
    sql_variable = _eso_to_sql_variable(variable)
    statement = _data_dict_statement(list(sql_variable.keys()), alike)
    
    values = tuple(f"%{v}%" for v in sql_variable.values()) if alike else tuple(sql_variable.values())
    params = (sql_frequency,) + values
    
    return conn.execute(statement, params)

def _get_outputs(conn: sqlite3.Connection, id_: int) -> list[float]:
    """
    Retrieve all numerical values for a specific time series entry.

    Parameters:
    - conn (sqlite3.Connection): SQLite connection.
    - id_ (int): ReportDataDictionaryIndex.

    Returns:
    - List[float]: List of output values.
    """
    statement = "SELECT Value FROM ReportData WHERE ReportDataDictionaryIndex = ?"
    return [r[0] for r in conn.execute(statement, (id_,))]

def _get_timestamps(conn: sqlite3.Connection, frequency: str) -> list[datetime]:
    """
    Retrieve and format timestamps for the specified frequency from the SQL database.

    Parameters:
    - conn (sqlite3.Connection): SQLite connection.
    - frequency (str): reporting frequency string.

    Returns:
    - List[datetime]: List of formatted datetime objects.
    """
    freq_map = {TS: -1, H: 1, D: 2, M: 3, RP: 4, A: 5}
    statement = f"SELECT Year, Month, Day, Hour, Minute FROM Time WHERE IntervalType = {freq_map.get(frequency.lower(), 1)}"
    
    timestamps = []
    for year, month, day, hour, minute in conn.execute(statement):
        # Handle cases where year is missing (default to standard EnergyPlus year if 0)
        eff_year = 2002 if year == 0 else year
        
        # EnergyPlus uses 24:00 to represent end of day; wrap to next day 00:00
        if hour == 24:
            ts = datetime(eff_year, month, day) + timedelta(days=1)
        else:
            ts = datetime(eff_year, month, day, hour, minute)
        timestamps.append(ts)
    return timestamps

# --- Main Task Functions ---

def validator(sql_path: str) -> dict[str, Any]:
    """
    Validate that the provided path exists and corresponds to a valid EnergyPlus SQL database.

    Parameters:
    - sql_path (str): Absolute path to the .sql file.

    Returns:
    - Dict[str, Any]: Status dictionary.
    """
    if not os.path.exists(sql_path):
        msg = f"ERROR: SQL file not found at: {sql_path}"
        logger.error(msg)
        return {"status": "ERROR", "messages": [msg]}
    
    try:
        conn = sqlite3.connect(sql_path)
        res = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='ReportData';").fetchone()
        conn.close()
        if not res:
            raise sqlite3.DatabaseError("Missing ReportData table.")
    except Exception as e:
        msg = f"ERROR: The file at {sql_path} is not a valid EnergyPlus SQL database. {str(e)}"
        logger.error(msg)
        return {"status": "ERROR", "messages": [msg]}

    logger.info(f"SQL file validated: {sql_path}")
    return {"status": "READY", "messages": ["OK: SQL file found and valid."]}

def run(
    sql_path: str,
    variables: list[Variable],
    frequency: str,
    alike: bool = False,
    start_date: datetime | None = None,
    end_date: datetime | None = None
    ) -> pd.DataFrame | None:
    """
    Extract specified time series data from an EnergyPlus SQL file into a pandas DataFrame.

    Parameters:
    - sql_path (str): Path to the EnergyPlus SQL file.
    - variables (List[Variable]): List of Variable namedtuples to extract.
    - frequency (str): Reporting frequency (e.g., 'hourly', 'daily').
    - alike (bool, optional): If True, use partial matching for variable names. Defaults to False.
    - start_date (datetime, optional): Start boundary for results filter.
    - end_date (datetime, optional): End boundary for results filter.

    Returns:
    - Optional[pd.DataFrame]: DataFrame with datetime index and matched variables, or None if no data is found.
    """
    logger.info(f"Starting extraction of '{frequency}' timeseries data from {sql_path}")
    
    conn = sqlite3.connect(sql_path)
    sql_freq = _to_sql_frequency(frequency)
    if not sql_freq:
        logger.error(f"Invalid frequency '{frequency}' provided.")
        conn.close()
        return None
    
    results_data = {}
    for var_req in variables:
        rows = _fetch_data_dict_rows(conn, var_req, sql_freq, alike)
        for id_, key, name, units in rows:
            col_name = f"{key}|{name}|{units}"
            results_data[col_name] = _get_outputs(conn, id_)

    if not results_data:
        logger.warning(f"No matching time series found for {variables} at {frequency} frequency.")
        conn.close()
        return None
        
    timestamps = _get_timestamps(conn, frequency)
    conn.close()
    
    # Align data lengths
    min_len = min(len(timestamps), min(len(v) for v in results_data.values()))
    
    df = pd.DataFrame({k: v[:min_len] for k, v in results_data.items()})
    df.index = timestamps[:min_len]
    
    # Filter by date range
    if start_date:
        df = df[df.index >= start_date]
    if end_date:
        df = df[df.index <= end_date]

    if df.empty:
        logger.warning("No data remains after applying date filters.")
        return None
    
    logger.info(f"Successfully extracted {len(df.columns)} time series.")
    return df