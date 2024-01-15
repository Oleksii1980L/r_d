import json
import tkinter as tk
from tkinter import simpledialog, filedialog
import tkinter.messagebox


class StudyPlannerGUI(tk.Tk):
    def __init__(self):

        self.is_plan_saved = True  # The plan is considered already saved

        super().__init__()
        self.study_plan = {'topics': {}}
        self.current_file = None

        self.title("Study Planner")
        self.geometry("300x300")
        # This creates an instance of the menu class, which will be the main menu of the application. self indicates
        # that this menu is associated with an instance of StudyPlannerGUI
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
        # creates a cascading "Options" menu item and links it to the file_menu submenu, which contains commands
        # for working with files and program options.
        self.menu.add_cascade(label="Options", menu=file_menu)

    # responsible for completing the program.
    def exit_program(self):
        self.destroy()

    def load_plan(self):
        #  opens a dialog box to select a file
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        # Checks whether the user has selected the file at all.
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as file:
                # The contents of the JSON file are read and stored in the study_plan attribute of the class instance.
                self.study_plan = json.load(file)
            # Iterates through all topics and subtopics when loading
            for topic_name in self.study_plan.get('topics', {}):
                # checks topics for completeness and updates information accordingly.
                self.check_topic_completion(topic_name)
            # Saves the path to the current file.
            self.current_file = file_path
            # displays the training plan in the program window.
            self.display_plan()

    #  makes saving the training plan to the current file or selects a new one to save if it wasn't saved earlier.
    def save_plan(self):
        if self.current_file:
            with open(self.current_file, 'w') as file:
                json.dump(self.study_plan, file, indent=2)
            self.is_plan_saved = True  # We indicate that the plan is saved
        else:
            self.save_plan_as()

    #  allows the user to select a new file to save the training plan and saves it
    def save_plan_as(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'w') as file:
                json.dump(self.study_plan, file, indent=2)
            self.current_file = file_path
            self.is_plan_saved = True  # We indicate that the plan is saved

    # interacts with the user to create a new topic and enter information about the new topic and responds
    # to the entered data,updating the training plan and displaying information to the user.
    def add_topic(self):
        topic_name = simpledialog.askstring("Add Topic", "Enter the name of the topic:")
        deadline = simpledialog.askstring("Add Topic", "Enter the deadline for the topic (YYYY-MM-DD):")
        if topic_name:
            if topic_name not in self.study_plan['topics']:
                self.study_plan['topics'][topic_name] = {'subtopics': {}, 'completed': [], 'deadline': deadline}
                self.save_plan()
                self.display_plan()
            else:
                tk.messagebox.showinfo("Info", f'Topic "{topic_name}" already exists. You can edit the deadline.')

    #  the function is responsible for removing a topic from the training plan.
    def remove_topic(self):
        topic_name = simpledialog.askstring("Remove Topic", "Enter the name of the topic:")
        # Checks whether the entered topic name is empty and whether it exists in the plan.
        if topic_name:
            if topic_name in self.study_plan['topics']:
                del self.study_plan['topics'][topic_name]
                self.save_plan()  # Saves the updated training plan.
                self.display_plan()  # Updating the plan display
            else:
                tk.messagebox.showinfo("Info", f'Topic "{topic_name}" does not exist.')

    # responsible for adding a new sub-topic to the topic in the training plan.
    def add_subtopic(self):
        #  to get the theme name (topic_name) from the user, the name of the new sub-theme (subtopic_name)
        #  and deadline for subtopics (deadline)
        topic_name = simpledialog.askstring("Add Subtopic", "Enter the name of the topic:")
        subtopic_name = simpledialog.askstring("Add Subtopic", "Enter the name of the subtopic:")
        deadline = 'Completed'
        # deadline = simpledialog.askstring("Add Subtopic", "Enter the deadline for the subtopic (YYYY-MM-DD):")
        if topic_name and subtopic_name:
            # Checks whether the topic to which the user wants to add a sub-topic exists in the plan.
            if topic_name in self.study_plan['topics']:
                topic = self.study_plan['topics'][topic_name]
                subtopics = topic.get('subtopics', {})

                if subtopic_name not in subtopics:
                    subtopics[subtopic_name] = {'completed': False, 'deadline': deadline}
                    topic['subtopics'] = subtopics

                    # Updating the theme deadline if all subtopics are Completed
                    if all(subtopic.get('completed', False) for subtopic in subtopics.values()):
                        topic['deadline'] = 'Completed'

                    self.save_plan()  # Saves the updated training plan.
                    self.display_plan()  # Updating the plan display
                else:
                    tk.messagebox.showinfo("Info",
                                           f'Subtopic "{subtopic_name}" already exists for topic "{topic_name}"'
                                           f'. You can edit the deadline.')
            else:
                tk.messagebox.showinfo("Info", f'Topic "{topic_name}" does not exist.')
        else:
            # if topic_name or subtopic_name is empty, a message about incorrect data is displayed
            tk.messagebox.showinfo("Info", "Invalid topic or subtopic name.")

    # removing a sub-topic from the specified topic
    def remove_subtopic(self):
        topic_name = simpledialog.askstring("Remove Subtopic", "Enter the name of the topic:")
        subtopic_name = simpledialog.askstring("Remove Subtopic", "Enter the name of the subtopic:")
        if topic_name and subtopic_name:
            if topic_name in self.study_plan['topics']:
                # checks whether the sub-topic with the specified name exists in the sub-topics of the selected topic.
                if subtopic_name in self.study_plan['topics'][topic_name]['subtopics']:
                    # Removes the specified sub-topic from the topic in the training plan.
                    del self.study_plan['topics'][topic_name]['subtopics'][subtopic_name]
                    self.save_plan()  # Saves the updated training plan.
                    self.display_plan()  # Updating the plan display
                else:
                    tk.messagebox.showinfo("Info",
                                           f'Subtopic "{subtopic_name}" does not exist for topic "{topic_name}".')
            else:
                tk.messagebox.showinfo("Info", f'Topic "{topic_name}" does not exist.')
        else:
            # if topic_name or subtopic_name is empty, a message about incorrect data is displayed
            tk.messagebox.showinfo("Info", "Invalid topic or subtopic name.")

    # setting the "completed" status for a sub-topic of the specified topic.
    def mark_completed(self):
        # window where the user must enter the theme name
        topic_name = simpledialog.askstring("Mark Subtopic as Completed", "Enter the name of the topic:")
        #  window where the user must enter the name of the sub-topic
        subtopic_name = simpledialog.askstring("Mark Subtopic as Completed", "Enter the name of the subtopic:")

        if topic_name and subtopic_name:
            # Checks whether the topic with the specified name exists in the training plan.
            if topic_name in self.study_plan['topics']:
                topic = self.study_plan['topics'][topic_name]
                # Checks whether the sub-topic with the specified name exists in the sub-topics of the selected topic.
                if 'subtopics' in topic and subtopic_name in topic['subtopics']:
                    subtopic = topic['subtopics'][subtopic_name]
                    # Setting the subtheme status to True
                    subtopic['completed'] = True
                    # Checks whether all subtopics of the specified topic are now completed (completed),
                    # and sets the "completed" status for the theme, if so.
                    self.check_topic_completion(topic_name)
                    self.save_plan()  # Saves the updated training plan.
                    self.display_plan()  # Updating the plan display
                else:
                    tk.messagebox.showinfo("Info",
                                           f'Subtopic "{subtopic_name}" does not exist '
                                           f'for topic "{topic_name}".')
            else:
                tk.messagebox.showinfo("Info", f'Topic "{topic_name}" does not exist.')

    # determines whether all subtopics for a given topic are completed ,and sets or cancels the status accordingly
    # "completed" for the theme itself.
    def check_topic_completion(self, topic_name):
        topic = self.study_plan['topics'][topic_name]
        # The all function returns True if all elements of the specified iterable object'
        # 'are true.checks all subtopics for the value 'completed',which is True.
        all_subtopics_completed = all(
            sub_details.get('completed', False)  # For each subteme, it gets the value of the 'completed'key.
            # If the key is missing, the default value is returned, which in this case is False.
            for sub_details in topic.get('subtopics', {}).values()  # Gets a dictionary of all subtopics for the
            # selected topic. If there are no sub-topics in the topic, an empty dictionary is returned.
        )
        # Checks whether all subtopics have been completed and whether the topic has not yet been marked as completed
        if all_subtopics_completed and not topic.get('completed', False):
            topic['completed'] = True  # Sets the "completed" status for the theme.
            topic['deadline'] = "Completed"  # Sets the "Completed" status for the theme.
            self.save_plan()  # Saves the updated training plan.
            self.display_plan()  # Updating the plan display
        elif not all_subtopics_completed and topic.get('completed', False):
            topic['completed'] = False
            self.save_plan()

    #  to change the deadline for the selected topic in the training plan.
    def change_deadline(self):
        topic_name = simpledialog.askstring("Change Deadline", "Enter the name of the topic:")
        if topic_name:
            if topic_name in self.study_plan['topics']:
                new_deadline = simpledialog.askstring("Change Deadline", "Enter the new deadline for the"
                                                                         " topic (YYYY-MM-DD):")
                self.study_plan['topics'][topic_name]['deadline'] = new_deadline
                self.save_plan()
                self.display_plan()
            else:
                tk.messagebox.showinfo("Info", f'Topic "{topic_name}" does not exist.')

    # Code for displaying the plan...
    def display_plan(self):
        if not self.is_plan_saved:  # Saving the plan if it has been changed
            self.save_plan()
        # Creates a plan_text string with the heading "Study Plan:".
        plan_text = "\nStudy Plan:"
        # Iterates through topics in the training plan and adds information about each topic to the plan_text string,
        # including the topic name and deadline (if specified).
        for topic, details in self.study_plan['topics'].items():
            deadline = details.get('deadline', 'No deadline')
            plan_text += f"\n\nTopic: {topic} (Deadline: {deadline})"
            # If a topic has sub-topics, it adds information to the plan_text string for each sub-topic,
            # including the name of the sub-topic
            # and its status (completed or not).
            if 'subtopics' in details:
                subtopics = details['subtopics']
                if subtopics:
                    plan_text += "\n  Subtopics:"
                    for subtopic, sub_details in subtopics.items():
                        if isinstance(sub_details, dict):  # Checking whether sub_details is a dictionary
                            status = "Completed" if sub_details.get('completed', False) else "Not Completed"
                            plan_text += f"\n    - {subtopic} ({status})"
                        else:
                            plan_text += f"\n    - {subtopic} (Not Completed)"

        # Opens a dialog box with information about the training plan, where the string plan_text is displayed.
        tk.messagebox.showinfo("Study Plan", plan_text)

    # saves the current training plan and completes the program
    def save_and_exit(self):
        self.save_plan()
        self.destroy()  # closes the main window of the program,which leads to the end of program execution.


# This construct checks whether the file is executed directly (and not imported as a module into another script)
if __name__ == "__main__":
    planner = StudyPlannerGUI()  # Creating an instance of the StudyPlannerGUI class, the graphical interface
    # of the plan program.training.
    planner.mainloop()  # Starts the Tkinter event processing loop. This method waits for events
    # (such as button clicks, resize windows, etc.) and calls the corresponding event handling functions.
    # Until the window is closed or called
