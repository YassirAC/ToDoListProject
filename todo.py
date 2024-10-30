import json
from datetime import datetime
import os

class Task:
    def __init__(self, title, description="", due_date=None, completed=False):
        self.title = title
        self.description = description
        self.created_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.due_date = due_date
        self.completed = completed

    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "created_date": self.created_date,
            "due_date": self.due_date,
            "completed": self.completed
        }

    @classmethod
    def from_dict(cls, data):
        task = cls(data["title"], data["description"], data["due_date"])
        task.created_date = data["created_date"]
        task.completed = data["completed"]
        return task

class TodoList:
    def __init__(self, filename="todo.json"):
        self.filename = filename
        self.tasks = []
        self.load_tasks()

    def load_tasks(self):
        """Load tasks from file"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    data = json.load(f)
                    self.tasks = [Task.from_dict(task_data) for task_data in data]
            except json.JSONDecodeError:
                print("Error reading file. Starting with empty task list.")
                self.tasks = []
        else:
            self.tasks = []

    def save_tasks(self):
        """Save tasks to file"""
        with open(self.filename, 'w') as f:
            data = [task.to_dict() for task in self.tasks]
            json.dump(data, f, indent=2)

    def add_task(self, title, description="", due_date=None):
        """Add a new task"""
        task = Task(title, description, due_date)
        self.tasks.append(task)
        self.save_tasks()
        return task

    def complete_task(self, index):
        """Mark a task as completed"""
        if 0 <= index < len(self.tasks):
            self.tasks[index].completed = True
            self.save_tasks()
            return True
        return False

    def delete_task(self, index):
        """Delete a task"""
        if 0 <= index < len(self.tasks):
            del self.tasks[index]
            self.save_tasks()
            return True
        return False

    def get_tasks(self, include_completed=True):
        """Get all tasks or only incomplete tasks"""
        if include_completed:
            return self.tasks
        return [task for task in self.tasks if not task.completed]

    def update_task(self, index, title=None, description=None, due_date=None):
        """Update task details"""
        if 0 <= index < len(self.tasks):
            task = self.tasks[index]
            if title:
                task.title = title
            if description:
                task.description = description
            if due_date:
                task.due_date = due_date
            self.save_tasks()
            return True
        return False

def main():
    todo_list = TodoList()
    
    while True:
        print("\n=== Todo List Manager ===")
        print("1. Add Task")
        print("2. List Tasks")
        print("3. Complete Task")
        print("4. Delete Task")
        print("5. Update Task")
        print("6. View Task Details")
        print("7. Exit")
        
        choice = input("\nEnter your choice (1-7): ")
        
        if choice == '1':
            title = input("Enter task title: ")
            description = input("Enter task description (optional): ")
            due_date = input("Enter due date (YYYY-MM-DD) (optional): ")
            if due_date == "":
                due_date = None
            todo_list.add_task(title, description, due_date)
            print("Task added successfully!")

        elif choice == '2':
            tasks = todo_list.get_tasks()
            if not tasks:
                print("No tasks found.")
            else:
                print("\nCurrent Tasks:")
                for i, task in enumerate(tasks):
                    status = "✓" if task.completed else " "
                    print(f"{i + 1}. [{status}] {task.title}")

        elif choice == '3':
            tasks = todo_list.get_tasks()
            if not tasks:
                print("No tasks found.")
                continue
                
            for i, task in enumerate(tasks):
                status = "✓" if task.completed else " "
                print(f"{i + 1}. [{status}] {task.title}")
                
            try:
                index = int(input("Enter task number to complete: ")) - 1
                if todo_list.complete_task(index):
                    print("Task marked as completed!")
                else:
                    print("Invalid task number.")
            except ValueError:
                print("Please enter a valid number.")

        elif choice == '4':
            tasks = todo_list.get_tasks()
            if not tasks:
                print("No tasks found.")
                continue
                
            for i, task in enumerate(tasks):
                status = "✓" if task.completed else " "
                print(f"{i + 1}. [{status}] {task.title}")
                
            try:
                index = int(input("Enter task number to delete: ")) - 1
                if todo_list.delete_task(index):
                    print("Task deleted successfully!")
                else:
                    print("Invalid task number.")
            except ValueError:
                print("Please enter a valid number.")

        elif choice == '5':
            tasks = todo_list.get_tasks()
            if not tasks:
                print("No tasks found.")
                continue
                
            for i, task in enumerate(tasks):
                status = "✓" if task.completed else " "
                print(f"{i + 1}. [{status}] {task.title}")
                
            try:
                index = int(input("Enter task number to update: ")) - 1
                title = input("Enter new title (or press Enter to skip): ")
                description = input("Enter new description (or press Enter to skip): ")
                due_date = input("Enter new due date (YYYY-MM-DD) (or press Enter to skip): ")
                
                if todo_list.update_task(index, 
                                       title if title else None,
                                       description if description else None,
                                       due_date if due_date else None):
                    print("Task updated successfully!")
                else:
                    print("Invalid task number.")
            except ValueError:
                print("Please enter a valid number.")

        elif choice == '6':
            tasks = todo_list.get_tasks()
            if not tasks:
                print("No tasks found.")
                continue
                
            for i, task in enumerate(tasks):
                status = "✓" if task.completed else " "
                print(f"{i + 1}. [{status}] {task.title}")
                
            try:
                index = int(input("Enter task number to view details: ")) - 1
                if 0 <= index < len(tasks):
                    task = tasks[index]
                    print("\nTask Details:")
                    print(f"Title: {task.title}")
                    print(f"Description: {task.description}")
                    print(f"Created: {task.created_date}")
                    print(f"Due Date: {task.due_date or 'Not set'}")
                    print(f"Status: {'Completed' if task.completed else 'Pending'}")
                else:
                    print("Invalid task number.")
            except ValueError:
                print("Please enter a valid number.")

        elif choice == '7':
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()