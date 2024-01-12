import json
import tkinter as tk
from tkinter import simpledialog, filedialog, messagebox

class StudyPlannerGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.study_plan = {'topics': {}}
        self.current_file = None

        self.title("Study Planner")
        self.geometry("300x300")

        self.menu = tk.Menu(self)
        self.config(menu=self.menu)

        file_menu = tk.Menu(self.menu, tearoff=0)
        file_menu.add_command(label="Display Plan", command=self.display_plan)
        file_menu.add_command(label="Add Topic", command=self.add_topic)
        file_menu.add_command(label="Remove Topic", command=self.remove_topic)
        file_menu.add_command(label="Add Subtopic", command=self.add_subtopic)
        file_menu.add_command(label="Remove Subtopic", command=self.remove_subtopic)
        file_menu.add_command(label="Mark Subtopic as Completed", command=self.mark_completed)
        file_menu.add_command(label="Change Deadline", command=self.change_deadline)
        file_menu.add_separator()
        file_menu.add_command(label="Save", command=self.save_plan)
        file_menu.add_command(label="Save As...", command=self.save_plan_as)
        file_menu.add_command(label="Load", command=self.load_plan)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.exit_program)
        self.menu.add_cascade(label="Options", menu=file_menu)

    def exit_program(self):
        self.destroy()

    def load_plan(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as file:
                self.study_plan = json.load(file)
            self.current_file = file_path
            self.display_plan()

    def save_plan(self):
        if self.current_file:
            with open(self.current_file, 'w') as file:
                json.dump(self.study_plan, file, indent=2)
        else:
            self.save_plan_as()

    def save_plan_as(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'w') as file:
                json.dump(self.study_plan, file, indent=2)
            self.current_file = file_path

    def add_topic(self):
        topic_name = simpledialog.askstring("Add Topic", "Enter the name of the topic:")
        deadline = simpledialog.askstring("Add Topic", "Enter the deadline for the topic (YYYY-MM-DD):")
        if topic_name:
            if topic_name not in self.study_plan['topics']:
                self.study_plan['topics'][topic_name] = {'subtopics': {}, 'completed': [], 'deadline': deadline}
                self.save_plan()
                self.display_plan()
            else:
                messagebox.showinfo("Info", f'Topic "{topic_name}" already exists. You can edit the deadline.')

    def remove_topic(self):
        topic_name = simpledialog.askstring("Remove Topic", "Enter the name of the topic:")
        if topic_name:
            if topic_name in self.study_plan['topics']:
                del self.study_plan['topics'][topic_name]
                self.save_plan()
                self.display_plan()
            else:
                messagebox.showinfo("Info", f'Topic "{topic_name}" does not exist.')

    def add_subtopic(self):
        topic_name = simpledialog.askstring("Add Subtopic", "Enter the name of the topic:")
        subtopic_name = simpledialog.askstring("Add Subtopic", "Enter the name of the subtopic:")
        deadline = simpledialog.askstring("Add Subtopic", "Enter the deadline for the subtopic (YYYY-MM-DD):")

        if topic_name:
            if topic_name not in self.study_plan['topics']:
                messagebox.showinfo("Info", f'Topic "{topic_name}" does not exist.')
                return

            if 'subtopics' not in self.study_plan['topics'][topic_name]:
                self.study_plan['topics'][topic_name]['subtopics'] = {}

            if subtopic_name not in self.study_plan['topics'][topic_name]['subtopics']:
                self.study_plan['topics'][topic_name]['subtopics'][subtopic_name] = {
                    'completed': False,
                    'deadline': deadline
                }
                self.save_plan()
                self.display_plan()
            else:
                messagebox.showinfo("Info",
                                    f'Subtopic "{subtopic_name}" already exists for topic "{topic_name}". You can edit the deadline.')

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
                    tk.messagebox.showinfo("Info",
                                           f'Subtopic "{subtopic_name}" does not exist for topic "{topic_name}".')
            else:
                tk.messagebox.showinfo("Info", f'Topic "{topic_name}" does not exist.')

    def mark_completed(self):
        topic_name = simpledialog.askstring("Mark Subtopic as Completed", "Enter the name of the topic:")
        subtopic_name = simpledialog.askstring("Mark Subtopic as Completed", "Enter the name of the subtopic:")

        if topic_name and subtopic_name:
            if topic_name in self.study_plan['topics']:
                topic = self.study_plan['topics'][topic_name]

                if 'subtopics' in topic and subtopic_name in topic['subtopics']:
                    subtopic = topic['subtopics'][subtopic_name]

                    if not subtopic.get('completed', False):
                        subtopic['completed'] = True
                        self.save_plan()
                        self.display_plan()
                    else:
                        tk.messagebox.showinfo("Info",
                                               f'Subtopic "{subtopic_name}" is already marked as completed.')
                else:
                    tk.messagebox.showinfo("Info",
                                           f'Subtopic "{subtopic_name}" does not exist for topic "{topic_name}".')
            else:
                tk.messagebox.showinfo("Info", f'Topic "{topic_name}" does not exist.')

    def check_topic_completion(self, topic_name):
        all_subtopics_completed = all(
            self.study_plan['topics'][topic_name]['subtopics'][subtopic]['completed']
            for subtopic in self.study_plan['topics'][topic_name]['subtopics']
        )
        if all_subtopics_completed:
            self.study_plan['topics'][topic_name]['completed'] = True
            self.save_plan()

    def change_deadline(self):
        topic_name = simpledialog.askstring("Change Deadline", "Enter the name of the topic:")
        if topic_name:
            if topic_name in self.study_plan['topics']:
                new_deadline = simpledialog.askstring("Change Deadline", "Enter the new deadline for the topic (YYYY-MM-DD):")
                self.study_plan['topics'][topic_name]['deadline'] = new_deadline
                self.save_plan()
                self.display_plan()
            else:
                tk.messagebox.showinfo("Info", f'Topic "{topic_name}" does not exist.')

    def display_plan(self):
        plan_text = "\nStudy Plan:"
        completed_topics = []

        for topic, details in self.study_plan['topics'].items():
            if 'subtopics' in details and all(
                    sub_details.get('completed', False) for sub_details in details['subtopics'].values()):
                completed_topics.append(topic)
            else:
                deadline = details.get('deadline', 'No deadline')
                plan_text += f"\n\nTopic: {topic} (Deadline: {deadline})"

                if 'subtopics' in details:
                    subtopics = details['subtopics']
                    if subtopics:
                        plan_text += "\n  Subtopics:"
                        for subtopic, sub_details in subtopics.items():
                            if isinstance(sub_details, dict):  # Перевірка, чи sub_details є словником
                                status = "Completed" if sub_details.get('completed', False) else "Not Completed"
                                plan_text += f"\n    - {subtopic} ({status})"
                                if sub_details.get('completed', False):
                                    completed_topics.append(subtopic)

        # if completed_topics:
        #     plan_text += "\n\nCompleted Topics:"
        #     for completed_topic in completed_topics:
        #         plan_text += f"\n  - {completed_topic} (Completed)"

        messagebox.showinfo("Study Plan", plan_text)

    def save_and_exit(self):
        self.save_plan()
        self.destroy()


if __name__ == "__main__":
    planner = StudyPlannerGUI()
    planner.mainloop()
