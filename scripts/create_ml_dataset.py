import pandas as pd
import random
import os

# Create data folder if not exists
os.makedirs("data", exist_ok=True)

students = []

departments = ["SE", "IT", "CS", "DS"]

for i in range(1, 101):
    student_id = f"S{i:03d}"
    name = f"Student_{i}"
    department = random.choice(departments)

    total_classes = 40
    attended_classes = random.randint(15, 40)

    attendance_percentage = round((attended_classes / total_classes) * 100, 2)

    assignment_average = random.randint(35, 95)

    previous_absences = total_classes - attended_classes

    # Risk rule
    if attendance_percentage >= 80:
        risk_level = "Low"
    elif attendance_percentage >= 60:
        risk_level = "Medium"
    else:
        risk_level = "High"

    students.append({
        "Student_ID": student_id,
        "Name": name,
        "Department": department,
        "Total_Classes": total_classes,
        "Attended_Classes": attended_classes,
        "Attendance_Percentage": attendance_percentage,
        "Assignment_Average": assignment_average,
        "Previous_Absences": previous_absences,
        "Risk_Level": risk_level
    })

df = pd.DataFrame(students)

df.to_csv("data/student_attendance_ml.csv", index=False)

print("ML dataset created successfully!")
print(df.head())