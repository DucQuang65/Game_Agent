import argparse
import importlib
import sys


TaskManager = importlib.import_module("task_manager").TaskManager
TaskDatabase = importlib.import_module("task_db").TaskDatabase

def main():
    parser = argparse.ArgumentParser(description="Warrior CLI v4.1")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Add Task
    add_p = subparsers.add_parser("add", help="Add a new task")
    add_p.add_argument("description", help="Task description")
    add_p.add_argument("--priority", default="medium", choices=["low", "medium", "high", "critical"])

    # List Tasks
    subparsers.add_parser("list", help="List active tasks")

    # Resume Tasks
    subparsers.add_parser("resume", help="Resume in-progress tasks")

    # Update Task Status
    update_p = subparsers.add_parser("status", help="Update task status")
    update_p.add_argument("id", help="Task ID")
    update_p.add_argument("status", choices=["pending", "doing", "done", "blocked", "failed"])

    args = parser.parse_args()
    manager = TaskManager()
    db = TaskDatabase()

    if args.command == "add":
        # Add to both ChromaDB (semantic) and SQLite (execution)
        tid = manager.add_task(args.description, args.priority)
        db.add_task(tid, args.description, "pending")
        print(f"Task added: [{tid}] {args.description}")

    elif args.command == "list":
        tasks = db.get_active_tasks()
        if not tasks:
            print("No active tasks.")
        else:
            for task in tasks:
                print(task)

    elif args.command == "status":
        tid = args.id
        if manager.update_task_status(tid, args.status):
            print(f"Task [{tid}] updated to '{args.status}'.")
        else:
            print(f"Task [{tid}] not found.")
            
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
