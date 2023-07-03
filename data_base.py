import pandas as pd
import sqlite3


def create_db():
    try:
        conn = sqlite3.connect("weather.db")
        with open("grid_weather_data.sql", "r") as file:
            sql_scripts = file.read()
    
        cursor = conn.cursor()
        cursor.executescript(sql_scripts)
        conn.close()
    except sqlite3.OperationalError:
        print("DB already exist!")


def db_connection():
    conn = sqlite3.connect("weather.db")
    return conn

def make_query(db_query):
    conn = db_connection()
    data = pd.read_sql_query(db_query, conn)
    conn.close()
    return data

def delete_query(db_query):
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute(db_query)
    conn.commit()
    conn.close()

def add_query(db_query, values):
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute(db_query, values)
    conn.commit()
    conn.close()

def update_query(db_query, values):
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute(db_query, values)
    conn.commit()
    conn.close()

def read_grid_weather_json():
    with open("grid_weather.json", "r") as file:
        file_data = file.read()
    cities = pd.read_json(file_data)
    return cities

def get_cities_ids_names():
    query = """
        SELECT DISTINCT cod_city
        FROM grid_weather_data
    """
    data = make_query(query)
    cities_name = read_grid_weather_json()
    cities_name = data.merge(cities_name, "left", "cod_city")
    cities_name = cities_name[["cod_city", "name_station"]].to_json()
    return cities_name

def get_weather_data(
        id: int, 
        year: str=0, 
        month: str=0, 
        day: str=0
        ):
    query = f"""
        SELECT * 
        FROM grid_weather_data
        WHERE cod_city = '{id}'
        {f"AND strftime('%Y', date) = '{year}'" if int(year) > 0 else " "}
        {f"AND strftime('%m', date) = '{month}'" if int(month) > 0 else " "}
        {f"AND strftime('%d', date) = '{day}'" if int(day) > 0 else " "}
    """

    data = make_query(query)
    return data.to_json()

def delete_weather_data(
        id: int, 
        year: str=0, 
        month: str=0, 
        day: str=0
        ):
    data = get_weather_data(id, year, month, day)
    if pd.read_json(data).empty:
        message = "Data not found"
        status_code = 404
        return message, '{}', status_code
    
    query = f"""
        DELETE FROM grid_weather_data
        WHERE cod_city = '{id}'
        {f"AND strftime('%Y', date) = '{year}'" if int(year) > 0 else " "}
        {f"AND strftime('%m', date) = '{month}'" if int(month) > 0 else " "}
        {f"AND strftime('%d', date) = '{day}'" if int(day) > 0 else " "}
    """
    delete_query(query)
    message = "Data removed!"
    status_code = 200
    
    return message, data, status_code

def add_weather_data( 
        id: int,
        date: str,
        precipitation: int,
        high_temperature: int,
        relative_humidity: int,
        evaporation: int
        ):
    query = """
        INSERT INTO grid_weather_data (cod_city, date, precipitation, high_temperature, relative_humidity, evaporation) 
        VALUES (?, ?, ?, ?, ?, ?)
    """
    values = (id, date, precipitation, high_temperature, relative_humidity, evaporation)
    add_query(query, values)

    verify_query = f"""
        SELECT *
        FROM grid_weather_data
        WHERE cod_city = {id}
        AND date = '{date}'
    """
    data = make_query(verify_query)
    return data.to_json()

def update_weather_data(
        id: int,
        date: str,
        precipitation: int,
        high_temperature: int,
        relative_humidity: int,
        evaporation: int
):
    query = """
        UPDATE grid_weather_data SET precipitation = ?,
        high_temperature = ?,
        relative_humidity = ?,
        evaporation = ?
        WHERE cod_city = ?
        AND date = ?
    """

    values = (precipitation, high_temperature, relative_humidity, evaporation, id, date)
    update_query(query, values)

    verify_query = f"""
        SELECT *
        FROM grid_weather_data
        WHERE cod_city = {id}
        AND date = '{date}'
    """
    data = make_query(verify_query)
    if data.empty:
        message = "Data not found"
        status_code = 404
        return message, '{}', status_code
    
    message = "Data updated"
    status_code = 200
    return message, data.to_json(), status_code
