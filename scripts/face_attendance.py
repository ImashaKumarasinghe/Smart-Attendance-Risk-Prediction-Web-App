import cv2
import os
import pandas as pd
from datetime import datetime

# Input and output folders
image_folder = "images"
output_file = "data/attendance_raw.csv"

# Create required folders if they do not exist
os.makedirs("data", exist_ok=True)
os.makedirs("output", exist_ok=True)

# Load OpenCV face detection model
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

attendance_data = []

# Read all images from images folder
for filename in os.listdir(image_folder):

    if filename.endswith(".jpg") or filename.endswith(".png"):

        image_path = os.path.join(image_folder, filename)

        # Read image
        image = cv2.imread(image_path)

        if image is None:
            print(f"Could not read image: {filename}")
            continue

        # Convert image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Detect faces
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5
        )

        student_name = filename.split(".")[0]

        # Draw rectangle around detected faces
        for (x, y, w, h) in faces:
            cv2.rectangle(
                image,
                (x, y),
                (x + w, y + h),
                (0, 255, 0),
                2
            )

        # Mark attendance
        if len(faces) > 0:
            status = "Present"
            face_detected = 1
        else:
            status = "Absent"
            face_detected = 0

        # Save detected image to output folder
        cv2.imwrite(f"output/detected_{filename}", image)

        # Add attendance record
        attendance_data.append({
            "Student_ID": student_name.upper(),
            "Name": student_name,
            "Date": datetime.now().strftime("%Y-%m-%d"),
            "Time": datetime.now().strftime("%H:%M:%S"),
            "Face_Detected": face_detected,
            "Status": status
        })

# Convert to table
df = pd.DataFrame(attendance_data)

# Save CSV
df.to_csv(output_file, index=False)

print("Attendance saved successfully!")
print(df)