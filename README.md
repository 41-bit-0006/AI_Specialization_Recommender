# AI-Based IT Specialization and Course Recommendation System

A simple university-level Streamlit prototype that recommends an IT specialization using weighted academic scoring and interest alignment, then checks rule-based course eligibility.

## Final UI

The UI is intentionally simple and viva-friendly rather than an industry-style SaaS dashboard. It uses a blue-and-white academic theme and four main screens:

1. Home / Welcome
2. Student Information
3. Recommendation Result
4. Eligible Courses + Save Result

The existing system inputs and workflow are preserved. The visual layer was redesigned with custom Streamlit CSS.

## Inputs

- Degree Program
- Current Study Stage
- Programming mark (0-100)
- Database mark (0-100)
- Networking mark (0-100)
- Security mark (0-100)
- Mathematics mark (0-100)
- Current overall GPA (0.0-4.0)
- Completed Courses
- Field of Interest

## System flow

Student Data Input -> Data Validation -> Rule-Based Eligibility Check -> Weighted Scoring -> Interest-Based Adjustment -> Ranked Recommendation -> Eligible Courses

## Important prototype note

The weighting values and course prerequisite rows in the CSV files are prototype/configurable data. They should be validated against the official curriculum before being described as official KDU rules.

## Run on Windows

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

Open `http://localhost:8501` if the browser does not open automatically.

## Tests

The `tests` folder is retained for academic verification and is not exposed as a user-facing feature.
