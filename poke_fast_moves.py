"""
This Python script web scrapes Pokemon Go PVE fast moves from gamepress.gg and inserts this data into MySQL
"""

# Install dependencies - "pip3 install -r requirements.txt"
import sys
import requests
from pyquery import PyQuery as pq
import mysql.connector

def clean_data(value):
    """
    Function to clean the web scraped data
    """
    value = value.strip() # Trim spaces at the beginning and end
    # If character is not a character, number, space, ., (, or ), remove the character
    return ''.join(char if char.isalnum() or char.isspace() or char in ('.', '(', ')') else '' for char in value)

def scrape_website(website):
    """
    Function to web scrape and return list of Pokemon Go PVE fast moves from gamepress.gg
    """
    try:
        # Adding timeout argument to requests.get
        print(website)
        response = requests.get(website, timeout = 30)  # Timeout value is in seconds, adjust as needed

        # Handle response
        if response.status_code == 200:
            print(response)
            #print(response.text)
            doc = pq(response.text)

            # Assume the information is inside a table with class 'views-table'
            # Within the table body find all rows containing the data
            pve_fast_moves_data = doc('table.views-table tbody tr')
            #print(pve_fast_moves_list)

            scraped_fast_moves = []

            for row in pve_fast_moves_data.items():
                # Extract table header data from each row
                name = clean_data(row('td[headers="view-title-table-column"]').text())
                move_type = clean_data(row('td[headers="view-field-move-element-table-column"]').text())
                power = clean_data(row('td[headers="view-field-move-damage-table-column"]').text())
                energy_per_use = clean_data(row('td[headers="view-field-energy-delta-table-column"]').text())
                dps = clean_data(row('td[headers="view-field-move-dps-table-column"]').text())
                eps = clean_data(row('td[headers="view-field-move-energy-per-second-table-column"]').text())
                cooldown = clean_data(row('td[headers="view-field-move-cooldown-table-column"]').text())

                # Append list of moveset traits
                scraped_fast_moves.append((name, move_type, power, energy_per_use, dps, eps, cooldown))
                #print(scraped_fast_moves)
            return scraped_fast_moves
        else:
            print("Failed to fetch data. Status code:", response.status_code)
            return None
    except requests.Timeout:
        print("Timeout occurred while fetching data from the website.")
        return None
    except requests.RequestException as e:
        print("An error occurred during the request:", e)
        return None
    except Exception as e:
        print("An error occurred:", e)
        return None

def connect_to_database(hostname, username, pwd):
    """
    Function to establish a connection to the MySQL database
    """
    try:
        conn = mysql.connector.connect(
            host=hostname,
            user=username,
            password=pwd
        )
        if conn.is_connected():
            print("Connected to the MySQL database")
            return conn
    except mysql.connector.Error as e:
        print("Error connecting to MySQL database:", e)
    return None

def insert_into_database(conn, data):
    """
    Function to create MySQL database and insert cleaned data
    """
    # Create the Pokemon Go database and table to store Pokemon Go Fast Moves
    try:
        cursor = conn.cursor()

        cursor.execute('CREATE DATABASE IF NOT EXISTS pokemon_go')

        cursor.execute('USE pokemon_go')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pokemon_go_fast_moves (
                name VARCHAR(255) PRIMARY KEY,
                move_type VARCHAR(255),
                power INT,
                energy_per_use INT,
                dps DECIMAL(4,2),
                eps DECIMAL(4,2),
                cooldown DECIMAL(4,2),
                insert_user VARCHAR(255),
                insert_date DATETIME,
                update_user VARCHAR(255),
                update_date DATETIME,
                INDEX idx_move_type (move_type)
            )
        ''')

        # Insert cleaned data into the MySQL database
        for entry in data:
            #print(entry)
            name, move_type, power, energy_per_use, dps, eps, cooldown = entry
            cursor.execute('''
                INSERT INTO pokemon_go_fast_moves (name, move_type, power, energy_per_use, dps, eps, cooldown, insert_user, insert_date, update_user, update_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW(), %s, NOW())

                ON DUPLICATE KEY UPDATE
                move_type = VALUES(move_type),
                power = VALUES(power),
                energy_per_use = VALUES(energy_per_use),
                dps = VALUES(dps),
                eps = VALUES(eps),
                cooldown = VALUES(cooldown),
                update_user = VALUES(update_user),
                update_date = NOW()
            ''', (name, move_type, power, energy_per_use, dps, eps, cooldown, USER, USER))
        conn.commit()
        print("Data inserted successfully.")
    except mysql.connector.Error as e:
        print("Error inserting data into MySQL database:", e)
    finally:
        if conn.is_connected():
            conn.close()

# Main script
if __name__ == "__main__":
    # Step 1: Prompt the user for database connection information
    HOST = input("Enter the host: ")
    USER = input("Enter the user: ")
    PASSWORD = input("Enter the password: ")

    # Step 2: Connect to MySQL database
    connection = connect_to_database(HOST, USER, PASSWORD)

    if not connection:
        # Connection failed, handle accordingly
        print("Unable to establish connection to the database. Exiting.")
        sys.exit(1)

    # Step 3: Scrape data from the website using PyQuery
    URL = 'https://gamepress.gg/pokemongo/pve-fast-moves'
    scraped_data = scrape_website(URL)

    if not scraped_data:
        print("No data scraped. Exiting.")
        sys.exit(1)

    # Step 4: Clean the data
    cleaned_data = [(clean_data(name), clean_data(move_type), clean_data(power), clean_data(energy_per_use),
                     clean_data(dps), clean_data(eps), clean_data(cooldown))
                    for name, move_type, power, energy_per_use, dps, eps, cooldown in scraped_data]

    # Step 5: Insert cleaned data into the MySQL database
    insert_into_database(connection, cleaned_data)
