import sqlite3
import os
import json
from datetime import datetime

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(PROJECT_ROOT, "data", "tasks.db")

class TaskDatabase:
    def __init__(self):
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        self.conn = sqlite3.connect(DB_PATH)
        self._create_table()

    def _create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id TEXT PRIMARY KEY,
                description TEXT,
                status TEXT,
                agent TEXT,
                created_at TEXT,
                updated_at TEXT,
                commands_run TEXT
            )
        ''')
        self.conn.commit()

    def add_task(self, task_id, description, status="pending", agent="general"):
        timestamp = datetime.now().isoformat()
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO tasks (id, description, status, agent, created_at, updated_at, commands_run)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (task_id, description, status, agent, timestamp, timestamp, json.dumps([])))
        self.conn.commit()

    def update_status(self, task_id, status):
        timestamp = datetime.now().isoformat()
        cursor = self.conn.cursor()
        cursor.execute('''
            UPDATE tasks SET status = ?, updated_at = ? WHERE id = ?
        ''', (status, timestamp, task_id))
        self.conn.commit()

    def log_command(self, task_id, command):
        cursor = self.conn.cursor()
        cursor.execute('SELECT commands_run FROM tasks WHERE id = ?', (task_id,))
        row = cursor.fetchone()
        if row:
            cmds = json.loads(row[0])
            if command not in cmds:
                cmds.append(command)
                cursor.execute('UPDATE tasks SET commands_run = ? WHERE id = ?', (json.dumps(cmds), task_id))
                self.conn.commit()

    def get_active_tasks(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM tasks WHERE status IN ("pending", "doing", "in_progress")')
        return cursor.fetchall()

    def close(self):
        self.conn.close()

if __name__ == "__main__":
    db = TaskDatabase()
    print("Task Database initialized at:", DB_PATH)
    active = db.get_active_tasks()
    print(f"Found {len(active)} active tasks.")
    db.close()
