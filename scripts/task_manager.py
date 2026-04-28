import chromadb  # pyre-ignore[21]
import uuid
from datetime import datetime
import os
import argparse

# Configuration
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(PROJECT_ROOT, "data", "chroma_db")

class TaskManager:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=DB_PATH)
        self.collection = self.client.get_or_create_collection("tasks")

    def add_task(self, description, priority="medium", agent="general"):
        task_id = str(uuid.uuid4()).split("-")[0]
        timestamp = datetime.now().isoformat()
        
        metadata = {
            "task_id": task_id,
            "status": "pending",
            "priority": priority,
            "agent": agent,
            "created_at": timestamp,
            "updated_at": timestamp
        }
        
        self.collection.add(
            ids=[task_id],
            documents=[description],
            metadatas=[metadata]
        )
        return task_id

    def list_tasks(self, status=None):
        where_clause = {}
        if status:
            where_clause = {"status": status}
            
        results = self.collection.get(where=where_clause)
        tasks = []
        for i in range(len(results["ids"])):
            tasks.append({
                "id": results["ids"][i],
                "description": results["documents"][i],
                "metadata": results["metadatas"][i]
            })
        return tasks

    def update_task_status(self, task_id, status):
        results = self.collection.get(ids=[task_id])
        if not results["ids"]:
            return False
            
        metadata = results["metadatas"][0]
        metadata["status"] = status
        metadata["updated_at"] = datetime.now().isoformat()
        
        self.collection.update(
            ids=[task_id],
            metadatas=[metadata]
        )
        return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Warrior Task Manager")
    parser.add_argument("--add", help="Task description")
    parser.add_argument("--priority", default="medium", choices=["low", "medium", "high", "critical"])
    parser.add_argument("--list", action="store_true", help="List all pending tasks")
    parser.add_argument("--status", help="Filter by status")
    parser.add_argument("--update", help="Task ID to update")
    parser.add_argument("--set-status", help="New status for the task")
    
    args = parser.parse_args()
    manager = TaskManager()
    
    if args.add:
        tid = manager.add_task(args.add, args.priority)
        print(f"Task added: [{tid}] {args.add}")
    elif args.list:
        tasks = manager.list_tasks(args.status)
        if not tasks:
            print("No tasks found.")
        for t in tasks:
            m = t["metadata"]
            print(f"[{t['id']}] ({m['status']}) [{m['priority'].upper()}] {t['description']}")
    elif args.update and args.set_status:
        if manager.update_task_status(args.update, args.set_status):
            print(f"Task {args.update} updated to {args.set_status}")
        else:
            print(f"Task {args.update} not found.")
