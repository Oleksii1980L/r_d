
import json
import tkinter as tk
from tkinter import simpledialog, filedialog
import tkinter.messagebox


class StudyPlannerGUI(tk.Tk):
    def __init__(self):

        self.is_plan_saved = True  # План вважається вже збереженим

        super().__init__()
        self.study_plan = {'topics': {}}
        self.current_file = None

        self.title("Study Planner")
        self.geometry("300x300")
        # Це створює екземпляр класу menu, який буде головним меню програми. self вказує
        # , що це меню пов'язане з екземпляром StudyPlannerGUI
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
        # створює каскадний пункт меню "Options" і пов'язує його з підменю file_menu, яке містить команди
        # для роботи з файлами та опціями програми.
        self.menu.add_cascade(label="Options", menu=file_menu)

    # відповідає за завершення роботи програми.
    def exit_program(self):
        self.destroy()

    def load_plan(self):
        #  відкриває діалогове вікно для вибору файлу
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        # Перевіряється, чи користувач взагалі вибрав файл.
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as file:
                # Зчитується вміст файлу JSON та зберігається в атрибуті study_plan екземпляра класу.
                self.study_plan = json.load(file)
            # Перебирає всі теми та підтеми при завантаженні
            for topic_name in self.study_plan.get('topics', {}):
                # перевіряє теми на завершеність та оновлює інформацію відповідно.
                self.check_topic_completion(topic_name)
            # Зберігає шлях до поточного файлу.
            self.current_file = file_path
            # відображає план навчання у вікні програми.
            self.display_plan()

    #  робить збереження плану навчання в поточний файл або вибирає новий для збереження,якщо не був збережений раніше.
    def save_plan(self):
        if self.current_file:
            with open(self.current_file, 'w') as file:
                json.dump(self.study_plan, file, indent=2)
            self.is_plan_saved = True  # Позначаємо, що план збережений
        else:
            self.save_plan_as()

    #  дозволяє користувачеві вибрати новий файл для збереження плану навчання та зберігає його
    def save_plan_as(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'w') as file:
                json.dump(self.study_plan, file, indent=2)
            self.current_file = file_path
            self.is_plan_saved = True  # Позначаємо, що план збережений

    # взаємодіє з користувачем для створення нової теми та введення інформації про нову тему та реагує на введені дані,
    # оновлюючи план навчаннята виводячи інформацію користувачеві.
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

    #  функція відповідає за видалення теми з плану навчання.
    def remove_topic(self):
        topic_name = simpledialog.askstring("Remove Topic", "Enter the name of the topic:")
        # Перевіряє, чи введена назва теми не є порожньою та чи вона існує в плані.
        if topic_name:
            if topic_name in self.study_plan['topics']:
                del self.study_plan['topics'][topic_name]
                self.save_plan()
                self.display_plan()
            else:
                tk.messagebox.showinfo("Info", f'Topic "{topic_name}" does not exist.')

    # відповідає за додавання нової підтеми до теми в плані навчання.
    def add_subtopic(self):
        # щоб отримати від користувача назву теми (topic_name), назву нової підтеми (subtopic_name)
        # та дедлайн для підтеми (deadline)
        topic_name = simpledialog.askstring("Add Subtopic", "Enter the name of the topic:")
        subtopic_name = simpledialog.askstring("Add Subtopic", "Enter the name of the subtopic:")
        deadline = simpledialog.askstring("Add Subtopic", "Enter the deadline for the subtopic (YYYY-MM-DD):")
        if topic_name and subtopic_name:
            # Перевіряє, чи тема, до якої користувач хоче додати підтему, існує в плані.
            if topic_name in self.study_plan['topics']:
                topic = self.study_plan['topics'][topic_name]
                subtopics = topic.get('subtopics', {})

                if subtopic_name not in subtopics:
                    subtopics[subtopic_name] = {'completed': False, 'deadline': deadline}
                    topic['subtopics'] = subtopics

                    # Оновлення дедлайну теми, якщо всі підтеми Completed
                    if all(subtopic.get('completed', False) for subtopic in subtopics.values()):
                        topic['deadline'] = 'Completed'

                    self.save_plan()  # Зберігає оновлений план навчання.
                    self.display_plan()  # Оновлення відображення плану
                else:
                    tk.messagebox.showinfo("Info",
                                           f'Subtopic "{subtopic_name}" already exists for topic "{topic_name}"'
                                           f'. You can edit the deadline.')
            else:
                tk.messagebox.showinfo("Info", f'Topic "{topic_name}" does not exist.')
        else:
            # якщо topic_name або subtopic_name порожні - виведення повідомлення про невірні дані
            tk.messagebox.showinfo("Info", "Invalid topic or subtopic name.")

    # видалення підтеми з вказаної теми
    def remove_subtopic(self):
        topic_name = simpledialog.askstring("Remove Subtopic", "Enter the name of the topic:")
        subtopic_name = simpledialog.askstring("Remove Subtopic", "Enter the name of the subtopic:")
        if topic_name and subtopic_name:
            if topic_name in self.study_plan['topics']:
                # Перевіряє, чи підтема з вказаною назвою існує в підтемах обраної теми.
                if subtopic_name in self.study_plan['topics'][topic_name]['subtopics']:
                    # Видаляє вказану підтему з теми в плані навчання.
                    del self.study_plan['topics'][topic_name]['subtopics'][subtopic_name]
                    self.save_plan()  # Зберігає оновлений план навчання.
                    self.display_plan()  # Оновлює відображення плану навчання.
                else:
                    tk.messagebox.showinfo("Info",
                                           f'Subtopic "{subtopic_name}" does not exist for topic "{topic_name}".')
            else:
                tk.messagebox.showinfo("Info", f'Topic "{topic_name}" does not exist.')
        else:
            # якщо topic_name або subtopic_name порожні - виведення повідомлення про невірні дані
            tk.messagebox.showinfo("Info", "Invalid topic or subtopic name.")

    # встановлення статусу "completed" для підтеми вказаної теми.
    def mark_completed(self):
        # вікно, в якому користувач повинен ввести назву теми
        topic_name = simpledialog.askstring("Mark Subtopic as Completed", "Enter the name of the topic:")
        #  вікно, в якому користувач повинен ввести назву підтеми
        subtopic_name = simpledialog.askstring("Mark Subtopic as Completed", "Enter the name of the subtopic:")

        if topic_name and subtopic_name:
            #  Перевіряє, чи тема з вказаною назвою існує в плані навчання.
            if topic_name in self.study_plan['topics']:
                topic = self.study_plan['topics'][topic_name]
                # Перевіряє, чи підтема з вказаною назвою існує в підтемах обраної теми.
                if 'subtopics' in topic and subtopic_name in topic['subtopics']:
                    subtopic = topic['subtopics'][subtopic_name]

                    # Встановлюємо статус підтеми на True
                    subtopic['completed'] = True
                    # Перевіряє, чи всі підтеми вказаної теми тепер виконані (completed),
                    # і встановлює статус "completed" для теми, якщо так.
                    self.check_topic_completion(topic_name)
                    self.save_plan()  # Зберігає оновлений план навчання.
                    self.display_plan()  # Оновлення відображення плану
                else:
                    tk.messagebox.showinfo("Info",
                                           f'Subtopic "{subtopic_name}" does not exist '
                                           f'for topic "{topic_name}".')
            else:
                tk.messagebox.showinfo("Info", f'Topic "{topic_name}" does not exist.')

    # визначає, чи всі підтеми для даної теми виконані (completed), і відповідно встановлює або скасовує статус
    # "completed" для самої теми.
    def check_topic_completion(self, topic_name):
        topic = self.study_plan['topics'][topic_name]
        # Функція all повертає True,якщо всі елементи вказаного ітерабельного об'єкта'
        # 'є істинними.перевіряє всі підтеми на значення 'completed',що дорівнює True.
        all_subtopics_completed = all(
            sub_details.get('completed', False)  # Для кожної підтеми отримує значення ключа 'completed'.
            # Якщо ключ відсутній, повертається значення за замовчуванням, яке в даному випадку є False.
            for sub_details in topic.get('subtopics', {}).values()  # Отримує словник усіх підтем для обраної теми.
            # Якщо в темі немає підтем, повертається порожній словник.
        )
        # Перевіряє, чи всі підтеми виконані і чи тема ще не відзначена як виконана
        if all_subtopics_completed and not topic.get('completed', False):
            topic['completed'] = True  # Встановлює статус "completed" для теми.
            topic['deadline'] = "Completed"  # Встановлює дедлайн теми як "Completed".
            self.save_plan()
            self.display_plan()
        elif not all_subtopics_completed and topic.get('completed', False):
            topic['completed'] = False
            self.save_plan()

    #  для зміни дедлайну для обраної теми в плані навчання.
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

    # Код для відображення плану...
    def display_plan(self):
        if not self.is_plan_saved:  # Зберігаємо план, якщо він був змінений
            self.save_plan()
        # Створює рядок plan_text з заголовком "Study Plan:".
        plan_text = "\nStudy Plan:"
        # Ітерується по темам в плані навчання та додає інформацію про кожну тему до рядка plan_text,
        # включаючи назву теми та дедлайн (якщо вказано).
        for topic, details in self.study_plan['topics'].items():
            deadline = details.get('deadline', 'No deadline')
            plan_text += f"\n\nTopic: {topic} (Deadline: {deadline})"
            # Якщо у теми є підтеми, то для кожної підтеми додає інформацію до рядка plan_text, включаючи назву підтеми
            # та її статус (виконана чи ні).
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

        # Викликає діалогове вікно з інформацією про план навчання, де виводиться рядок plan_text.
        tk.messagebox.showinfo("Study Plan", plan_text)

    # зберігає поточний план навчання та завершує програму
    def save_and_exit(self):
        self.save_plan()
        self.destroy()  # закриває головне вікно програми,що призводить до завершення виконання програми.


# Ця конструкція перевіряє, чи файл виконується безпосередньо (а не імпортований як модуль у інший скрипт)
if __name__ == "__main__":
    planner = StudyPlannerGUI()  # Створюєм екземпляр класу StudyPlannerGUI,-графічний інтерфейс програми план.навчання.
    planner.mainloop()  # Запускає цикл обробки подій Tkinter. Цей метод очікує на події (такі як натискання кнопок,
    # ресайз вікна тощо) і викликає відповідні функції обробки подій. Поки вікно не буде закрито або не буде викликано
