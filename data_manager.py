import sqlite3
import json
import os
from datetime import datetime
import pandas as pd

class DataManager:
    """
    Manage data persistence with SQLite
    """
    def __init__(self, db_path='fcot_data.db'):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create analysis history table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS analysis_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                chemical_1 TEXT,
                chemical_2 TEXT,
                category_1 TEXT,
                category_2 TEXT,
                result TEXT,
                status TEXT
            )
        ''')
        
        # Create favorites table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS favorites (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                combination TEXT
            )
        ''')
        
        # Create notes table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                title TEXT,
                content TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_analysis(self, chem1, chem2, cat1, cat2, result, status):
        """Save analysis to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute('''
            INSERT INTO analysis_history 
            (timestamp, chemical_1, chemical_2, category_1, category_2, result, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (timestamp, chem1, chem2, cat1, cat2, result, status))
        
        conn.commit()
        conn.close()
    
    def get_all_analysis(self):
        """Get all analysis history"""
        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql_query('SELECT * FROM analysis_history', conn)
        conn.close()
        return df
    
    def save_favorite(self, combination):
        """Save favorite combination"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check if already exists
        cursor.execute('SELECT * FROM favorites WHERE combination = ?', (combination,))
        if cursor.fetchone() is None:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute('''
                INSERT INTO favorites (timestamp, combination)
                VALUES (?, ?)
            ''', (timestamp, combination))
            conn.commit()
        conn.close()
    
    def get_favorites(self):
        """Get all favorites"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT combination FROM favorites ORDER BY timestamp DESC')
        favorites = [row[0] for row in cursor.fetchall()]
        conn.close()
        return favorites
    
    def delete_favorite(self, combination):
        """Delete favorite"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM favorites WHERE combination = ?', (combination,))
        conn.commit()
        conn.close()
    
    def save_note(self, title, content):
        """Save note"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute('''
            INSERT INTO notes (timestamp, title, content)
            VALUES (?, ?, ?)
        ''', (timestamp, title, content))
        
        conn.commit()
        conn.close()
    
    def get_notes(self):
        """Get all notes"""
        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql_query('SELECT * FROM notes ORDER BY timestamp DESC', conn)
        conn.close()
        return df
    
    def export_to_json(self, filename=None):
        """Export all data to JSON"""
        if filename is None:
            filename = f"fcot_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        conn = sqlite3.connect(self.db_path)
        history_df = pd.read_sql_query('SELECT * FROM analysis_history', conn)
        favorites_df = pd.read_sql_query('SELECT * FROM favorites', conn)
        notes_df = pd.read_sql_query('SELECT * FROM notes', conn)
        conn.close()
        
        data = {
            'exported_at': datetime.now().isoformat(),
            'analysis_history': history_df.to_dict('records'),
            'favorites': favorites_df.to_dict('records'),
            'notes': notes_df.to_dict('records')
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        return filename
    
    def get_statistics(self):
        """Get analysis statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM analysis_history')
        total_analysis = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM analysis_history WHERE status LIKE "%BERBAHAYA%"')
        dangerous_count = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM analysis_history WHERE status LIKE "%AMAN%"')
        safe_count = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM analysis_history WHERE status LIKE "%PERHATIAN%"')
        warning_count = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM favorites')
        total_favorites = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'total_analysis': total_analysis,
            'dangerous': dangerous_count,
            'safe': safe_count,
            'warning': warning_count,
            'favorites': total_favorites
        }
