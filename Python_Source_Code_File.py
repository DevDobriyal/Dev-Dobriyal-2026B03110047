"""Student Academic Performance Analytics - all 15 tasks.

Run (after generate_data.py):  python student_performance_analysis.py
Uses only pandas and numpy. Prints tables and saves CSV files.
"""

import numpy as np
import pandas as pd

pd.set_option("display.width", 130)
pd.set_option("display.max_columns", 20)
pd.set_option("display.float_format", "{:.2f}".format)

SUBJECTS = ["Python_Marks", "Maths_Marks", "Physics_Marks"]


def task1_load(path):
    print("\n=== TASK 1: Load and Inspect ===")
    df = pd.read_csv(path)
    print("Shape:", df.shape)
    print("Columns:", list(df.columns))
    print(df.dtypes)
    print(df.head())
    print(df.describe())
    return df


def task2_missing_duplicates(df):
    print("\n=== TASK 2: Missing & Duplicate Audit ===")
    print("Missing values per column:")
    print(df.isna().sum())
    dups = df[df.duplicated("Student_ID", keep=False)]
    print("\nRows with a repeated Student_ID:", len(dups))
    print(dups.head(6))
    before = len(df)
    df = df.drop_duplicates("Student_ID", keep="first")
    print(f"Removed duplicates: {before} -> {len(df)} rows")
    return df


def task3_fill_attendance(df):
    print("\n=== TASK 3: Handle Missing Attendance ===")
    print("Missing before:", df["Attendance_Percent"].isna().sum())
    dept_median = df.groupby("Department")["Attendance_Percent"].transform(
        "median")
    df["Attendance_Percent"] = df["Attendance_Percent"].fillna(dept_median)
    print("Missing after:", df["Attendance_Percent"].isna().sum())
    print("Why department median? It is not affected by extreme values like "
          "the mean is,\nit keeps each student's cohort in mind, and "
          "dropping rows would throw away valid marks.")
    return df


def task4_check_scores(df):
    print("\n=== TASK 4: Score Range Validation (0-100) ===")
    for col in SUBJECTS:
        bad = df[(df[col] < 0) | (df[col] > 100)]
        print(f"{col}: {len(bad)} invalid values")
        if len(bad) > 0:
            print(bad[["Student_ID", col]])
    df[SUBJECTS] = df[SUBJECTS].clip(0, 100)
    print("Fixed by clipping all marks to the range 0-100.")
    return df


def task5_totals(df):
    print("\n=== TASK 5: Total & Average Marks ===")
    df["Total_Marks"] = df[SUBJECTS].sum(axis=1)
    df["Average_Marks"] = df["Total_Marks"] / 3
    # Pass = at least 40 in every subject. Pass_Rate is 100 or 0, so the
    # mean of this column is the pass percentage.
    df["Result"] = np.where((df[SUBJECTS] >= 40).all(axis=1), "Pass", "Fail")
    df["Pass_Rate"] = np.where(df["Result"] == "Pass", 100, 0)
    print(df[["Student_ID"] + SUBJECTS + ["Total_Marks", "Average_Marks",
                                          "Result"]].head())
    return df


def task6_grades(df):
    print("\n=== TASK 6: Grade Classification ===")
    df["Grade"] = pd.cut(df["Average_Marks"],
                         bins=[0, 40, 55, 70, 85, 100.01],
                         labels=["F", "D", "C", "B", "A"], right=False)
    counts = df["Grade"].value_counts().sort_index(ascending=False)
    print(pd.DataFrame({"Count": counts,
                        "Percent": counts / len(df) * 100}))
    return df


def task7_departments(df):
    print("\n=== TASK 7: Department-Wise Performance ===")
    summary = df.groupby("Department").agg(
        Students=("Student_ID", "count"),
        Avg_Marks=("Average_Marks", "mean"),
        Pass_Rate=("Pass_Rate", "mean"),
        Avg_Attendance=("Attendance_Percent", "mean"),
    )
    print(summary.sort_values("Avg_Marks", ascending=False))


def task8_top10(df):
    print("\n=== TASK 8: Top 10 Performers ===")
    top = df.sort_values("Average_Marks", ascending=False).head(10)
    print(top[["Student_ID", "Department"] + SUBJECTS
              + ["Average_Marks", "Grade"]].to_string(index=False))


def task9_at_risk(df):
    print("\n=== TASK 9: At-Risk Students (Average < 40) ===")
    at_risk = df[df["Average_Marks"] < 40].sort_values("Average_Marks")
    print("At-risk students:", len(at_risk))
    print(at_risk[["Student_ID", "Department", "Average_Marks",
                   "Attendance_Percent", "Study_Hours_Per_Day"]].head(10))
    at_risk.to_csv("at_risk_students.csv", index=False)
    print("Saved all of them to at_risk_students.csv")
    return at_risk


def task10_attendance(df):
    print("\n=== TASK 10: Attendance Band Comparison ===")
    df["Attendance_Band"] = pd.cut(
        df["Attendance_Percent"], bins=[0, 60, 75, 90, 100.01],
        labels=["Low (<60)", "Moderate (60-74)", "Good (75-89)",
                "Excellent (90-100)"], right=False)
    print(df.groupby("Attendance_Band", observed=True).agg(
        Students=("Student_ID", "count"),
        Avg_Marks=("Average_Marks", "mean"),
        Pass_Rate=("Pass_Rate", "mean")))
    return df


def task11_study_hours(df):
    print("\n=== TASK 11: Study Hours vs Marks ===")
    df["Study_Bracket"] = pd.cut(
        df["Study_Hours_Per_Day"], bins=[0, 2, 3, 4, 5, 10],
        labels=["<2h", "2-3h", "3-4h", "4-5h", "5h+"], right=False)
    print(df.groupby("Study_Bracket", observed=True).agg(
        Students=("Student_ID", "count"),
        Avg_Marks=("Average_Marks", "mean")))
    r = np.corrcoef(df["Study_Hours_Per_Day"], df["Average_Marks"])[0, 1]
    print(f"\nPearson correlation (np.corrcoef): {r:.3f}")
    return df, r


def task12_internet(df):
    print("\n=== TASK 12: Internet Access Impact ===")
    print(df.groupby("Internet_Access").agg(
        Students=("Student_ID", "count"),
        Avg_Marks=("Average_Marks", "mean"),
        Pass_Rate=("Pass_Rate", "mean"),
        Avg_Study_Hours=("Study_Hours_Per_Day", "mean")))
    df["Support_Flag"] = np.where(
        (df["Internet_Access"] == "No") & (df["Average_Marks"] < 55),
        "Needs Support", "OK")
    print("\nSupport_Flag counts:")
    print(df["Support_Flag"].value_counts())
    return df


def task13_python_stats(df):
    print("\n=== TASK 13: NumPy Stats on Python_Marks ===")
    x = df["Python_Marks"].to_numpy()
    q1, q2, q3 = np.percentile(x, [25, 50, 75])
    print("Median:", np.median(x))
    print("Std dev:", round(np.std(x), 2))
    print(f"Q1: {q1}  Q2: {q2}  Q3: {q3}")


def task14_outliers(df):
    print("\n=== TASK 14: Outliers using IQR ===")
    for col in SUBJECTS:
        x = df[col].to_numpy()
        q1, q3 = np.percentile(x, [25, 75])
        iqr = q3 - q1
        low, high = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        n_low, n_high = (x < low).sum(), (x > high).sum()
        print(f"{col}: IQR={iqr:.1f}, fences=({low:.1f}, {high:.1f}), "
              f"low outliers={n_low}, high outliers={n_high}")
    x = df["Python_Marks"].to_numpy()
    q1, q3 = np.percentile(x, [25, 75])
    low = q1 - 1.5 * (q3 - q1)
    print("\nLowest Python_Marks outliers:")
    print(df[df["Python_Marks"] < low].sort_values("Python_Marks")
          [["Student_ID", "Department", "Python_Marks"]].head(10))


def task15_recommendations(df, at_risk, r):
    print("\n=== TASK 15: Recommendations ===")
    low_att = df[df["Attendance_Percent"] < 60]["Average_Marks"].mean()
    high_att = df[df["Attendance_Percent"] >= 90]["Average_Marks"].mean()
    low_study = df[df["Study_Hours_Per_Day"] < 2]["Average_Marks"].mean()
    high_study = df[df["Study_Hours_Per_Day"] >= 5]["Average_Marks"].mean()
    net = df.groupby("Internet_Access")["Average_Marks"].mean()
    weakest = df[SUBJECTS].mean().idxmin()

    print(f"1. Give extra help to the {len(at_risk)} at-risk students "
          f"(average below 40).")
    print(f"2. Warn students when attendance falls below 60%: they average "
          f"{low_att:.1f} marks vs {high_att:.1f} at 90%+.")
    print(f"3. Teach study habits: under 2 h/day averages {low_study:.1f} vs "
          f"{high_study:.1f} for 5+ h (r = {r:.2f}).")
    print(f"4. Support students without internet: {net['No']:.1f} average "
          f"marks vs {net['Yes']:.1f} with internet.")
    print(f"5. Add tutoring for {weakest}, the lowest-scoring subject.")


def main():
    df = task1_load("student_performance_1000.csv")
    df = task2_missing_duplicates(df)
    df = task3_fill_attendance(df)
    df = task4_check_scores(df)
    df = task5_totals(df)
    df = task6_grades(df)
    task7_departments(df)
    task8_top10(df)
    at_risk = task9_at_risk(df)
    df = task10_attendance(df)
    df, r = task11_study_hours(df)
    df = task12_internet(df)
    task13_python_stats(df)
    task14_outliers(df)
    task15_recommendations(df, at_risk, r)
    df.to_csv("student_performance_cleaned.csv", index=False)
    print("\nDone. Cleaned data saved to student_performance_cleaned.csv")


if __name__ == "__main__":
    main()
