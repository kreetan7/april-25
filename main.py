#!/usr/bin/env python3
"""
Task Manager CLI Application
Author: Your Name
Description:
A simple but powerful command-line task manager with persistent storage.
Features:
- Add, update, delete tasks
- Mark tasks as complete
- Filter tasks
- JSON-based storage
"""

import json
import os
from datetime import datetime
from typing import List, Dict

DATA_FILE = "tasks.json"


class TaskManager:
    def __init__(self, file_path: str = DATA_FILE):
        self.file_path = file_path
        self.tasks: List[Dict] = self.load_tasks()

    def load_tasks(self) -> List[Dict]:
        if not os.path.exists(self.file_path):
            return []
        try:
            with open(self.file_path, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            print("⚠️ Corrupted data file. Starting fresh.")
            return []

    def save_tasks(self):
        with open(self.file_path, "w") as file:
            json.dump(self.tasks, file, indent=4)

    def add_task(self, title: str):
        task = {
            "id": len(self.tasks) + 1,
            "title": title,
            "completed": False,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.tasks.append(task)
        self.save_tasks()
        print("✅ Task added successfully.")

    def list_tasks(self):
        if not self.tasks:
            print("📭 No tasks found.")
            return

        for task in self.tasks:
            status = "✔" if task["completed"] else "✘"
            print(f"[{status}] {task['id']}: {task['title']} ({task['created_at']})")

    def complete_task(self, task_id: int):
        for task in self.tasks:
            if task["id"] == task_id:
                task["completed"] = True
                self.save_tasks()
                print("✅ Task marked as completed.")
                return
        print("❌ Task not found.")

    def delete_task(self, task_id: int):
        original_length = len(self.tasks)
        self.tasks = [t for t in self.tasks if t["id"] != task_id]

        if len(self.tasks) == original_length:
            print("❌ Task not found.")
        else:
            self.save_tasks()
            print("🗑 Task deleted successfully.")

    def filter_tasks(self, completed: bool):
        filtered = [t for t in self.tasks if t["completed"] == completed]
        if not filtered:
            print("📭 No matching tasks.")
            return

        for task in filtered:
            print(f"{task['id']}: {task['title']}")


def show_menu():
    print("\n=== TASK MANAGER ===")
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Complete Task")
    print("4. Delete Task")
    print("5. View Completed Tasks")
    print("6. View Pending Tasks")
    print("0. Exit")


def main():
    manager = TaskManager()

    while True:
        show_menu()
        choice = input("Select option: ").strip()

        if choice == "1":
            title = input("Enter task title: ").strip()
            if title:
                manager.add_task(title)
            else:
                print("❌ Title cannot be empty.")

        elif choice == "2":
            manager.list_tasks()

        elif choice == "3":
            try:
                task_id = int(input("Enter task ID: "))
                manager.complete_task(task_id)
            except ValueError:
                print("❌ Invalid input.")

        elif choice == "4":
            try:
                task_id = int(input("Enter task ID: "))
                manager.delete_task(task_id)
            except ValueError:
                print("❌ Invalid input.")

        elif choice == "5":
            manager.filter_tasks(True)

        elif choice == "6":
            manager.filter_tasks(False)

        elif choice == "0":
            print("👋 Exiting...")
            break

        else:
            print("❌ Invalid option. Try again.")


if __name__ == "__main__":
    main()