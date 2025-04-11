
# Maps class display names to actual .json filenames
class_file_map = {
    "DS 3850": "DS_3850.json",
    "DS 3860": "DS_3860.json",
    "Money and Banking": "Money_and_Banking.json",
    "Investment Challenge I": "Investment_Challenge_I.json",  # Updated key
    "Intermediate Finance": "Intermediate_Finance.json",
    "Theater": "Theater.json"
}


import tkinter as tk
from tkinter import messagebox
import json
import os


# Function to open the Administrator window with password
def open_admin():
    # Password prompt window
    pw_window = tk.Toplevel(root)
    pw_window.title("Admin Login")
    pw_window.geometry("300x150")

    tk.Label(pw_window, text="Enter Admin Password:", font=('Helvetica', 12)).pack(pady=10)
    pw_entry = tk.Entry(pw_window, show="*", width=30)
    pw_entry.pack(pady=5)

    def check_password():
        if pw_entry.get() == "CanIPleaseHaveExtraCreditPorFavor":
            pw_window.destroy()
            open_class_selector()
        else:
            messagebox.showerror("Access Denied", "Incorrect password.")

    tk.Button(pw_window, text="Submit", command=check_password).pack(pady=10)


def open_class_selector():
    class_window = tk.Toplevel(root)
    class_window.title("Select Class")
    class_window.geometry("300x350")

    tk.Label(class_window, text="Choose a Class to Create Quiz", font=('Helvetica', 12)).pack(pady=10)

    classes = [
        "DS 3850",
        "DS 3860",
        "Money and Banking",
        "Investment Challenge I",
        "Intermediate Finance",
        "Theater"
    ]

    for cls in classes:
        tk.Button(class_window, text=cls, width=30, command=lambda c=cls: open_admin_panel(c)).pack(pady=5)


def open_admin_panel(class_name):
    admin_window = tk.Toplevel(root)
    admin_window.title(f"Administrator - {class_name}")
    admin_window.geometry("400x300")

    tk.Label(admin_window, text=f"Admin Panel for {class_name}", font=('Helvetica', 14)).pack(pady=20)

    # Button for adding new question
    tk.Button(admin_window, text="➕ Add New Question", width=25,
              command=lambda: add_new_question_gui(class_name, admin_window)).pack(pady=5)

    # Button for editing existing questions
    tk.Button(admin_window, text="📝 Edit Existing Questions", width=25,
              command=lambda: edit_existing_questions(class_name)).pack(pady=5)

    # Button for deleting questions
    tk.Button(admin_window, text="❌ Delete Questions", width=25,
              command=lambda: edit_existing_questions(class_name, delete_only=True)).pack(pady=5)

    # Back button to go back to the class selector
    tk.Button(admin_window, text="⬅️ Back to Class List", width=25, command=admin_window.destroy).pack(pady=20)


def add_new_question_gui(class_name, parent_window):
    filename = class_file_map.get(class_name)
    if not filename:
        messagebox.showerror("Error", f"No file mapping found for {class_name}.")
        return

    quiz_data = load_quiz_data(filename)
    ...

    # Load the existing quiz data or create a new list if the file doesn't exist
    quiz_data = load_quiz_data(filename)

    # Add new blank question
    quiz_data.append({
        "type": "mcq",
        "question": "",
        "options": ["", "", "", ""],
        "answers": [""]
    })

    index = len(quiz_data) - 1

    # Save the updated data to the JSON file
    save_quiz_data(filename, quiz_data)

    edit_question_form(class_name, quiz_data, index, parent_window, is_new=True)


def edit_existing_questions(class_name, delete_only=False):
    filename = class_file_map.get(class_name)


    # Load the existing quiz data
    quiz_data = load_quiz_data(filename)

    edit_window = tk.Toplevel(root)
    edit_window.title(f"Edit Questions - {class_name}")
    edit_window.geometry("700x450")

    tk.Label(edit_window, text=f"{class_name} - Manage Quiz Questions", font=('Helvetica', 14)).pack(pady=5)
    tk.Label(edit_window, text="Select a question to {}:".format("delete" if delete_only else "edit"),
              font=('Helvetica', 12)).pack(pady=5)
    listbox = tk.Listbox(edit_window, width=90, height=15)
    listbox.pack(pady=10)

    def refresh_listbox():
        listbox.delete(0, tk.END)
        for i, q in enumerate(quiz_data):
            preview = f"{i + 1}. ({q['type']}) {q['question'][:70]}{'...' if len(q['question']) > 70 else ''}"
            listbox.insert(tk.END, preview)

    def edit_selected():
        selected = listbox.curselection()
        if not selected:
            messagebox.showwarning("Select One", "Please select a question to edit.")
            return
        index = selected[0]
        edit_question_form(class_name, quiz_data, index, edit_window, refresh_listbox)

    def delete_selected():
        selected = listbox.curselection()
        if not selected:
            messagebox.showwarning("Select One", "Please select a question to delete.")
            return
        index = selected[0]
        confirm = messagebox.askyesno("Delete Question", "Are you sure you want to delete this question?")
        if confirm:
            quiz_data.pop(index)
            save_quiz_data(filename, quiz_data)  # Save the data after deleting
            refresh_listbox()

    def add_new_question():
        quiz_data.append({
            "type": "mcq",
            "question": "",
            "options": ["", "", "", ""],
            "answers": [""]
        })
        index = len(quiz_data) - 1
        edit_question_form(class_name, quiz_data, index, edit_window, refresh_listbox, is_new=True)

    if delete_only:
        tk.Button(edit_window, text="Delete Selected", command=delete_selected).pack(pady=5)
    else:
        tk.Button(edit_window, text="Edit Selected", command=edit_selected).pack(pady=5)
        tk.Button(edit_window, text="Add New Question", command=add_new_question).pack(pady=5)

    refresh_listbox()


def edit_question_form(class_name, quiz_data, index, parent_window, refresh_callback=None, is_new=False):
    q = quiz_data[index]

    form = tk.Toplevel(root)
    form.title("Edit Question")
    form.geometry("550x550")

    tk.Label(form, text=f"{'New' if is_new else 'Edit'} Question #{index + 1}", font=('Helvetica', 12)).pack(pady=5)

    question_var = tk.StringVar(value=q.get("question", ""))
    tk.Label(form, text="Question Text:").pack()
    tk.Entry(form, textvariable=question_var, width=60).pack(pady=5)

    type_var = tk.StringVar(value=q.get("type", "mcq"))
    tk.Label(form, text="Question Type:").pack()
    tk.OptionMenu(form, type_var, "mcq", "fitb", "tf", "multi").pack()

    options_var = tk.StringVar(value=",".join(q.get("options", [])))
    tk.Label(form, text="Options (comma-separated):").pack()
    tk.Entry(form, textvariable=options_var, width=60).pack(pady=5)

    answers_var = tk.StringVar(value=",".join(q.get("answers", [])))
    tk.Label(form, text="Correct Answer(s) (comma-separated):").pack()
    tk.Entry(form, textvariable=answers_var, width=60).pack(pady=5)

    def save_changes():
        question_text = question_var.get().strip()
        q_type = type_var.get()
        options = [opt.strip() for opt in options_var.get().split(",") if opt.strip()]
        answers = [ans.strip() for ans in answers_var.get().split(",") if ans.strip()]

        if not question_text or not answers:
            messagebox.showwarning("Missing Info", "Please fill in question and at least one answer.")
            return

        q["question"] = question_text
        q["type"] = q_type
        q["answers"] = answers

        if q_type in ["mcq", "tf", "multi"]:
            if not options:
                messagebox.showwarning("Missing Options", "This question type requires options.")
                return
            q["options"] = options
        else:
            q["options"] = []

        # Save file
        filename = class_file_map.get(class_name)
        save_quiz_data(filename, quiz_data)

        messagebox.showinfo("Saved", "Question saved successfully.")
        form.destroy()
        if refresh_callback:
            refresh_callback()


def load_quiz_data(filename):
    # Check if the file exists, if not, return an empty list
    if os.path.exists(filename):
        with open(filename, "r") as f:
            return json.load(f)
    else:
        return []  # Return empty list if file does not exist
    print(f"Loading file: {filename}")


def save_quiz_data(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

    print(f"Saving file: {filename}")

# Function to open the Take Quiz window
def open_quiz():
    class_window = tk.Toplevel(root)
    class_window.title("Choose Class")
    class_window.geometry("300x300")

    tk.Label(class_window, text="Select a class to take the quiz:", font=('Helvetica', 12)).pack(pady=10)

    classes = [
        "DS 3850",
        "DS 3860",
        "Money and Banking",
        "Investment Challenge I",
        "Intermediate Finance",
        "Theater"
    ]

    def start_quiz(class_name):
        class_window.destroy()
        load_quiz(class_name)

    for cls in classes:
        tk.Button(class_window, text=cls, width=30, command=lambda c=cls: start_quiz(c)).pack(pady=5)


def load_quiz(class_name):
    filename = class_file_map.get(class_name)

    try:
        with open(filename, "r") as f:
            questions = json.load(f)
    except FileNotFoundError:
        messagebox.showerror("Error", f"No quiz found for {class_name}.")
        return
    print(f"Loading file: {filename}")

    quiz_window = tk.Toplevel(root)
    quiz_window.title(f"{class_name} - Quiz")
    quiz_window.geometry("500x400")

    current_index = [0]
    score = [0]
    selected_answer = tk.StringVar()
    multi_vars = []
    wrong_answers = []  # Track wrong answers with question details

    question_frame = tk.Frame(quiz_window)
    question_frame.pack(pady=20)

    def render_question():
        for widget in question_frame.winfo_children():
            widget.destroy()

        q = questions[current_index[0]]
        q_type = q["type"]
        selected_answer.set("")
        multi_vars.clear()

        tk.Label(question_frame, text=f"Question {current_index[0] + 1}", font=('Helvetica', 12)).pack(pady=5)
        tk.Label(question_frame, text=q["question"], wraplength=450).pack(pady=5)

        if q_type in ["mcq", "tf"]:
            for opt in q["options"]:
                tk.Radiobutton(question_frame, text=opt, variable=selected_answer, value=opt).pack(anchor="w")

        elif q_type == "fitb":
            tk.Entry(question_frame, textvariable=selected_answer, width=40).pack(pady=10)

        elif q_type == "multi":
            for opt in q["options"]:
                var = tk.IntVar()
                multi_vars.append((opt, var))
                tk.Checkbutton(question_frame, text=opt, variable=var).pack(anchor="w")

        tk.Button(question_frame, text="Next", command=next_question).pack(pady=10)

    def next_question():
        q = questions[current_index[0]]
        q_type = q["type"]
        user_answer = selected_answer.get().strip()

        if q_type == "mcq":
            if user_answer in q["answers"]:
                score[0] += 1
            else:
                wrong_answers.append({"question": q["question"], "correct": q["answers"], "given": user_answer})

        elif q_type == "tf":
            if user_answer in q["answers"]:
                score[0] += 1
            else:
                wrong_answers.append({"question": q["question"], "correct": q["answers"], "given": user_answer})

        elif q_type == "fitb":
            if user_answer.lower() in [ans.lower() for ans in q["answers"]]:
                score[0] += 1
            else:
                wrong_answers.append({"question": q["question"], "correct": q["answers"], "given": user_answer})

        elif q_type == "multi":
            selected_options = [opt for opt, var in zip(q["options"], multi_vars) if var.get()]
            if sorted(selected_options) == sorted(q["answers"]):
                score[0] += 1
            else:
                wrong_answers.append({"question": q["question"], "correct": q["answers"], "given": selected_options})

        current_index[0] += 1

        if current_index[0] < len(questions):
            render_question()
        else:
            display_result()

    def display_result():
        quiz_window.destroy()
        result_window = tk.Toplevel(root)
        result_window.title("Quiz Result")
        result_window.geometry("300x250")

        tk.Label(result_window, text="Quiz Completed!", font=('Helvetica', 14)).pack(pady=20)
        tk.Label(result_window, text=f"Your Score: {score[0]}/{len(questions)}", font=('Helvetica', 12)).pack(pady=10)

        if wrong_answers:
            tk.Label(result_window, text="Incorrect Answers:", font=('Helvetica', 12)).pack(pady=5)
            for wrong in wrong_answers:
                tk.Label(result_window, text=f"Q: {wrong['question']}\nCorrect: {wrong['correct']}\nYour Answer: {wrong['given']}\n").pack()


# Create main window
root = tk.Tk()
root.title("Quiz Application")
root.geometry("500x300")

# Add main buttons
tk.Button(root, text="Admin Panel", width=25, command=open_admin).pack(pady=20)
tk.Button(root, text="Take Quiz", width=25, command=open_quiz).pack(pady=10)

root.mainloop()
