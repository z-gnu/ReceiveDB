import sqlite3
import json

class Config:
    def __init__(self, config_file='config.json'):
        self._config_file = config_file
        self._config = self._read_config()
        self._create_properties()

    def _read_config(self):
        with open(self._config_file, 'r') as f:
            return json.load(f)

    def _create_properties(self):
        for key, value in self._config.items():
            setattr(self, key, value)

# Function to initialize the database
def init_db():
    conn = sqlite3.connect('received.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inspection_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            supplier TEXT,
            part_number TEXT,
            date TEXT,
            inspector TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Function to save data to the database
def save_to_db(data):
    conn = sqlite3.connect('received.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO inspection_data (supplier, part_number, date, inspector)
        VALUES (:supplier, :part_number, :date, :inspector)
    ''', data)
    conn.commit()
    conn.close()

# Function to search data in the database
def search_db(query):
    conn = sqlite3.connect('received.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT supplier, part_number, date, inspector
        FROM inspection_data
        WHERE supplier LIKE ?
        OR part_number LIKE ?
        OR date LIKE ?
        OR inspector LIKE ?
    ''', (f'%{query}%', f'%{query}%', f'%{query}%', f'%{query}%'))
    results = cursor.fetchall()
    conn.close()
    return results

# Initialize the database when the module is imported
init_db()
