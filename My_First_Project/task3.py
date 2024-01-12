import json
import tkinter as tk
from tkinter import simpledialog, filedialog

class StudyPlannerGUI(tk.Tk):
    def __init__(self):
        # Інші налаштування...
        self.is_plan_saved = True  # План вважається вже збереженим

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

            # Перевірка всіх тем та підтем при завантаженні
            for topic_name in self.study_plan.get('topics', {}):
                self.check_topic_completion(topic_name)

            self.current_file = file_path
            self.display_plan()

    def save_plan(self):
        if self.current_file:
            with open(self.current_file, 'w') as file:
                json.dump(self.study_plan, file, indent=2)
            self.is_plan_saved = True  # Позначаємо, що план збережений
        else:
            self.save_plan_as()

    def save_plan_as(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'w') as file:
                json.dump(self.study_plan, file, indent=2)
            self.current_file = file_path
            self.is_plan_saved = True  # Позначаємо, що план збережений

    def add_topic(self):
        topic_name = simpledialog.askstring("Add Topic", "Enter the name of the topic:")
        deadline = simpledialog.askstring("Add Topic", "Enter the deadline for the topic (YYYY-MM-DD):")
        if topic_name:
            if topic_name not in self.study_plan['topics']:
                self.study_plan['topics'][topic_name] = {'subtopics': {}, 'completed': [], 'deadline': deadline}
                self.check_topic_completion(topic_name)  # Перевірка на виконання всіх підтем
                self.save_plan()
                self.display_plan()
            else:
                tk.messagebox.showinfo("Info", f'Topic "{topic_name}" already exists. You can edit the deadline.')

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
                topic = self.study_plan['topics'][topic_name]
                subtopics = topic.get('subtopics', {})

                if subtopic_name not in subtopics:
                    subtopics[subtopic_name] = {'completed': False, 'deadline': deadline}
                    topic['subtopics'] = subtopics

                    # Оновлення дедлайну теми, якщо всі підтеми Completed
                    if all(subtopic.get('completed', False) for subtopic in subtopics.values()):
                        topic['deadline'] = 'Completed'

                    self.save_plan()
                    self.display_plan()  # Оновлення відображення плану
                else:
                    tk.messagebox.showinfo("Info",
                                           f'Subtopic "{subtopic_name}" already exists for topic "{topic_name}". You can edit the deadline.')
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

                    # Опціонально: видалення підтеми зі списку невиконаних
                    del topic['subtopics'][subtopic_name]

                    topic['completed'].append(subtopic_name)
                    self.save_plan()
                    self.display_plan()
                else:
                    tk.messagebox.showinfo("Info",
                                           f'Subtopic "{subtopic_name}" does not exist for topic "{topic_name}".')
            else:
                tk.messagebox.showinfo("Info", f'Topic "{topic_name}" does not exist.')

    def check_topic_completion(self, topic_name):
        topic = self.study_plan['topics'][topic_name]
        all_subtopics_completed = all(
            sub_details.get('completed', False)
            for sub_details in topic.get('subtopics', {}).values()
        )

        if all_subtopics_completed and not topic.get('completed', False):
            topic['completed'] = True
            topic['deadline'] = "Completed"
            self.save_plan()
            self.display_plan()
        elif not all_subtopics_completed and topic.get('completed', False):
            topic['completed'] = False
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
        # Код для відображення плану...
        if not self.is_plan_saved:
            self.save_plan()  # Зберегти план, якщо він був змінений

        plan_text = "\nStudy Plan:"
        for topic, details in self.study_plan['topics'].items():
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
                        else:
                            plan_text += f"\n    - {subtopic} (Not Completed)"

            # if details.get('completed', []):
            #     plan_text += "\n  Completed Subtopics:"
            #     for subtopic in details['completed']:
            #         plan_text += f"\n    - {subtopic} (Completed)"

        tk.messagebox.showinfo("Study Plan", plan_text)

    def save_and_exit(self):
        self.save_plan()
        self.destroy()


if __name__ == "__main__":
    planner = StudyPlannerGUI()
    planner.mainloop()
