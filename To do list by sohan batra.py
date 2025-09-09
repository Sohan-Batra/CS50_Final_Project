import json
import os
from datetime import datetime

# File to store tasks
tasks_file = "tasks.json"

# Load tasks from file
def load_tasks():
    # If the file exists, open it and load the list of tasks
    if os.path.exists(tasks_file):
        with open(tasks_file, "r") as f:
            return json.load(f)
    # If no file exists yet, return an empty list
    return []

# Save tasks to file
def save_tasks(tasks):
    # Save the current list of tasks to the file in JSON format
    with open(tasks_file, "w") as f:
        json.dump(tasks, f, indent=4)

# Show all tasks
def list_tasks(tasks):
    # If there are no tasks, inform the user
    if not tasks:
        print("No tasks found.")
        return
    # Otherwise, show all tasks with details like status, due date, and priority
    for i, task in enumerate(tasks, 1):
        status = "✔" if task.get("done") else "✘"  # Mark as done or not
        due = f" (Due: {task['due']})" if task.get("due") else ""  # Add due date if available
        priority = f" [Priority: {task['priority']}]" if task.get("priority") else ""  # Add priority if available
        print(f"{i}. {task['title']} {status}{due}{priority}")

# Get and validate due date input
def get_due_date():
    while True:
        due = input("Enter due date (YYYY-MM-DD, optional): ")
        if not due:  # allow empty input
            return None
        try:
            # Convert string to date object
            date_obj = datetime.strptime(due, "%Y-%m-%d")

            # Check year range (must be >= current year and <= 2100)
            current_year = datetime.today().year
            if not (current_year <= date_obj.year <= 2100):
                print(f"Year must be between {current_year} and 2100.")
                continue

            # Check if date is today or future
            today = datetime.today().date()
            if date_obj.date() < today:
                print("Due date cannot be in the past.")
                continue

            return due  # ✅ valid date, return it

        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")

# Add new task
def add_task(tasks):
    # Ask the user for task details
    title = input("Enter task: ")

    # Check for duplicate titles (case-insensitive)
    for task in tasks:
        if task["title"].lower() == title.lower():
            print("Task with this name already exists. Please use a different name.")
            return  # stop here without adding

    due = get_due_date()  # now with validation
    priority = input("Enter priority (high/medium/low, optional): ")

    # Create a dictionary for the task
    task = {"title": title, "done": False}
    if due:
        task["due"] = due
    if priority:
        task["priority"] = priority

    # Add task to the list and save it
    tasks.append(task)
    save_tasks(tasks)
    print("Task added!")

# Delete a task
def delete_task(tasks):
    # Show all tasks so the user can choose
    list_tasks(tasks)
    try:
        index = int(input("Enter task number to delete: ")) - 1
        # If the number is valid, remove the task
        if 0 <= index < len(tasks):
            removed = tasks.pop(index)
            save_tasks(tasks)
            print(f"Removed: {removed['title']}")
        else:
            print("Invalid number.")
    except ValueError:
        print("Please enter a valid number.")

# Mark a task as done
def mark_done(tasks):
    # Show all tasks so the user can choose
    list_tasks(tasks)
    try:
        index = int(input("Enter task number to mark as done: ")) - 1
        # If the number is valid, update the task as done
        if 0 <= index < len(tasks):
            tasks[index]["done"] = True
            save_tasks(tasks)
            print(f"Marked as done: {tasks[index]['title']}")
        else:
            print("Invalid number.")
    except ValueError:
        print("Please enter a valid number.")

# Main loop
def main():
    # Load existing tasks from the file when the program starts
    tasks = load_tasks()

    # Run the program until the user quits
    while True:
        print("\n--- To-Do List App ---")
        print("1. List tasks")
        print("2. Add task")
        print("3. Delete task")
        print("4. Mark task as done")
        print("5. Quit")
        choice = input("Choose an option: ")

        # Match the user's choice with the correct function
        if choice == "1":
            list_tasks(tasks)
        elif choice == "2":
            add_task(tasks)
        elif choice == "3":
            delete_task(tasks)
        elif choice == "4":
            mark_done(tasks)
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

# Run the program
if __name__ == "__main__":
    main()
