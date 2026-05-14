"""
Database manager for LinkedIn Automator.
Handles all SQLite operations through a clean interface.
"""

import sqlite3
import sqlite3
import os
from datetime import datetime, timedelta


class DatabaseManager:
    def __init__(self, db_path=None):
        """
        Initialize database connection.
        
        Args:
            db_path: Path to SQLite file. Defaults to data/history.db
        """
        if db_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            db_path = os.path.join(base_dir, "data", "history.db")
        
        self.db_path = db_path
        # Ensure the data/ directory exists
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

    def connect(self):
        """Establish database connection."""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
            raise

    def get_connection(self):
        """
        Create a fresh database connection.
        
        Why not store the connection as self.conn?
        SQLite connections aren't thread-safe. Creating fresh 
        connections per operation is safer and avoids "database 
        is locked" errors. At our scale (12 posts/month), the 
        overhead is negligible.
        
        Returns:
            sqlite3.Connection with row_factory set to sqlite3.Row
        """
        conn = sqlite3.connect(self.db_path)
        # This makes rows behave like dicts: row['title'] instead of row[0]
        conn.row_factory = sqlite3.Row

        # Enable foreign key enforcement (SQLite has it OFF by default!)
        conn.execute("PRAGMA foreign_keys = ON")
        return conn
       
    def init_database(self):
        """
        Run schema.sql to create tables.
        Safe to call multiple times (IF NOT EXISTS).
        """
        schema_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "schema.sql"
        )
        with open(schema_path, "r") as f:
            sql_script = f.read()
        
        conn = self.get_connection()
        try:
            conn.executescript(sql_script)
            conn.commit()
            print("✅ Database initialized successfully")
        except sqlite3.Error as e:
            print(f"❌ Error initializing database: {e}")
            raise
        finally:
            conn.close()
        
    # ── Project Operations ──────────────────────────────

    def add_project(self, title, description, tech_stack=None, 
                github_url=None, key_learnings=None):
        """
        Insert a portfolio project.
        
        Returns:
            int: The ID of the newly inserted project
        """
        conn = self.get_connection()
        try:
            cursor = conn.execute(
            """
                INSERT INTO projects 
                    (title, description, tech_stack, github_url, key_learnings)
                VALUES (?, ?, ?, ?, ?)
            """,
            (title, description, tech_stack, github_url, key_learnings)
            )
            conn.commit()
            print(f"✅ Added project: {title}")
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"❌ Error adding project: {e}")
            raise
        finally:
            conn.close()

    def get_projects(self):
        """
        Get all projects, ordered by most recent first.
        """
        conn = self.get_connection()
        try:
            rows = conn.execute(
                "select * from projects order by created_at desc"
            ).fetchall()
            return [dict(row) for row in rows] 
        except sqlite3.Error as e:
            print(f"❌ Error getting projects: {e}")
            raise
        finally:
            conn.close()  

    def get_least_recent_posted_project(self):
        """
        Get the project that hasn't been posted about in the longest time.
        Projects never posted (NULL last_posted_at) come first.
        
        This is how the system decides "which project to showcase next."
        
        Returns:
            dict or None: The project, or None if no projects exist
            
        """
                
        conn = self.get_connection()
        try:
            row = conn.execute(
                """
                    SELECT * from projects
                    order by 
                        CASE WHEN last_posted_at IS NULL THEN 0 ELSE 1 END,
                        last_posted_at ASC
                    limit 1
                """
            ).fetchone()
            return dict(row) if row else None

        except sqlite3.Error as e:
            print(f"❌ Error getting least recent posted project: {e}")
            raise
        finally:
            conn.close()
        

    def update_project_posted_at(self, project_id, posted_at=None):
        if posted_at is None:
            posted_at = datetime.now()
        
        conn = self.get_connection()
        try:
            conn.execute(
                "UPDATE projects SET last_posted_at = ? WHERE id = ?",
                (posted_at, project_id)
            )
            conn.commit()
            print(f"✅ Updated project {project_id} last_posted_at to {posted_at}")
        except sqlite3.Error as e:
            print(f"❌ Error updating project {project_id}: {e}")
            raise
        finally:
            conn.close()
        
    # def update_project_posted(self):

        

        
        

            
    
            