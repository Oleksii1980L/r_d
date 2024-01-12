import json
import tkinter as tk
from tkinter import simpledialog

class StudyPlannerGUI(tk.Tk):
    def __init__(self, plan_file='study_plan.json'):
        super().__init__()
        self.plan_file = plan_file
        self.study_plan = self.load_plan()

        self.title("Study Planner")
        self.geometry("400x300")

        self.menu = tk.Menu(self)
        self.config(menu=self.menu)

        file_menu = tk.Menu(self.menu, tearoff=0)
        file_menu.add_command(label="Display Plan", command=self.display_plan)
        file_menu.add_command(label="Add Topic", command=self.add_topic)
        file_menu.add_command(label="Remove Topic", command=self.remove_topic)
        file_menu.add_command(label="Add Subtopic", command=self.add_subtopic)
        file_menu.add_command(label="Remove Subtopic", command=self.remove_subtopic)
        file_menu.add_command(label="Mark Subtopic as Completed", command=self.mark_completed)
        file_menu.add_separator()
        file_menu.add_command(label="Save and Exit", command=self.save_and_exit)
        self.menu.add_cascade(label="Options", menu=file_menu)

    def load_plan(self):
        try:
            with open(self.plan_file, 'r', encoding='utf-8') as file:
                study_plan = json.load(file)
            return study_plan
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            return {'topics': {}}

    def save_plan(self):
        with open(self.plan_file, 'w') as file:
            json.dump(self.study_plan, file, indent=2)

    def add_topic(self):
        topic_name = simpledialog.askstring("Add Topic", "Enter the name of the topic:")
        deadline = simpledialog.askstring("Add Topic", "Enter the deadline for the topic (YYYY-MM-DD):")
        if topic_name:
            if topic_name not in self.study_plan['topics']:
                self.study_plan['topics'][topic_name] = {'subtopics': {}, 'completed': [], 'deadline': deadline}
                self.save_plan()
                self.display_plan()
            else:
                tk.messagebox.showinfo("Info", f'Topic "{topic_name}" already exists.')

    def remove_topic(self):
        topic_name = simpledialog.askstring("Remove Topic", "Enter the name of the topic:")
        if topic_name:
            if topic_name in self.study_plan['topics']:
                del self.study_plan['topics'][topic_name]
                self.save_plan()
                self.display_plan()
            else:
                tk.messagebox.showinfo("Info", f'Topic "{topic_name}" does not exist.')

    def add_subtopic(self):
        topic_name = simpledialog.askstring("Add Subtopic", "Enter the name of the topic:")
        subtopic_name = simpledialog.askstring("Add Subtopic", "Enter the name of the subtopic:")
        deadline = simpledialog.askstring("Add Subtopic", "Enter the deadline for the subtopic (YYYY-MM-DD):")
        if topic_name and subtopic_name:
            if topic_name in self.study_plan['topics']:
                if subtopic_name not in self.study_plan['topics'][topic_name]['subtopics']:
                    self.study_plan['topics'][topic_name]['subtopics'][subtopic_name] = {'completed': False, 'deadline': deadline}
                    self.save_plan()
                    self.display_plan()
                else:
                    tk.messagebox.showinfo("Info",
                                           f'Subtopic "{subtopic_name}" already exists for topic "{topic_name}".')
            else:
                tk.messagebox.showinfo("Info", f'Topic "{topic_name}" does not exist.')

    def remove_subtopic(self):
        topic_name = simpledialog.askstring("Remove Subtopic", "Enter the name of the topic:")
        subtopic_name = simpledialog.askstring("Remove Subtopic", "Enter the name of the subtopic:")
        if topic_name and subtopic_name:
            if topic_name in self.study_plan['topics']:
                if subtopic_name in self.study_plan['topics'][topic_name]['subtopics']:
                    del self.study_plan['topics'][topic_name]['subtopics'][subtopic_name]
                    self.save_plan()
                    self.display_plan()
                else:
                    tk.messagebox.showinfo("Info", f'Subtopic "{subtopic_name}" does not exist for topic "{topic_name}".')
            else:
                tk.messagebox.showinfo("Info", f'Topic "{topic_name}" does not exist.')

    def mark_completed(self):
        topic_name = simpledialog.askstring("Mark Subtopic as Completed", "Enter the name of the topic:")
        subtopic_name = simpledialog.askstring("Mark Subtopic as Completed", "Enter the name of the subtopic:")
        if topic_name and subtopic_name:
            if topic_name in self.study_plan['topics']:
                if subtopic_name in self.study_plan['topics'][topic_name]['subtopics']:
                    self.study_plan['topics'][topic_name]['subtopics'][subtopic_name]['completed'] = True
                    self.study_plan['topics'][topic_name]['completed'].append(subtopic_name)
                    self.save_plan()
                    self.display_plan()
                else:
                    tk.messagebox.showinfo("Info", f'Subtopic "{subtopic_name}" does not exist for topic "{topic_name}".')
            else:
                tk.messagebox.showinfo("Info", f'Topic "{topic_name}" does not exist.')

    def display_plan(self):
        plan_text = "\nStudy Plan:"
        for topic, details in self.study_plan['topics'].items():
            deadline = details.get('deadline', 'No deadline')
            plan_text += f"\n\nTopic: {topic} (Deadline: {deadline})"

            if 'subtopics' in details and details['subtopics']:
                plan_text += "\n  Subtopics:"
                for subtopic, sub_details in details['subtopics'].items():
                    status = "Completed" if sub_details['completed'] else "Not Completed"
                    sub_deadline = sub_details.get('deadline', 'No deadline')
                    plan_text += f"\n    - {subtopic} (Status: {status}, Deadline: {sub_deadline})"

            if details['completed']:
                plan_text += "\n  Completed Subtopics:"
                for subtopic in details['completed']:
                    plan_text += f"\n    - {subtopic}"

        tk.messagebox.showinfo("Study Plan", plan_text)



    def save_and_exit(self):
        self.save_plan()
        self.destroy()

if __name__ == "__main__":
    planner = StudyPlannerGUI(plan_file='your_plan_file.json')
    planner.mainloop()

