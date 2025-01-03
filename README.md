# Vim Practice Application

## Overview
The Vim Practice Application is an interactive tool designed to help users learn and practice Vim commands. With a wide range of commands implemented, the application is suitable for beginners and advanced users alike. It supports categories, hints, solutions, and spaced repetition to reinforce learning. The goal is to provide an engaging way to master Vim commands systematically.

---

## Features
- Interactive practice with Vim commands.
- Spaced repetition to reinforce learning.
- Hints and solutions for each command.
- Visual feedback for correct and incorrect answers.
- Progress tracking for each command category.
- Includes commands from Vim's roadmap and a comprehensive Vim cheat sheet.

---

## Categories
The following command categories are supported:

- Motion Commands
- Insert Commands
- Visual Mode Commands
- Undo and Redo Commands
- Search Commands
- Replace Mode Commands
- Scrolling Commands
- Delete Commands
- Yank and Paste Commands
- Text Object Commands
- Tabs and Windows Commands
- Registers, Macros, and Folding Commands

---

## Keyboard Shortcuts
- **Enter**: Submit the entered command for evaluation.
- **Up Arrow**: Show a hint for the current task.
- **Right Arrow**: Show the solution for the current task.
- **Ctrl + Key Combinations**: Practice commands requiring control keys (e.g., Ctrl-U, Ctrl-R).

---

## Commands
All commands in the application are stored in `commands.json`. This file contains tasks, commands, hints, and examples for practice. It covers commands from both Vim's roadmap and a comprehensive Vim cheat sheet to ensure complete coverage.

---

## How to Use
1. Launch the application.
2. Select a command category from the main menu.
3. Practice the commands by typing them in the input field.
4. Use hints and solutions if needed.
5. Progress through the commands until all are marked as "green" (learned).
6. Return to the main menu to choose another category.

---

## How to Start the Application
To start the Vim Practice Application, follow these steps:

1. **Download or Clone the Repository**:
   - Ensure you have the application files on your machine. If hosted on a repository (e.g., GitHub), clone it:
     ```bash
     git clone https://github.com/your-repo/vim-practice-app.git
     ```

2. **Run the Application**:
   - Navigate to the correct directory
   - In the terminal run the python file:
     ```bash
     python3 vim_practice.py
     ```
3. **Start Practicing**:
   - Follow the prompts to select a command category and begin practicing.

---

## Application Workflow
1. **Start Practice**: Select a category and start learning the commands.
2. **Submit Commands**: Type the command into the input box and press Enter.
3. **Feedback**: Receive immediate feedback on correctness.
4. **Hints and Solutions**: Use the arrow keys for additional help.
5. **Completion**: Once all commands in a category are learned, the application will return to the main menu.
