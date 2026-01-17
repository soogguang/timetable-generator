import tkinter as tk
from tkinter import messagebox, ttk
from collections import defaultdict

# 강의 정보를 담는 Lecture 클래스
class Lecture:
    def __init__(self, subject, professor, schedule, section=None):
        # 강의의 속성을 초기화
        self.subject = subject  # 과목명
        self.professor = professor  # 교수명
        self.schedule = schedule  # 강의 일정 (딕셔너리 형태)
        self.section = section  # 분반 (옵션)

    def __str__(self):
        # 강의 일정을 문자열로 생성
        schedule_str = ', '.join(
            [f"{day}: {times[0]:02d}:{times[1]:02d}-{times[2]:02d}:{times[3]:02d}" for day, times in self.schedule.items()])
        if self.section:
            return f"{self.subject} ({self.section}) by {self.professor} on {schedule_str}"
        else:
            return f"{self.subject} by {self.professor} on {schedule_str}"

# 과목 정보를 담는 Subject 클래스
class Subject:
    def __init__(self, name):
        self.name = name
        self.lectures = []  # 강의 리스트 초기화

    def add_lecture(self, lecture):
        self.lectures.append(lecture)  # 강의 추가

    def remove_lecture(self, lecture):
        self.lectures.remove(lecture)  # 강의 삭제

    def __str__(self):
        return f"{self.name}: {len(self.lectures)} 강의"

# 강의 시간 충돌을 확인하는 함수
def check_conflict(lecture1, lecture2):
    for day, times1 in lecture1.schedule.items():
        if day in lecture2.schedule:
            times2 = lecture2.schedule[day]
            start1 = times1[0] * 60 + times1[1]
            end1 = times1[2] * 60 + times1[3]
            start2 = times2[0] * 60 + times2[1]
            end2 = times2[2] * 60 + times2[3]
            if not (end1 <= start2 or end2 <= start1):
                return True  # 시간 충돌 발생
    return False  # 시간 충돌 없음

# 예비 시간표를 생성하는 함수
def create_preliminary_timetables(subjects):
    from itertools import product
    all_lectures = [subject.lectures for subject in subjects]
    all_combinations = list(product(*all_lectures))
    valid_timetables = []

    for combination in all_combinations:
        timetable = []
        conflict = False
        subject_sections = {}

        for lecture in combination:
            if any(check_conflict(lecture, existing) for existing in timetable):
                conflict = True
                break

            if lecture.subject in subject_sections:
                if subject_sections[lecture.subject] != lecture.section:
                    conflict = True
                    break
            else:
                subject_sections[lecture.subject] = lecture.section

            timetable.append(lecture)

        if not conflict:
            valid_timetables.append(timetable)

    return valid_timetables

# 시간표를 정렬하는 함수
def sort_timetable(timetable):
    days_order = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    timetable.sort(
        key=lambda lec: (days_order.index(list(lec.schedule.keys())[0]),
                         list(lec.schedule.values())[0][0] * 60 + list(lec.schedule.values())[0][1]))
    return timetable

# 삭제할 과목을 추천하는 함수
def recommend_removals(preliminary_timetable, elective_lectures):
    conflicts = []
    for elective in elective_lectures:
        for lecture in preliminary_timetable:
            if check_conflict(elective, lecture):
                conflicts.append(elective)
                break
    return conflicts

# 시간표 생성 앱 클래스
class TimetableApp:
    def __init__(self, root):
        self.root = root
        self.root.title("시간표 생성 프로그램")

        self.mandatory_subjects = []  # 필수 과목 리스트
        self.electives = []  # 선택 과목 리스트
        self.selected_timetable = []  # 선택된 시간표

        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.initialize_subjects()  # 초기 과목 데이터를 설정하는 메서드 호출
        self.create_main_screen()

    # 프레임을 초기화하는 함수
    def clear_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    # 초기 과목 데이터를 설정하는 함수
    def initialize_subjects(self):
        # 비판적사고와표현 과목 초기 데이터
        critical_thinking = Subject("비판적사고와표현")
        critical_thinking.add_lecture(Lecture("비판적사고와표현", "구태운", {"Wed": (11, 00, 12, 50)}, "비판적사고와학술적글쓰기"))
        critical_thinking.add_lecture(Lecture("비판적사고와표현", "김희진", {"Wed": (11, 00, 12, 50)}, "비판적사고와학술적글쓰기"))
        critical_thinking.add_lecture(Lecture("비판적사고와표현", "김문정", {"Wed": (11, 00, 12, 50)}, "비판적사고와학술적글쓰기"))
        critical_thinking.add_lecture(Lecture("비판적사고와표현", "박소영", {"Wed": (11, 00, 12, 50)}, "미디어사회와비평적글쓰기"))
        critical_thinking.add_lecture(Lecture("비판적사고와표현", "손민달", {"Wed": (11, 00, 12, 50)}, "기술혁신사회와과학기술글쓰기"))
        self.mandatory_subjects.append(critical_thinking)

        # 컴퓨팅적사고 과목 초기 데이터
        computing_thinking = Subject("컴퓨팅적사고")
        computing_thinking.add_lecture(Lecture("컴퓨팅적사고", "봉진숙", {"Mon": (12, 00, 13, 15)}, "컴퓨팅적사고와활용"))
        computing_thinking.add_lecture(Lecture("컴퓨팅적사고", "이희찬", {"Mon": (12, 00, 13, 15)}, "컴퓨팅적사고와코딩기초"))
        computing_thinking.add_lecture(Lecture("컴퓨팅적사고", "노현아", {"Mon": (12, 00, 13, 15)}, "컴퓨팅적사고와코딩기초"))
        computing_thinking.add_lecture(Lecture("컴퓨팅적사고", "윤수연", {"Mon": (12, 00, 13, 15)}, "컴퓨팅적사고와코딩기초"))
        computing_thinking.add_lecture(Lecture("컴퓨팅적사고", "노은희", {"Mon": (12, 00, 13, 15)}, "컴퓨팅적사고와알고리즘"))
        self.mandatory_subjects.append(computing_thinking)

        # 프로그래밍및실습1 과목 초기 데이터
        programming_and_practice1 = Subject("프로그래밍및실습1")
        programming_and_practice1.add_lecture(Lecture("프로그래밍및실습1", "김성신", {"Mon": (13, 30, 15, 20), "Wed" : (15, 30, 17, 20)}, "가"))
        programming_and_practice1.add_lecture(Lecture("프로그래밍및실습1", "김성신", {"Mon": (15, 30, 17, 20), "Wed" : (13, 30, 15, 20)}, "나"))
        programming_and_practice1.add_lecture(Lecture("프로그래밍및실습1", "김성신", {"Tue": (13, 30, 15, 20), "Fri" : (15, 30, 17, 20)}, "다"))
        programming_and_practice1.add_lecture(Lecture("프로그래밍및실습1", "김성신", {"Tue": (15, 30, 17, 20), "Fri" : (13, 30, 15, 20)}, "라"))
        self.mandatory_subjects.append(programming_and_practice1)

        # 기초AI수학 과목 초기 데이터
        basic_ai_math = Subject("기초AI수학")
        basic_ai_math.add_lecture(Lecture("기초AI수학", "윤진혁", {"Tue": (10, 30, 11, 45), "Fri" : (10, 30, 11, 45)}, "가"))
        basic_ai_math.add_lecture(Lecture("기초AI수학", "윤진혁", {"Mon": (12, 00, 13, 15), "Wed" : (12, 00, 13, 15)}, "나"))
        self.mandatory_subjects.append(basic_ai_math)

        # 물리및실험 과목 초기 데이터
        physics_and_experiment = Subject("물리및실험")
        physics_and_experiment.add_lecture(Lecture("물리및실험", "최현희, 이순녀", {"Thu": (9, 00, 12, 50)}, "가"))
        physics_and_experiment.add_lecture(Lecture("물리및실험", "최현희, 이동재", {"Thu": (9, 00, 12, 50)}, "나"))
        physics_and_experiment.add_lecture(Lecture("물리및실험", "이재구, 최현희", {"Thu": (9, 00, 12, 50)}, "다"))
        physics_and_experiment.add_lecture(Lecture("물리및실험", "김종안, 최현희", {"Thu": (9, 00, 12, 50)}, "라"))
        self.mandatory_subjects.append(physics_and_experiment)

    # 메인 화면을 생성하는 함수
    def create_main_screen(self):
        self.clear_frame(self.main_frame)

        title_label = tk.Label(self.main_frame, text="시간표 생성 프로그램", font=("Arial", 24))
        title_label.pack(pady=20)

        buttons = [
            ("필수 과목 관리", self.create_mandatory_subject_screen),
            ("교양 과목 관리", self.create_elective_subject_screen),
            ("종료", self.root.quit)
        ]

        for (text, command) in buttons:
            button = tk.Button(self.main_frame, text=text, command=command, font=("Arial", 14))
            button.pack(pady=10, padx=20, fill="x")

    # 필수 과목 관리 화면을 생성하는 함수
    def create_mandatory_subject_screen(self):
        self.clear_frame(self.main_frame)

        title_label = tk.Label(self.main_frame, text="시간표 생성 프로그램", font=("Arial", 24))
        title_label.pack(pady=20)

        buttons = [
            ("필수 과목 리스트 확인하기", self.show_mandatory_subjects),
            ("필수 과목 추가하기", self.add_mandatory_subject),
            ("필수 과목 삭제하기", self.delete_mandatory_subject),
            ("예비 시간표 생성하기", self.create_preliminary_timetable),
            ("뒤로가기", self.create_main_screen)
        ]

        for (text, command) in buttons:
            button = tk.Button(self.main_frame, text=text, command=command, font=("Arial", 14))
            button.pack(pady=10, padx=20, fill="x")

    # 선택 과목 관리 화면을 생성하는 함수
    def create_elective_subject_screen(self):
        self.clear_frame(self.main_frame)

        title_label = tk.Label(self.main_frame, text="시간표 생성 프로그램", font=("Arial", 24))
        title_label.pack(pady=20)

        buttons = [
            ("선택 과목 리스트 확인하기", self.show_elective_subjects),
            ("선택 과목 추가하기", self.add_elective_subject),
            ("선택 과목 삭제하기", self.delete_elective_subject),
            ("시간표 생성하기", self.create_final_timetable),
            ("뒤로가기", self.create_main_screen)
        ]

        for (text, command) in buttons:
            button = tk.Button(self.main_frame, text=text, command=command, font=("Arial", 14))
            button.pack(pady=10, padx=20, fill="x")

    # 필수 과목 리스트를 보여주는 함수
    def show_mandatory_subjects(self):
        self.clear_frame(self.main_frame)

        label = tk.Label(self.main_frame, text="필수과목 리스트 확인하기", font=("Arial", 18))
        label.pack(pady=20)

        canvas = tk.Canvas(self.main_frame)
        scroll_y = tk.Scrollbar(self.main_frame, orient="vertical", command=canvas.yview)

        table_frame = tk.Frame(canvas)

        headers = ["과목명", "분반", "교수명", "강의시간"]
        for i, header in enumerate(headers):
            label = tk.Label(table_frame, text=header, borderwidth=1, relief="solid", width=18)
            label.grid(row=0, column=i)

        row = 1
        for subject in self.mandatory_subjects:
            for lecture in subject.lectures:
                label = tk.Label(table_frame, text=subject.name, borderwidth=1, relief="solid", width=18)
                label.grid(row=row, column=0)
                label = tk.Label(table_frame, text=lecture.section, borderwidth=1, relief="solid", width=22)
                label.grid(row=row, column=1)
                label = tk.Label(table_frame, text=lecture.professor, borderwidth=1, relief="solid", width=18)
                label.grid(row=row, column=2)
                label = tk.Label(table_frame, text=", ".join([f"{day}: {start:02d}:{start_m:02d}-{end:02d}:{end_m:02d}" for day, (start, start_m, end, end_m) in lecture.schedule.items()]), borderwidth=1, relief="solid", width=40)
                label.grid(row=row, column=3)
                row += 1

        table_frame.update_idletasks()

        canvas.create_window(0, 0, anchor='nw', window=table_frame)
        canvas.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox('all'), yscrollcommand=scroll_y.set)

        canvas.pack(fill='both', expand=True, side='left')
        scroll_y.pack(fill='y', side='right')

        back_button = tk.Button(self.main_frame, text="뒤로가기", command=self.create_mandatory_subject_screen, font=("Arial", 14))
        back_button.pack(pady=20)

        # 창 크기를 조정하여 테이블에 맞게 설정
        self.main_frame.update_idletasks()
        width = min(self.main_frame.winfo_width(), 800)
        height = min(self.main_frame.winfo_height(), 600)
        self.root.geometry(f"{width}x{height}")

        # 화면 중앙에 창을 배치
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f"+{x}+{y}")

    # 선택 과목 리스트를 보여주는 함수
    def show_elective_subjects(self):
        self.clear_frame(self.main_frame)

        label = tk.Label(self.main_frame, text="선택 과목 리스트 확인하기", font=("Arial", 18))
        label.pack(pady=20)

        table_frame = tk.Frame(self.main_frame)
        table_frame.pack()

        headers = ["과목명", "분반", "교수명", "강의시간"]
        for i, header in enumerate(headers):
            label = tk.Label(table_frame, text=header, borderwidth=1, relief="solid", width=18)
            label.grid(row=0, column=i)

        for row, lecture in enumerate(self.electives, start=1):
            label = tk.Label(table_frame, text=lecture.subject, borderwidth=1, relief="solid", width=18)
            label.grid(row=row, column=0)
            label = tk.Label(table_frame, text=lecture.section, borderwidth=1, relief="solid", width=22)
            label.grid(row=row, column=1)
            label = tk.Label(table_frame, text=lecture.professor, borderwidth=1, relief="solid", width=18)
            label.grid(row=row, column=2)
            label = tk.Label(table_frame, text=", ".join([f"{day}: {start:02d}:{start_m:02d}-{end:02d}:{end_m:02d}" for day, (start, start_m, end, end_m) in lecture.schedule.items()]), borderwidth=1, relief="solid", width=40)
            label.grid(row=row, column=3)

        back_button = tk.Button(self.main_frame, text="뒤로가기", command=self.create_elective_subject_screen, font=("Arial", 14))
        back_button.pack(pady=20)

    # 필수 과목을 추가하는 화면을 생성하는 함수
    def add_mandatory_subject(self):
        self.clear_frame(self.main_frame)

        label = tk.Label(self.main_frame, text="필수 과목 추가하기", font=("Arial", 18))
        label.pack(pady=20)

        form_frame = tk.Frame(self.main_frame)
        form_frame.pack()

        labels = ["과목명", "교수명", "분반", "요일 (e.g., Mon)", "시작시간 (e.g., 09:00)", "종료시간 (e.g., 10:30)"]
        self.entries = {}

        for i, text in enumerate(labels):
            label = tk.Label(form_frame, text=text, width=20)
            label.grid(row=i, column=0, padx=10, pady=5)
            entry = tk.Entry(form_frame, width=30)
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.entries[text] = entry

        add_time_button = tk.Button(self.main_frame, text="시간추가하기", command=self.add_schedule_time, font=("Arial", 14))
        add_time_button.pack(pady=10)

        add_subject_button = tk.Button(self.main_frame, text="필수 과목 추가하기", command=self.save_mandatory_subject, font=("Arial", 14))
        add_subject_button.pack(pady=10)

        back_button = tk.Button(self.main_frame, text="뒤로가기", command=self.create_mandatory_subject_screen, font=("Arial", 14))
        back_button.pack(pady=20)

        self.schedule = {}

    # 시간 추가를 위한 함수
    def add_schedule_time(self):
        day = self.entries["요일 (e.g., Mon)"].get()
        start = self.entries["시작시간 (e.g., 09:00)"].get()
        end = self.entries["종료시간 (e.g., 10:30)"].get()

        try:
            start_hour, start_minute = map(int, start.split(":"))
            end_hour, end_minute = map(int, end.split(":"))
            self.schedule[day] = (start_hour, start_minute, end_hour, end_minute)
            messagebox.showinfo("성공", f"{day} {start}-{end} 추가됨.")
        except ValueError:
            messagebox.showerror("오류", "시간 형식이 올바르지 않습니다. (e.g., 09:00)")

        self.entries["요일 (e.g., Mon)"].delete(0, tk.END)
        self.entries["시작시간 (e.g., 09:00)"].delete(0, tk.END)
        self.entries["종료시간 (e.g., 10:30)"].delete(0, tk.END)

    # 필수 과목을 저장하는 함수
    def save_mandatory_subject(self):
        subject_name = self.entries["과목명"].get()
        professor = self.entries["교수명"].get()
        section = self.entries["분반"].get() or None

        if not subject_name or not professor or not self.schedule:
            messagebox.showerror("오류", "모든 필드를 입력해주세요.")
            return

        lecture = Lecture(subject_name, professor, self.schedule, section)
        subject = next((sub for sub in self.mandatory_subjects if sub.name == subject_name), None)
        if subject is None:
            subject = Subject(subject_name)
            self.mandatory_subjects.append(subject)
        subject.add_lecture(lecture)

        messagebox.showinfo("성공", "필수 과목이 추가되었습니다.")
        self.create_mandatory_subject_screen()

    # 필수 과목을 삭제하는 화면을 생성하는 함수
    def delete_mandatory_subject(self):
        self.clear_frame(self.main_frame)

        label = tk.Label(self.main_frame, text="필수 과목 삭제하기", font=("Arial", 18))
        label.pack(pady=20)

        table_frame = tk.Frame(self.main_frame)
        table_frame.pack()

        headers = ["Index", "과목명", "분반", "교수명", "강의시간"]
        for i, header in enumerate(headers):
            label = tk.Label(table_frame, text=header, borderwidth=1, relief="solid", width=22)
            label.grid(row=0, column=i)

        self.lecture_map = {}
        row = 1
        index = 1
        for subject in self.mandatory_subjects:
            for lecture in subject.lectures:
                self.lecture_map[index] = (subject, lecture)
                label = tk.Label(table_frame, text=str(index), borderwidth=1, relief="solid", width=22)
                label.grid(row=row, column=0)
                label = tk.Label(table_frame, text=subject.name, borderwidth=1, relief="solid", width=22)
                label.grid(row=row, column=1)
                label = tk.Label(table_frame, text=lecture.section, borderwidth=1, relief="solid", width=22)
                label.grid(row=row, column=2)
                label = tk.Label(table_frame, text=lecture.professor, borderwidth=1, relief="solid", width=22)
                label.grid(row=row, column=3)
                label = tk.Label(table_frame, text=", ".join([f"{day}: {start:02d}:{start_m:02d}-{end:02d}:{end_m:02d}" for day, (start, start_m, end, end_m) in lecture.schedule.items()]), borderwidth=1, relief="solid", width=30)
                label.grid(row=row, column=4)
                row += 1
                index += 1

        self.delete_index_entry = tk.Entry(self.main_frame, width=10)
        self.delete_index_entry.pack(pady=10)

        delete_button = tk.Button(self.main_frame, text="필수 과목 삭제하기", command=self.confirm_delete, font=("Arial", 14))
        delete_button.pack(pady=10)

        back_button = tk.Button(self.main_frame, text="뒤로가기", command=self.create_mandatory_subject_screen, font=("Arial", 14))
        back_button.pack(pady=20)

    # 필수 과목 삭제 확인 함수
    def confirm_delete(self):
        try:
            index = int(self.delete_index_entry.get())
            if index in self.lecture_map:
                subject, lecture = self.lecture_map[index]
                subject.remove_lecture(lecture)
                if not subject.lectures:
                    self.mandatory_subjects.remove(subject)
                messagebox.showinfo("성공", "필수 과목이 삭제되었습니다.")
            else:
                messagebox.showerror("오류", "유효하지 않은 인덱스입니다.")
        except ValueError:
            messagebox.showerror("오류", "인덱스는 숫자여야 합니다.")

    # 예비 시간표를 생성하는 화면을 생성하는 함수
    def create_preliminary_timetable(self):
        self.clear_frame(self.main_frame)

        label = tk.Label(self.main_frame, text="예비 시간표 생성하기", font=("Arial", 18))
        label.pack(pady=20)

        preliminary_timetables = create_preliminary_timetables(self.mandatory_subjects)
        self.timetable_map = {}

        canvas = tk.Canvas(self.main_frame)
        scroll_y = tk.Scrollbar(self.main_frame, orient="vertical", command=canvas.yview)

        table_frame = tk.Frame(canvas)

        headers = ["Index", "예비 시간표 초안"]
        for i, header in enumerate(headers):
            label = tk.Label(table_frame, text=header, borderwidth=1, relief="solid", width=20)
            label.grid(row=0, column=i)

        for index, timetable in enumerate(preliminary_timetables, start=1):
            self.timetable_map[index] = timetable
            label = tk.Label(table_frame, text=str(index), borderwidth=1, relief="solid", width=20)
            label.grid(row=index, column=0)
            label = tk.Label(table_frame, text="\n".join([str(lec) for lec in timetable]), borderwidth=1, relief="solid", width=50)
            label.grid(row=index, column=1)

        canvas.create_window(0, 0, anchor='nw', window=table_frame)
        canvas.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox('all'), yscrollcommand=scroll_y.set)

        canvas.pack(fill='both', expand=True, side='left')
        scroll_y.pack(fill='y', side='right')

        self.timetable_index_entry = tk.Entry(self.main_frame, width=10)
        self.timetable_index_entry.pack(pady=10)

        select_button = tk.Button(self.main_frame, text="예비 시간표 선택하기", command=self.select_preliminary_timetable, font=("Arial", 14))
        select_button.pack(pady=10)

        back_button = tk.Button(self.main_frame, text="뒤로가기", command=self.create_mandatory_subject_screen, font=("Arial", 14))
        back_button.pack(pady=20)

    # 예비 시간표를 선택하는 함수
    def select_preliminary_timetable(self):
        try:
            index = int(self.timetable_index_entry.get())
            if index in self.timetable_map:
                self.selected_timetable = self.timetable_map[index]
                messagebox.showinfo("성공", "예비 시간표가 선택되었습니다.")
                self.create_elective_subject_screen()
            else:
                messagebox.showerror("오류", "유효하지 않은 인덱스입니다.")
        except ValueError:
            messagebox.showerror("오류", "인덱스는 숫자여야 합니다.")

    # 선택 과목을 추가하는 화면을 생성하는 함수
    def add_elective_subject(self):
        self.clear_frame(self.main_frame)

        label = tk.Label(self.main_frame, text="선택 과목 추가하기", font=("Arial", 18))
        label.pack(pady=20)

        form_frame = tk.Frame(self.main_frame)
        form_frame.pack()

        labels = ["과목명", "교수명", "분반", "요일 (e.g., Mon)", "시작시간 (e.g., 09:00)", "종료시간 (e.g., 10:30)"]
        self.entries = {}

        for i, text in enumerate(labels):
            label = tk.Label(form_frame, text=text, width=20)
            label.grid(row=i, column=0, padx=10, pady=5)
            entry = tk.Entry(form_frame, width=30)
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.entries[text] = entry

        add_time_button = tk.Button(self.main_frame, text="시간추가하기", command=self.add_elective_schedule_time, font=("Arial", 14))
        add_time_button.pack(pady=10)

        add_subject_button = tk.Button(self.main_frame, text="선택 과목 추가하기", command=self.save_elective_subject, font=("Arial", 14))
        add_subject_button.pack(pady=10)

        back_button = tk.Button(self.main_frame, text="뒤로가기", command=self.create_elective_subject_screen, font=("Arial", 14))
        back_button.pack(pady=20)

        self.schedule = {}

    # 선택 과목 시간 추가를 위한 함수
    def add_elective_schedule_time(self):
        day = self.entries["요일 (e.g., Mon)"].get()
        start = self.entries["시작시간 (e.g., 09:00)"].get()
        end = self.entries["종료시간 (e.g., 10:30)"].get()

        try:
            start_hour, start_minute = map(int, start.split(":"))
            end_hour, end_minute = map(int, end.split(":"))
            self.schedule[day] = (start_hour, start_minute, end_hour, end_minute)
            messagebox.showinfo("성공", f"{day} {start}-{end} 추가됨.")
        except ValueError:
            messagebox.showerror("오류", "시간 형식이 올바르지 않습니다. (e.g., 09:00)")

        self.entries["요일 (e.g., Mon)"].delete(0, tk.END)
        self.entries["시작시간 (e.g., 09:00)"].delete(0, tk.END)
        self.entries["종료시간 (e.g., 10:30)"].delete(0, tk.END)

    # 선택 과목을 저장하는 함수
    def save_elective_subject(self):
        subject_name = self.entries["과목명"].get()
        professor = self.entries["교수명"].get()
        section = self.entries["분반"].get() or None

        if not subject_name or not professor or not self.schedule:
            messagebox.showerror("오류", "모든 필드를 입력해주세요.")
            return

        lecture = Lecture(subject_name, professor, self.schedule, section)
        self.electives.append(lecture)

        messagebox.showinfo("성공", "선택 과목이 추가되었습니다.")
        self.create_elective_subject_screen()

    # 선택 과목을 삭제하는 화면을 생성하는 함수
    def delete_elective_subject(self):
        self.clear_frame(self.main_frame)

        label = tk.Label(self.main_frame, text="선택 과목 삭제하기", font=("Arial", 18))
        label.pack(pady=20)

        table_frame = tk.Frame(self.main_frame)
        table_frame.pack()

        headers = ["Index", "과목명", "분반", "교수명", "강의시간"]
        for i, header in enumerate(headers):
            label = tk.Label(table_frame, text=header, borderwidth=1, relief="solid", width=22)
            label.grid(row=0, column=i)

        self.elective_map = {}
        row = 1
        for index, lecture in enumerate(self.electives, start=1):
            self.elective_map[index] = lecture
            label = tk.Label(table_frame, text=str(index), borderwidth=1, relief="solid", width=22)
            label.grid(row=row, column=0)
            label = tk.Label(table_frame, text=lecture.subject, borderwidth=1, relief="solid", width=22)
            label.grid(row=row, column=1)
            label = tk.Label(table_frame, text=lecture.section, borderwidth=1, relief="solid", width=22)
            label.grid(row=row, column=2)
            label = tk.Label(table_frame, text=lecture.professor, borderwidth=1, relief="solid", width=22)
            label.grid(row=row, column=3)
            label = tk.Label(table_frame, text=", ".join([f"{day}: {start:02d}:{start_m:02d}-{end:02d}:{end_m:02d}" for day, (start, start_m, end, end_m) in lecture.schedule.items()]), borderwidth=1, relief="solid", width=30)
            label.grid(row=row, column=4)
            row += 1

        self.delete_elective_index_entry = tk.Entry(self.main_frame, width=10)
        self.delete_elective_index_entry.pack(pady=10)

        delete_button = tk.Button(self.main_frame, text="선택 과목 삭제하기", command=self.confirm_delete_elective, font=("Arial", 14))
        delete_button.pack(pady=10)

        back_button = tk.Button(self.main_frame, text="뒤로가기", command=self.create_elective_subject_screen, font=("Arial", 14))
        back_button.pack(pady=20)

    # 선택 과목 삭제 확인 함수
    def confirm_delete_elective(self):
        try:
            index = int(self.delete_elective_index_entry.get())
            if index in self.elective_map:
                lecture = self.elective_map[index]
                self.electives.remove(lecture)
                messagebox.showinfo("성공", "선택 과목이 삭제되었습니다.")
            else:
                messagebox.showerror("오류", "유효하지 않은 인덱스입니다.")
        except ValueError:
            messagebox.showerror("오류", "인덱스는 숫자여야 합니다.")

    # 최종 시간표를 생성하는 함수
    def create_final_timetable(self):
        final_timetable = self.selected_timetable[:]
        conflict_lectures = []
        for elective in self.electives:
            if not any(check_conflict(elective, lecture) for lecture in final_timetable):
                final_timetable.append(elective)
            else:
                conflict_lectures.append(elective)

        self.clear_frame(self.main_frame)

        if conflict_lectures:
            label = tk.Label(self.main_frame, text="시간표 생성에 실패했습니다.", font=("Arial", 18))
            label1 = tk.Label(self.main_frame, text="삭제하면 좋을 과목", font=("Arial", 10))
            label.pack(pady=20)
            label1.pack(padx=10)
            
            table_frame = tk.Frame(self.main_frame)
            table_frame.pack()

            headers = ["강의명", "분반", "교수명", "강의 시간"]
            for i, header in enumerate(headers):
                label = tk.Label(table_frame, text=header, borderwidth=1, relief="solid", width=22)
                label.grid(row=0, column=i)

            for row, lecture in enumerate(recommend_removals(final_timetable, conflict_lectures), start=1):
                label = tk.Label(table_frame, text=lecture.subject, borderwidth=1, relief="solid", width=22)
                label.grid(row=row, column=0)
                label = tk.Label(table_frame, text=lecture.section, borderwidth=1, relief="solid", width=22)
                label.grid(row=row, column=1)
                label = tk.Label(table_frame, text=lecture.professor, borderwidth=1, relief="solid", width=22)
                label.grid(row=row, column=2)
                label = tk.Label(table_frame, text=", ".join([f"{day}: {start:02d}:{start_m:02d}-{end:02d}:{end_m:02d}" for day, (start, start_m, end, end_m) in lecture.schedule.items()]), borderwidth=1, relief="solid", width=30)
                label.grid(row=row, column=3)

            back_button = tk.Button(self.main_frame, text="뒤로가기", command=self.create_elective_subject_screen, font=("Arial", 14))
            back_button.pack(pady=20)

        else:
            sorted_final_timetable = sort_timetable(final_timetable)
            label = tk.Label(self.main_frame, text="최종 시간표", font=("Arial", 18))
            label.pack(pady=20)

            canvas = tk.Canvas(self.main_frame)
            scroll_y = tk.Scrollbar(self.main_frame, orient="vertical", command=canvas.yview)

            table_frame = tk.Frame(canvas)

            headers = ["시간", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
            for i, header in enumerate(headers):
                label = tk.Label(table_frame, text=header, borderwidth=1, relief="solid", width=22)
                label.grid(row=0, column=i)

            timetable_dict = defaultdict(list)
            for lecture in sorted_final_timetable:
                for day, (start_hour, start_minute, end_hour, end_minute) in lecture.schedule.items():
                    time_slot = f"{start_hour:02d}:{start_minute:02d}-{end_hour:02d}:{end_minute:02d}"
                    timetable_dict[time_slot].append((day, lecture))

            row = 1
            for time_slot, lectures in sorted(timetable_dict.items()):
                label = tk.Label(table_frame, text=time_slot, borderwidth=1, relief="solid", width=22)
                label.grid(row=row, column=0)
                for day in headers[1:]:
                    lecture_info = "\n".join([f"{lec.subject} ({lec.section})" for d, lec in lectures if d == day])
                    label = tk.Label(table_frame, text=lecture_info, borderwidth=1, relief="solid", width=22)
                    label.grid(row=row, column=headers.index(day))
                row += 1

            canvas.create_window(0, 0, anchor='nw', window=table_frame)
            canvas.update_idletasks()
            canvas.configure(scrollregion=canvas.bbox('all'), yscrollcommand=scroll_y.set)

            canvas.pack(fill='both', expand=True, side='left')
            scroll_y.pack(fill='y', side='right')

            back_button = tk.Button(self.main_frame, text="뒤로가기", command=self.create_elective_subject_screen, font=("Arial", 14))
            back_button.pack(pady=20)

    # 프레임을 초기화하는 함수
    def clear_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

# 메인 함수
if __name__ == "__main__":
    root = tk.Tk()
    app = TimetableApp(root)
    root.mainloop()

