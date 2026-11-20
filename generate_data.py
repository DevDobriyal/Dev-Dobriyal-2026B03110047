"""Generate student_performance_1000.csv (1,212 rows) with messy data.

Run:  python generate_data.py
Uses only numpy and pandas. Seed 42 makes the file identical every run.
"""

import numpy as np
import pandas as pd

np.random.seed(42)
N = 1200

# --- 1. Clean base data ---------------------------------------------------
df = pd.DataFrame({
    "Student_ID": [f"STU{i:04d}" for i in range(1, N + 1)],
    "Department": np.random.choice(
        ["CSE", "ECE", "Mechanical", "Civil", "Electrical"], N),
    "Attendance_Percent": np.clip(
        np.random.normal(75, 12, N).round(1), 40, 100),
    "Study_Hours_Per_Day": np.clip(
        np.random.normal(3.0, 1.3, N).round(1), 0.5, 7.0),
    "Internet_Access": np.random.choice(["Yes", "No"], N, p=[0.88, 0.12]),
})

# Marks grow with study hours and attendance (plus random noise)
no_net = np.where(df["Internet_Access"] == "No", -3, 0)
for subject, base in [("Python", 40), ("Maths", 37), ("Physics", 39)]:
    marks = (base + 9 * df["Study_Hours_Per_Day"]
             + 0.25 * (df["Attendance_Percent"] - 75)
             + no_net + np.random.normal(0, 12, N))
    df[f"{subject}_Marks"] = np.clip(marks.round(), 0, 100).astype(int)

df["Assignments_Submitted"] = np.clip(
    (1.5 * df["Study_Hours_Per_Day"] + np.random.normal(0, 2, N)).round(),
    0, 10).astype(int)

# A few very low (but valid) marks -> IQR outliers
df.loc[[10, 200, 450, 800], "Python_Marks"] = [2, 6, 9, 11]
df.loc[[30, 600], "Maths_Marks"] = [3, 8]
df.loc[[90, 700, 1000], "Physics_Marks"] = [1, 5, 10]

# --- 2. Total and Result (pass = at least 40 in every subject) ------------
marks_cols = ["Python_Marks", "Maths_Marks", "Physics_Marks"]
df["Total_Marks"] = df[marks_cols].sum(axis=1)
df["Result"] = np.where((df[marks_cols] >= 40).all(axis=1), "Pass", "Fail")

# --- 3. Inject data-quality problems -------------------------------------
missing_rows = np.random.choice(N, 28, replace=False)
df.loc[missing_rows, "Attendance_Percent"] = np.nan          # 28 NaNs

df.loc[[55, 320, 540, 975], "Python_Marks"] = [-5, 108, 112, -12]  # invalid

duplicates = df.sample(12, random_state=42)                  # 12 duplicates
df = pd.concat([df, duplicates]).sort_values(
    "Student_ID", kind="mergesort").reset_index(drop=True)

df.to_csv("student_performance_1000.csv", index=False)
print(f"Saved {len(df)} rows -> student_performance_1000.csv")
