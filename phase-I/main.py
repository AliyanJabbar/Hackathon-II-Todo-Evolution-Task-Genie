from todo import TodoApp

def main():
    app = TodoApp()
    actions = {
        "1": "Add Task",
        "2": "View Tasks",
        "3": "Update Task",
        "4": "Delete Task",
        "5": "Mark Complete",
        "6": "Exit"
    }

    while True:
        print("\n=== Todo App ===")
        for key, action in actions.items():
            print(f"{key}. {action}")

        choice = input("Select an option: ")

        if choice == "1":
            title = input("Enter task title: ")
            description = input("Enter task description: ")
            app.add_task(title, description)
        elif choice == "2":
            app.view_tasks()
        elif choice == "3":
            task_id = int(input("Enter task ID to update: "))
            title = input("Enter new title (leave blank to skip): ")
            description = input("Enter new description (leave blank to skip): ")
            app.update_task(task_id, title if title else None, description if description else None)
        elif choice == "4":
            task_id = int(input("Enter task ID to delete: "))
            app.delete_task(task_id)
        elif choice == "5":
            task_id = int(input("Enter task ID to mark complete/incomplete: "))
            completed_input = input("Mark as complete? (y/n): ").lower()
            completed = True if completed_input == "y" else False
            app.mark_complete(task_id, completed)
        elif choice == "6":
            print("Exiting Todo App. Goodbye!")
            break
        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    main()
