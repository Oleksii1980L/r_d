import json

class StudyPlanner:
    def __init__(self, plan_file='study_plan.json'):
        self.plan_file = plan_file
        self.study_plan = self.load_plan()

    def load_plan(self):
        try:
            with open(self.plan_file, 'r') as file:
                study_plan = json.load(file)
            return study_plan
        except FileNotFoundError:
            return {'topics': {}}

    def save_plan(self):
        with open(self.plan_file, 'w') as file:
            json.dump(self.study_plan, file, indent=2)

    def add_topic(self, topic_name):
        if topic_name not in self.study_plan['topics']:
            self.study_plan['topics'][topic_name] = {'subtopics': {}, 'completed': []}
            self.save_plan()
            print(f'Topic "{topic_name}" added successfully.')
        else:
            print(f'Topic "{topic_name}" already exists.')

    def remove_topic(self, topic_name):
        if topic_name in self.study_plan['topics']:
            del self.study_plan['topics'][topic_name]
            self.save_plan()
            print(f'Topic "{topic_name}" removed successfully.')
        else:
            print(f'Topic "{topic_name}" does not exist.')

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

    def display_plan(self):
        print("\nStudy Plan:")
        for topic, details in self.study_plan['topics'].items():
            print(f"\nTopic: {topic}")
            if details['subtopics']:
                print("  Subtopics:")
                for subtopic, completed in details['subtopics'].items():
                    status = "Completed" if completed else "Not Completed"
                    print(f"    - {subtopic} ({status})")
            if details['completed']:
                print("  Completed Subtopics:")
                for subtopic in details['completed']:
                    print(f"    - {subtopic}")

# Приклад використання:
planner = StudyPlanner()

# Додавання та відображення тем
planner.add_topic("Python Basics")
planner.add_subtopic("Python Basics", "Variables")
planner.display_plan()

# Відмічання пройдених тем
planner.mark_completed("Python Basics", "Variables")
planner.display_plan()

# Видалення теми та відображення плану
planner.remove_topic("Python Basics")
planner.display_plan()
