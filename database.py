import sqlite3
import json
import os

DATABASE_FILE = "digital_toolbox.db"

def get_db_connection():
    """Establishes and returns a connection to the SQLite database."""
    conn = sqlite3.connect(DATABASE_FILE)
    # This allows you to access columns by name
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """
    Initializes the database and creates the necessary tables if they
    do not already exist.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create a 'users' table.
    # The 'preferences' column will store a JSON string.
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            preferences TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

# --- UserPreferences now lives in the database module ---
class UserPreferences:
    def __init__(self, username):
        self.username = username
        self.conn = get_db_connection()
        # Load or create the user on initialization
        self.preferences = self._load_or_create_user()

    def _load_or_create_user(self):
        """
        Loads user preferences from the database. If the user doesn't exist,
        creates a new entry with default preferences.
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT preferences FROM users WHERE username = ?", (self.username,))
        row = cursor.fetchone()
        
        if row:
            # User exists, load their preferences
            # The preferences are stored as a JSON string, so we parse it
            return json.loads(row['preferences'])
        else:
            # User does not exist, create them with empty preferences
            default_prefs = {}
            # Convert the dictionary to a JSON string for storage
            prefs_json = json.dumps(default_prefs)
            cursor.execute("INSERT INTO users (username, preferences) VALUES (?, ?)",
                           (self.username, prefs_json))
            self.conn.commit()
            return default_prefs

    def get_preference(self, tool_name, key, default=None):
        """Gets a specific preference value for a tool."""
        return self.preferences.get(tool_name, {}).get(key, default)

    def set_preference(self, tool_name, key, value):
        """Sets a specific preference value and saves it to the database."""
        if tool_name not in self.preferences:
            self.preferences[tool_name] = {}
        self.preferences[tool_name][key] = value
        
        # Save the entire updated preferences dictionary back to the DB
        prefs_json = json.dumps(self.preferences)
        cursor = self.conn.cursor()
        cursor.execute("UPDATE users SET preferences = ? WHERE username = ?",
                       (prefs_json, self.username))
        self.conn.commit()

    def close_connection(self):
        """Closes the database connection."""
        if self.conn:
            self.conn.close()