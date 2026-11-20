# Student Academic Performance Analytics

Education / EdTech project using **only `pandas` and `numpy`**. It creates a
messy student dataset (1,212 rows), cleans it, and runs 15 analysis tasks.
All results are printed as console tables or saved as CSV. There are no charts.

## Files

| File | What it is |
|---|---|
| `generate_data.py` | Creates `student_performance_1000.csv` |
| `student_performance_analysis.py` | Runs all 15 tasks |
| `at_risk_students.csv` | Students with average marks below 40 (Task 9) |
| `student_performance_cleaned.csv` | Cleaned data with extra columns |
| `run_output.txt` | Console output of one full run |
| `SRS_Document.md` | Requirements document |

## How to run

```bash
pip install pandas numpy
python generate_data.py
python student_performance_analysis.py
```

Run both commands from this folder. The seed is fixed (`np.random.seed(42)`),
so you get the same data every time.

## The data

Columns: `Student_ID`, `Department`, `Attendance_Percent`,
`Study_Hours_Per_Day`, `Python_Marks`, `Maths_Marks`, `Physics_Marks`,
`Assignments_Submitted`, `Internet_Access`, `Total_Marks`, `Result`.

Problems added on purpose so the cleaning steps have work to do:

- 12 duplicate `Student_ID` rows
- 28 missing `Attendance_Percent` values
- 4 invalid `Python_Marks` (-12, -5, 108, 112)
- a few very low valid marks (outliers)

A student **passes** only if all three subjects are at least 40.
The data is synthetic, so the results show the method, not real students.

## What the script does

1. Load and inspect
2. Missing and duplicate audit (duplicates removed, first kept)
3. Fill missing attendance with the department median
4. Check marks are within 0-100 (clip invalid ones)
5. Recalculate `Total_Marks`, add `Average_Marks`
6. Grades with `pd.cut` (F, D, C, B, A)
7. Department summary with `groupby().agg()`
8. Top 10 students
9. At-risk students (average below 40), saved to CSV
10. Attendance bands
11. Study hours vs marks (`np.corrcoef`)
12. Internet access comparison and an `np.where` support flag
13. Median, standard deviation and quartiles of `Python_Marks` (NumPy)
14. IQR outliers
15. Five recommendations

## Main findings (seed 42)

- 1,212 rows became 1,200 after removing duplicates.
- Grades: C is the largest group (39%); F is 2.75% (33 students).
- 33 students are at risk (average below 40).
- Attendance: average marks go from 60.2 (under 60%) to 70.2 (90% and above).
- Study hours: correlation with average marks is 0.83. Under 2 hours a day
  averages 49.8 marks; 5+ hours averages 86.8.
- Internet access: small gap, 64.6 without vs 66.1 with.
- `Python_Marks`: median 67, std 16.9, Q1 56, Q3 79, with 8 low outliers.
- Strong links here come from how the data was generated, and correlation
  does not prove cause.
