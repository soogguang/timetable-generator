# Timetable Generator

This project is a **GUI-based timetable generation program** that automatically creates all possible valid course schedules based on selected subjects.

Users can input mandatory and elective courses they are interested in, and the program generates **conflict-free timetable combinations** by checking lecture times, sections, and constraints.

The application is implemented in **Python using Tkinter**, providing an interactive interface for course selection and timetable visualization.

---

## Features

- Select **mandatory and elective subjects**
- Support for **multiple lectures and sections per subject**
- Automatic **time conflict detection**
- Generation of all possible **valid timetable combinations**
- Interactive **GUI-based workflow**
- Scrollable timetable display for large result sets

---

## How It Works

1. Each subject contains one or more lectures with:
   - Subject name  
   - Professor  
   - Weekly schedule (day and time)  
   - Section information (if applicable)

2. The program generates all possible lecture combinations using a Cartesian product.

3. Each combination is filtered by:
   - **Time conflict detection**
   - **Section consistency per subject**

4. Only valid, non-conflicting timetables are displayed to the user.

---

## Technologies Used

- Python 3
- Tkinter (GUI)
- itertools (combinatorial generation)
- Object-Oriented Programming (OOP)

---

## Use Case

This program is useful for students who:
- Have multiple course options per subject
- Want to explore all feasible timetable combinations
- Need to avoid overlapping class times automatically

---

## Notes

- The number of generated timetables increases rapidly with more subjects.
- For best performance, limit the number of selectable lectures per subject.
