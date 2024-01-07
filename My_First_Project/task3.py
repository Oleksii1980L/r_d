import json


class StudyPlanner:
    def __init__(self, plan_file='study_plan.json'):
        self.plan_file = plan_file
        self.study_plan = self.load_plan()

    # Uploading a theme plan from a file
    def load_plan(self):
        try:
            with open(self.plan_file, 'r') as file:
                study_plan = json.load(file)
            return study_plan
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            return {'topics': {}}

    # Saving the theme plan to a file
    def save_plan(self):
        with open(self.plan_file, 'w') as file:
            json.dump(self.study_plan, file, indent=2)

    # Adding topic
    def add_topic(self, topic_name):
        if topic_name not in self.study_plan['topics']:
            self.study_plan['topics'][topic_name] = {'subtopics': {}, 'completed': []}
            self.save_plan()
            print(f'Topic "{topic_name}" added successfully.')
        else:
            print(f'Topic "{topic_name}" already exists.')

    # Deleting a topic
    def remove_topic(self, topic_name):
        if topic_name in self.study_plan['topics']:
            del self.study_plan['topics'][topic_name]
            self.save_plan()
            print(f'Topic "{topic_name}" removed successfully.')
        else:
            print(f'Topic "{topic_name}" does not exist.')

    # Adding subtopics
    def add_subtopic(self, topic_name, subtopic_name):
        if topic_name in self.study_plan['topics']:
            if subtopic_name not in self.study_plan['topics'][topic_name]['subtopics']:
                self.study_plan['topics'][topic_name]['subtopics'][subtopic_name] = False
                self.save_plan()
                print(f'Subtopic "{subtopic_name}" added to topic "{topic_name}" successfully.')
            else:
                print(f'Subtopic "{subtopic_name}" already exists for topic "{topic_name}".')
        else:
            print(f'Topic "{topic_name}" does not exist.')

    # Deleting subtopics
    def remove_subtopic(self, topic_name, subtopic_name):
        if topic_name in self.study_plan['topics']:
            if subtopic_name in self.study_plan['topics'][topic_name]['subtopics']:
                del self.study_plan['topics'][topic_name]['subtopics'][subtopic_name]
                self.save_plan()
                print(f'Subtopic "{subtopic_name}" removed from topic "{topic_name}" successfully.')
            else:
                print(f'Subtopic "{subtopic_name}" does not exist for topic "{topic_name}".')
        else:
            print(f'Topic "{topic_name}" does not exist.')

    # Marking completed subtopics
    def mark_completed(self, topic_name, subtopic_name):
        if topic_name in self.study_plan['topics']:
            if subtopic_name in self.study_plan['topics'][topic_name]['subtopics']:
                self.study_plan['topics'][topic_name]['subtopics'][subtopic_name] = True
                self.study_plan['topics'][topic_name]['completed'].append(subtopic_name)
                self.save_plan()
                print(f'Subtopic "{subtopic_name}" marked as completed for topic "{topic_name}".')
            else:
                print(f'Subtopic "{subtopic_name}" does not exist for topic "{topic_name}".')
        else:
            print(f'Topic "{topic_name}" does not exist.')

    # Displaying the topic plan
    def display_plan(self):
        print("\nStudy Plan:")
        for topic, details in self.study_plan['topics'].items():
            print(f"\nTopic: {topic}")
            if details['subtopics']:
                print("  Subtopics:")
                for subtopic, completed in details['subtopics'].items():
                    status = "Completed" if completed else "Not Completed"
                    print(f"    - {subtopic} ({status})")
            # if details['completed']:
            #     print("  Completed Subtopics:")
            #     for subtopic in details['completed']:
            #         print(f"    - {subtopic}")

    def run(self):
        while True:
            print("\n1. Display Plan")
            print("2. Add Topic")
            print("3. Remove Topic")
            print("4. Add Subtopic")
            print("5. Remove Subtopic")
            print("6. Mark Subtopic as Completed")
            print("7. Save and Exit")

            choice = input("Enter your choice (1-7): ")

            if choice == "1":
                self.display_plan()
            elif choice == "2":
                topic_name = input("Enter the name of the topic: ")
                self.add_topic(topic_name)
            elif choice == "3":
                topic_name = input("Enter the name of the topic: ")
                self.remove_topic(topic_name)
            elif choice == "4":
                topic_name = input("Enter the name of the topic: ")
                subtopic_name = input("Enter the name of the subtopic: ")
                self.add_subtopic(topic_name, subtopic_name)
            elif choice == "5":
                topic_name = input("Enter the name of the topic: ")
                subtopic_name = input("Enter the name of the subtopic: ")
                self.remove_subtopic(topic_name, subtopic_name)
            elif choice == "6":
                topic_name = input("Enter the name of the topic: ")
                subtopic_name = input("Enter the name of the subtopic: ")
                self.mark_completed(topic_name, subtopic_name)
            elif choice == "7":
                self.save_plan()
                break
            else:
                print("Invalid choice. Please enter a number from 1 to 7.")


if __name__ == "__main__":
    planner = StudyPlanner()
    planner.run()
# Приклад використання:
# planner = StudyPlanner()
#
# # Додавання  підтем
# planner.add_topic("Python Basics")
# planner.add_subtopic("Python Basics", "Variables")
# planner.display_plan()
#
# # Відмічання пройдених підтем
# planner.mark_completed("Python Basics", "Variables")
# planner.display_plan()
#
# # Видалення теми та відображення тем плану
# planner.remove_topic("Python Basics")
# planner.display_plan()
