import json

class StudyPlan:
    def __init__(self):
        self.topics = {
            "1": {"name": "Основи мови Python", "subtopics": ["Введення у Python", "Змінні та типи даних", "Оператори та вирази"]},
            "2": {"name": "Структури даних в Python", "subtopics": ["Списки", "Кортежі", "Стрічки"]},
            # ... Додайте інші теми тут
        }
        self.completed_topics = set()

    def mark_as_completed(self, topic_number):
        self.completed_topics.add(topic_number)

    def display_plan(self):
        print("Студентський план:")
        for topic_number, topic_info in self.topics.items():
            status = "Пройдено" if topic_number in self.completed_topics else "Не пройдено"
            print(f"{topic_number}. {topic_info['name']} ({status})")
            for subtopic in topic_info["subtopics"]:
                print(f"   - {subtopic}")

    def save_to_file(self, filename):
        with open(filename, 'w') as file:
            json.dump({"completed_topics": list(self.completed_topics)}, file)

    def load_from_file(self, filename):
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
                self.completed_topics = set(data.get("completed_topics", []))
        except FileNotFoundError:
            print("Файл не знайдено. Починаємо спочатку.")

def main():
    study_plan = StudyPlan()
    study_plan.load_from_file("study_plan.json")

    while True:
        study_plan.display_plan()
        print("\n1. Відмітити тему як пройдену")
        print("2. Зберегти і вийти")
        choice = input("Ваш вибір (1 або 2): ")

        if choice == "1":
            topic_number = input("Введіть номер теми, яку ви хочете відмітити: ")
            study_plan.mark_as_completed(topic_number)
        elif choice == "2":
            study_plan.save_to_file("study_plan.json")
            print("Дякую! Ваші результати збережено.")
            break
        else:
            print("Невірний вибір. Будь ласка, введіть 1 або 2.")

if __name__ == "__main__":
    main()
