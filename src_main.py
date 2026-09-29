import json
import os
from calculator import AttendanceEngine, GradeEngine

DATA_FILE = "courses.json"


def load_courses():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}


def save_courses(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


def handle_attendance(data):
    code = input("Enter Course Code (e.g., CSE1001): ").strip().upper()
    try:
        attended = int(input("Enter attended classes: "))
        total = int(input("Enter total classes: "))
        target = float(input("Enter target attendance % [default 75]: ") or 75)

        res = AttendanceEngine.calculate_status(attended, total, target)
        print(f"\nCurrent Attendance: {res['current_pct']}%")
        print(f"Status: {res['status']}")
        print(res['message'])

        if input("Save/Update course data? (y/n): ").strip().lower() == "y":
            data[code] = {"attended": attended, "total": total}
            save_courses(data)
            print(f"Saved {code} successfully!")
    except ValueError as e:
        print(f"Error: {e}")


def handle_grades():
    try:
        cat1 = float(input("CAT 1 Score (out of 50): "))
        cat2 = float(input("CAT 2 Score (out of 50): "))
        da = float(input("DA/Quiz Total Score (out of 30): "))

        internal = GradeEngine.calculate_internal_score(cat1, cat2, da)
        print(f"\nCalculated Internal Score: {internal:.2f} / 60")

        reqs = GradeEngine.get_fat_requirements(internal)
        print("\nFAT Marks Required (out of 100):")
        print("-" * 35)
        for grade, req in reqs.items():
            val = req["fat_required"] if req["fat_required"] is not None else "N/A"
            print(f"Grade {grade}: {val:<5} ({req['status']})")
        print("-" * 35)
    except ValueError as e:
        print(f"Error: {e}")


def main():
    data = load_courses()
    while True:
        print("\n==================================")
        print("  VTOP ATTENDANCE & GRADE PREDICTOR ")
        print("==================================")
        print("1. Calculate Attendance Safety")
        print("2. Estimate Grade Requirements")
        print("3. View Saved Courses")
        print("4. Exit")

        choice = input("\nSelect (1-4): ").strip()
        if choice == "1":
            handle_attendance(data)
        elif choice == "2":
            handle_grades()
        elif choice == "3":
            print("\nSaved Courses:", data if data else "No data stored.")
        elif choice == "4":
            print("Exiting...")
            break


if __name__ == "__main__":
    main()