import json
import tkinter as tk
from tkinter import messagebox
import random
from collections import deque

# Load Command Database
def load_commands(file_path):
    """
    Load Vim commands database from a JSON file.
    """
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        messagebox.showerror("Error", f"File not found: {file_path}")
        exit(1)
    except json.JSONDecodeError:
        messagebox.showerror("Error", f"Invalid JSON format in: {file_path}")
        exit(1)

class VimPracticeApp:
    def __init__(self, root, commands):
        self.root = root
        self.commands = commands
        self.category = None
        self.tasks = deque()
        self.current_task = None
        self.performance = {}
        self.progress_tracker = {}
        self.green_tasks = []

        # Configure the root window
        self.root.title("Vim Practice Application")
        self.root.geometry("1000x700")
        self.root.configure(bg="#1e1e1e")

        # Progress Tracker
        self.progress_label = tk.Label(
            root, text="Progress: ", font=("Consolas", 14), bg="#1e1e1e", fg="#ffffff"
        )
        self.progress_label.pack(pady=10)

        # Header
        self.header_label = tk.Label(
            root, text="Vim Practice Application", font=("Consolas", 20, "bold"), fg="#ffffff", bg="#1e1e1e"
        )
        self.header_label.pack(pady=20)

        # Category Selection
        self.category_label = tk.Label(
            root, text="Select a Category:", font=("Consolas", 16), fg="#ffffff", bg="#1e1e1e"
        )
        self.category_label.pack(pady=10)

        self.category_list = tk.Listbox(
            root, font=("Consolas", 14), height=8, bg="#252526", fg="#ffffff", selectbackground="#007acc"
        )
        for category in commands.keys():
            self.category_list.insert(tk.END, category)
        self.category_list.pack(pady=10)

        self.start_button = tk.Button(
            root, text="Start", font=("Consolas", 14), bg="#007acc", fg="#ffffff", command=self.start_practice
        )
        self.start_button.pack(pady=10)

        # Practice Widgets
        self.task_label = tk.Label(
            root, text="", font=("Consolas", 14), fg="#ffffff", bg="#1e1e1e", wraplength=700
        )
        self.text_area = tk.Text(root, font=("Consolas", 12), width=80, height=15, bg="#252526", fg="#ffffff")
        self.command_entry = tk.Entry(root, font=("Consolas", 14), bg="#252526", fg="#ffffff")
        self.feedback_label = tk.Label(
            root, text="", font=("Consolas", 12), fg="#ff5555", bg="#1e1e1e", wraplength=700
        )
        self.hint_label = tk.Label(
            root, text="", font=("Consolas", 12), fg="#f1fa8c", bg="#1e1e1e", wraplength=700
        )
        self.solution_label = tk.Label(
            root, text="", font=("Consolas", 12), fg="#50fa7b", bg="#1e1e1e", wraplength=700
        )
        self.back_button = tk.Button(
            root, text="Back", font=("Consolas", 14), bg="#44475a", fg="#ffffff", command=self.go_back_to_categories
        )

        # Key bindings for hints and solutions
        self.root.bind("<Up>", lambda event: self.use_hint())
        self.root.bind("<Right>", lambda event: self.use_solution())
        self.root.bind("<KeyPress>", self.process_key)

    def start_practice(self):
        selected_index = self.category_list.curselection()
        if not selected_index:
            messagebox.showwarning("Warning", "Please select a category.")
            return

        self.category = self.category_list.get(selected_index)
        self.tasks = deque(self.commands[self.category])

        # Initialize performance and progress tracking
        for task in self.tasks:
            self.performance[task["task"]] = {"correct": 0, "attempts": 0, "required": 3}
            self.progress_tracker[task["task"]] = "red"  # Initially red (not learned)

        random.shuffle(self.tasks)
        self.current_task = None

        self.category_label.pack_forget()
        self.category_list.pack_forget()
        self.start_button.pack_forget()

        self.update_progress()
        self.task_label.pack(pady=10)
        self.text_area.pack(pady=10)
        self.command_entry.pack(pady=10)
        self.command_entry.bind("<Return>", lambda event: self.submit_command())
        self.hint_label.pack(pady=5)
        self.solution_label.pack(pady=5)
        self.feedback_label.pack(pady=10)
        self.back_button.pack(pady=10)

        self.display_task()

    def update_progress(self):
        """Update progress tracker."""
        learned = sum(1 for status in self.progress_tracker.values() if status == "green")
        learning = sum(1 for status in self.progress_tracker.values() if status == "yellow")
        not_learned = sum(1 for status in self.progress_tracker.values() if status == "red")

        self.progress_label.config(
            text=f"Progress: 🔴 {not_learned} | 🟡 {learning} | 🟢 {learned}",
            fg="#ffffff"
        )
        self.root.update_idletasks()

    def display_task(self):
        """Display the next task."""
        if self.tasks or self.green_tasks:
            if self.tasks:
                self.current_task = self.tasks.popleft()
            elif self.green_tasks:
                self.current_task = random.choice(self.green_tasks)

            self.task_label.config(text=f"Task: {self.current_task['task']}")
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, self.current_task.get("example", ""))
            self.command_entry.delete(0, tk.END)
            self.feedback_label.config(text="")
            self.hint_label.config(text="")
            self.solution_label.config(text="")
            self.update_progress()  # Ensure progress is updated when displaying a task
        else:
            self.end_practice()

    def submit_command(self):
        """Handle user input and task progression."""
        user_input = self.command_entry.get().strip()
        task = self.current_task["task"]
        correct_command = self.current_task["command"]

        self.performance[task]["attempts"] += 1

        if user_input.lower() == correct_command.lower():
            self.performance[task]["correct"] += 1
            correct_count = self.performance[task]["correct"]
            required = self.performance[task]["required"]

            if correct_count >= required:
                self.progress_tracker[task] = "green"
                if task not in self.green_tasks:
                    self.green_tasks.append(self.current_task)
            elif correct_count > 0:
                self.progress_tracker[task] = "yellow"
            else:
                self.progress_tracker[task] = "red"

            self.feedback_label.config(
                text=f"Correct! Task: {task} | Command: {correct_command}", fg="#57a64a"
            )

            if all(status == "green" for status in self.progress_tracker.values()):
                self.end_practice()
            else:
                self.root.after(200, self.display_task)
        else:
            self.progress_tracker[task] = "red"
            self.feedback_label.config(text=f"Incorrect! Try again or use a hint.", fg="#f44747")

        self.update_progress()  # Update progress after submitting command

    def use_hint(self):
        task = self.current_task["task"]
        self.performance[task]["required"] = max(self.performance[task]["required"], 5)
        self.hint_label.config(text=f"Hint: {self.current_task['hint']}")
        self.update_progress()  # Update progress when hint is used

    def use_solution(self):
        task = self.current_task["task"]
        self.performance[task]["required"] = max(self.performance[task]["required"], 7)
        self.solution_label.config(text=f"Solution: {self.current_task['command']}")
        self.update_progress()  # Update progress when solution is used

    def process_key(self, event):
        """Process all keypress events and detect Ctrl combinations."""
        if event.state & 0x0004 and event.keysym != "Control_L" and event.keysym != "Control_R":
            if event.keysym == "Alt_R":
                # AltGr (right alt) should behave as it normally does
                event.keysym = "ISO_Level3_Shift"
            else:
                keybind = f"CTRL-{event.keysym}"
                self.command_entry.delete(0, tk.END)
                self.command_entry.insert(0, keybind)
                self.submit_command()

    def go_back_to_categories(self):
        self.task_label.pack_forget()
        self.text_area.pack_forget()
        self.command_entry.pack_forget()
        self.hint_label.pack_forget()
        self.solution_label.pack_forget()
        self.feedback_label.pack_forget()
        self.back_button.pack_forget()

        self.category_label.pack(pady=10)
        self.category_list.pack(pady=10)
        self.start_button.pack(pady=10)
        self.update_progress()  # Ensure progress is updated when going back

    def end_practice(self):
        """Return to the main menu after completing a section."""
        self.task_label.pack_forget()
        self.text_area.pack_forget()
        self.command_entry.pack_forget()
        self.hint_label.pack_forget()
        self.solution_label.pack_forget()
        self.feedback_label.pack_forget()
        self.back_button.pack_forget()

        messagebox.showinfo("Section Complete", "You have completed this section!")

        self.tasks.clear()
        self.green_tasks.clear()
        self.current_task = None
        self.performance.clear()
        self.progress_tracker.clear()

        self.go_back_to_categories()

if __name__ == "__main__":
    commands = load_commands("commands.json")
    root = tk.Tk()
    app = VimPracticeApp(root, commands)
    root.mainloop()

