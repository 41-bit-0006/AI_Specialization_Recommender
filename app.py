import html
from pathlib import Path

import pandas as pd
import streamlit as st

from logic.eligibility import check_eligibility
from logic.recommendation import calculate_final_scores, generate_explanation
from logic.scoring import calculate_scores
from utils.validation import validate_gpa, validate_mark

BASE_DIR = Path(__file__).resolve().parent

st.set_page_config(
    page_title="AI Specialization Recommender",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# -----------------------------------------------------------------------------
# UI THEME - simple blue/white academic prototype
# -----------------------------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    :root {
        --blue: #1E4E8C;
        --blue-dark: #163A68;
        --blue-light: #EAF3FF;
        --bg: #F7F9FC;
        --text: #172033;
        --muted: #667085;
        --border: #D9E2EC;
        --success: #198754;
    }

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp { background: var(--bg); color: var(--text); }
    .block-container { max-width: 1120px; padding-top: 0.8rem; padding-bottom: 3rem; }

    /* Hide Streamlit chrome that is not part of the student-facing UI. */
    [data-testid="stSidebar"] { display: none; }
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }

    .topbar {
        background: #FFFFFF;
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 0.65rem 1rem;
        margin-bottom: 1.4rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 2px 10px rgba(22,58,104,.04);
    }
    .brand { display:flex; align-items:center; gap:.65rem; font-weight:700; color:var(--text); }
    .brand-icon { width:34px; height:34px; border-radius:9px; background:var(--blue); color:white;
                  display:flex; align-items:center; justify-content:center; font-size:18px; }
    .brand-sub { font-size:.72rem; color:var(--muted); font-weight:500; margin-top:-2px; }

    .eyebrow { color:var(--blue); font-size:.72rem; font-weight:800; letter-spacing:.09em; }
    .hero-title { color:var(--text); font-size:2.55rem; line-height:1.12; font-weight:800; margin:.45rem 0 .8rem; }
    .hero-copy { color:var(--muted); font-size:1rem; line-height:1.65; max-width:620px; }

    .hero-visual {
        background:#FFFFFF; border:1px solid var(--border); border-radius:18px;
        min-height:285px; display:flex; align-items:center; justify-content:center;
        box-shadow:0 8px 24px rgba(22,58,104,.05); position:relative; overflow:hidden;
    }
    .orbit { width:210px; height:210px; border:1px dashed #A9C8EE; border-radius:50%; position:relative; display:flex; align-items:center; justify-content:center; }
    .orbit:before { content:''; position:absolute; width:145px; height:145px; border:1px solid #D5E6FA; border-radius:50%; }
    .core { width:64px; height:64px; border-radius:16px; background:var(--blue); color:white; display:flex; align-items:center; justify-content:center; font-size:25px; box-shadow:0 8px 20px rgba(30,78,140,.25); z-index:2; }
    .node { position:absolute; background:white; border:1px solid var(--border); border-radius:8px; padding:.42rem .58rem; font-size:.68rem; font-weight:600; color:var(--text); box-shadow:0 3px 12px rgba(22,58,104,.07); }
    .node.n1 { top:5px; left:50%; transform:translateX(-50%); }
    .node.n2 { right:-12px; top:50%; transform:translateY(-50%); }
    .node.n3 { bottom:5px; left:50%; transform:translateX(-50%); }
    .node.n4 { left:-24px; top:50%; transform:translateY(-50%); }

    .feature-card, .panel, .score-card, .course-card, .rank-row {
        background:#FFFFFF; border:1px solid var(--border); border-radius:12px;
        box-shadow:0 3px 14px rgba(22,58,104,.04);
    }
    .feature-card { padding:1.15rem; min-height:145px; }
    .icon-box { width:34px; height:34px; border-radius:9px; background:var(--blue-light); color:var(--blue); display:flex; align-items:center; justify-content:center; font-size:17px; margin-bottom:.8rem; }
    .feature-title { font-weight:700; margin-bottom:.3rem; }
    .small-copy { color:var(--muted); font-size:.82rem; line-height:1.55; }

    .page-heading { margin-bottom:1rem; }
    .page-heading h1 { margin:0; font-size:1.9rem; font-weight:800; }
    .page-heading p { margin:.35rem 0 0; color:var(--muted); font-size:.9rem; }
    .section-title { font-size:1.08rem; font-weight:700; margin:1.15rem 0 .5rem; }
    .section-copy { color:var(--muted); font-size:.82rem; margin-bottom:.65rem; }

    .progress-wrap { margin:.8rem 0 1.3rem; }
    .progress-label { display:flex; justify-content:space-between; color:var(--muted); font-size:.74rem; margin-bottom:.35rem; }
    .progress-line { height:6px; background:#E6EDF5; border-radius:999px; overflow:hidden; }
    .progress-fill { height:100%; background:var(--blue); border-radius:999px; }

    .recommendation-card { background:linear-gradient(135deg,#FFFFFF 0%,#F1F7FF 100%); border:1px solid #CFE0F5; border-radius:18px; padding:1.7rem; box-shadow:0 8px 25px rgba(22,58,104,.07); }
    .recommendation-label { color:var(--blue); font-size:.72rem; letter-spacing:.09em; font-weight:800; }
    .recommendation-name { font-size:2rem; font-weight:800; margin:.25rem 0; color:var(--text); }
    .match-number { color:var(--blue); font-size:2.65rem; font-weight:800; line-height:1; }
    .match-caption { color:var(--muted); font-size:.76rem; margin-top:.25rem; }

    .score-card { padding:1rem 1.15rem; }
    .score-name { color:var(--muted); font-size:.75rem; }
    .score-value { color:var(--blue); font-size:1.45rem; font-weight:800; margin-top:.2rem; }

    .insight { background:var(--blue-light); border:1px solid #CFE0F5; border-radius:12px; padding:1rem 1.1rem; color:#27496F; line-height:1.6; font-size:.87rem; }

    .subject-row { background:#FFFFFF; border:1px solid var(--border); border-radius:10px; padding:.8rem .95rem; margin:.5rem 0; }
    .subject-top { display:flex; justify-content:space-between; align-items:center; font-size:.83rem; }
    .subject-name { font-weight:650; }
    .subject-meta { color:var(--muted); font-size:.73rem; }

    .rank-row { padding:.75rem .9rem; margin:.5rem 0; }
    .rank-number { font-weight:800; color:var(--blue); }
    .rank-name { font-weight:650; }
    .rank-score { font-weight:750; text-align:right; }
    .recommended-badge { display:inline-block; background:var(--blue-light); color:var(--blue); border-radius:999px; padding:.18rem .5rem; font-size:.66rem; font-weight:800; margin-left:.4rem; }

    .course-card { padding:1rem 1.05rem; margin:.65rem 0; }
    .course-name { font-size:1rem; font-weight:700; }
    .eligible { color:var(--success); font-size:.78rem; font-weight:650; margin-top:.35rem; }
    .prereq { color:var(--muted); font-size:.76rem; margin-top:.25rem; }

    .empty-state { background:#FFFFFF; border:1px dashed #B9C8D9; border-radius:14px; padding:2rem; text-align:center; }
    .empty-icon { font-size:2rem; }
    .empty-title { font-weight:750; font-size:1rem; margin:.45rem 0; }
    .empty-copy { color:var(--muted); font-size:.82rem; line-height:1.55; }

    .how-step { text-align:center; padding:.8rem; }
    .step-number { width:34px; height:34px; border-radius:50%; background:var(--blue-light); color:var(--blue); display:inline-flex; align-items:center; justify-content:center; font-weight:800; }
    .step-title { font-size:.82rem; font-weight:700; margin-top:.45rem; }

    div[data-testid="stButton"] > button, div[data-testid="stDownloadButton"] > button {
        border-radius:9px; min-height:2.5rem; font-weight:650; border:1px solid var(--border);
    }
    div[data-testid="stButton"] > button[kind="primary"], div[data-testid="stDownloadButton"] > button {
        background:var(--blue); color:white; border-color:var(--blue);
    }
    div[data-testid="stButton"] > button[kind="primary"]:hover, div[data-testid="stDownloadButton"] > button:hover {
        background:var(--blue-dark); border-color:var(--blue-dark);
    }
    div[data-testid="stTextInput"] input, div[data-testid="stNumberInput"] input,
    div[data-baseweb="select"] > div { border-radius:9px !important; }
    .stNumberInput button { display:none; }

    .footer { border-top:1px solid var(--border); margin-top:2.2rem; padding-top:1rem; color:var(--muted); font-size:.72rem; text-align:center; }

    @media (max-width: 800px) {
        .hero-title { font-size:2rem; }
        .block-container { padding-left:1rem; padding-right:1rem; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def load_data():
    specialization_data = pd.read_csv(BASE_DIR / "data" / "specializations.csv")
    interest_data = pd.read_csv(BASE_DIR / "data" / "interests.csv")
    subject_data = pd.read_csv(BASE_DIR / "data" / "subjects.csv")
    degree_data = pd.read_csv(BASE_DIR / "data" / "degree_programs.csv")
    completed_data = pd.read_csv(BASE_DIR / "data" / "completed_courses.csv")
    prerequisite_data = pd.read_csv(BASE_DIR / "data" / "course_prerequisites.csv")
    return specialization_data, interest_data, subject_data, degree_data, completed_data, prerequisite_data


(
    specialization_data,
    interest_data,
    subject_data,
    degree_data,
    completed_data,
    prerequisite_data,
) = load_data()

subjects = subject_data["subject"].tolist()

specializations = {
    row["specialization"]: {subject: float(row[subject]) for subject in subjects}
    for _, row in specialization_data.iterrows()
}

interest_profiles = {
    row["interest"]: {subject: float(row[subject]) for subject in subjects}
    for _, row in interest_data.iterrows()
}

courses = {}
for _, row in prerequisite_data.iterrows():
    course = row["course"]
    if course not in courses:
        courses[course] = {
            "specialization": row["specialization"],
            "required_courses": set(),
            "marks": {},
        }
    courses[course]["required_courses"].add(row["required_course"])
    courses[course]["marks"][row["subject"]] = float(row["minimum_mark"])

for details in courses.values():
    details["required_courses"] = sorted(details["required_courses"])


def run_recommendation(marks, gpa, interest):
    academic_scores = calculate_scores(marks, gpa, specializations)
    final_scores = calculate_final_scores(
        academic_scores, interest, interest_profiles, specializations
    )
    return sorted(final_scores.items(), key=lambda item: item[1]["final_score"], reverse=True)


def get_eligible_courses(path, marks, completed):
    eligible = []
    for course, details in courses.items():
        if details["specialization"] != path:
            continue
        ok, _ = check_eligibility(
            {"required_courses": details["required_courses"], "marks": details["marks"]},
            marks,
            completed,
        )
        if ok and course not in completed:
            eligible.append((course, details))
    return eligible


def go(screen):
    st.session_state["screen"] = screen
    st.rerun()


def render_header():
    screen = st.session_state.get("screen", "home")
    st.markdown(
        """
        <div class="topbar">
            <div class="brand">
                <div class="brand-icon">AI</div>
                <div>
                    <div>AI Specialization Recommender</div>
                    <div class="brand-sub">Academic recommendation prototype</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    c1, c2, c3, c4 = st.columns([1, 1, 1, 1])
    with c1:
        if st.button("Home", use_container_width=True):
            go("home")
    with c2:
        if st.button("How It Works", use_container_width=True):
            go("home")
    with c3:
        if st.button("Recommendation", use_container_width=True, disabled=("result" not in st.session_state)):
            go("result")
    with c4:
        if st.button("Eligible Courses", use_container_width=True, disabled=("result" not in st.session_state)):
            go("courses")


def render_footer():
    st.markdown(
        "<div class='footer'>AI-Based IT Specialization and Course Recommendation System · University academic prototype</div>",
        unsafe_allow_html=True,
    )


def render_home():
    left, right = st.columns([1.12, 0.88], gap="large")
    with left:
        st.markdown("<div class='eyebrow'>AI-BASED ACADEMIC RECOMMENDATION</div>", unsafe_allow_html=True)
        st.markdown("<div class='hero-title'>Find the IT Specialization<br>That Suits You</div>", unsafe_allow_html=True)
        st.markdown(
            "<div class='hero-copy'>Analyze your academic performance, GPA, completed courses and field of interest to discover a suitable IT specialization.</div>",
            unsafe_allow_html=True,
        )
        st.write("")
        if st.button("Start My Recommendation  →", type="primary", use_container_width=False):
            go("input")
    with right:
        st.markdown(
            """
            <div class="hero-visual">
                <div class="orbit">
                    <div class="core">AI</div>
                    <div class="node n1">GPA</div>
                    <div class="node n2">Interest</div>
                    <div class="node n3">Specialization</div>
                    <div class="node n4">Marks</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("### What the system considers")
    cols = st.columns(3, gap="medium")
    features = [
        ("📊", "Academic Performance", "Uses your subject marks and GPA to calculate academic suitability."),
        ("🎯", "Interest Matching", "Considers your selected field of interest when ranking specializations."),
        ("📚", "Course Eligibility", "Checks course prerequisites and shows courses you are eligible for."),
    ]
    for col, (icon, title, copy) in zip(cols, features):
        with col:
            st.markdown(
                f"<div class='feature-card'><div class='icon-box'>{icon}</div><div class='feature-title'>{title}</div><div class='small-copy'>{copy}</div></div>",
                unsafe_allow_html=True,
            )

    st.markdown("### How It Works")
    cols = st.columns(4)
    steps = ["Enter Your Information", "Analyze Performance", "Match Your Interest", "Get Recommendation"]
    for i, (col, step) in enumerate(zip(cols, steps), 1):
        with col:
            st.markdown(
                f"<div class='how-step'><div class='step-number'>{i}</div><div class='step-title'>{step}</div></div>",
                unsafe_allow_html=True,
            )


def render_input():
    st.markdown(
        """
        <div class="page-heading">
            <h1>Enter Your Academic Information</h1>
            <p>Provide your academic performance and interests to generate a specialization recommendation.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.progress(0.5, text="Step 1 of 2  ·  Your Information")

    st.markdown("<div class='section-title'>Academic Information</div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        degree_program = st.selectbox("Degree Program", degree_data["degree_program"].astype(str).tolist())
    with c2:
        stage = st.selectbox(
            "Current Study Stage",
            ["First Year - Second Semester", "Second Year", "Third Year", "Final Year"],
        )

    st.markdown("<div class='section-title'>Academic Performance</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-copy'>Enter your average marks for each subject.</div>", unsafe_allow_html=True)
    student_marks = {}
    cols = st.columns(2, gap="medium")
    for i, row in subject_data.iterrows():
        subject = row["subject"]
        display = row["display_name"]
        with cols[i % 2]:
            student_marks[subject] = st.number_input(
                display,
                min_value=0,
                max_value=100,
                value=0,
                step=1,
                key=f"ui_mark_{subject}",
                help=f"Enter your {display} mark from 0 to 100.",
            )

    st.markdown("<div class='section-title'>Overall GPA</div>", unsafe_allow_html=True)
    gpa = st.number_input(
        "Current Overall GPA",
        min_value=0.0,
        max_value=4.0,
        value=0.0,
        step=0.1,
        help="Enter your latest/current overall GPA from 0.0 to 4.0.",
    )

    st.markdown("<div class='section-title'>Completed Courses</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-copy'>Select the foundation courses you have already completed.</div>", unsafe_allow_html=True)
    completed_courses = st.multiselect(
        "Completed Courses",
        completed_data["course"].astype(str).tolist(),
    )

    st.markdown("<div class='section-title'>Field of Interest</div>", unsafe_allow_html=True)
    interest = st.selectbox("Field of Interest", list(interest_profiles.keys()))

    st.write("")
    if st.button("Get My Recommendation  →", type="primary", use_container_width=True):
        if not all(validate_mark(mark) for mark in student_marks.values()):
            st.error("Please enter valid marks between 0 and 100.")
            return
        if not validate_gpa(gpa):
            st.error("Please enter a GPA between 0.0 and 4.0.")
            return

        st.session_state["result"] = {
            "degree": degree_program,
            "stage": stage,
            "marks": student_marks.copy(),
            "gpa": gpa,
            "completed": completed_courses.copy(),
            "interest": interest,
            "ranked": run_recommendation(student_marks, gpa, interest),
        }
        st.session_state["screen"] = "result"
        st.rerun()


def render_result():
    result = st.session_state["result"]
    ranked = result["ranked"]
    marks = result["marks"]
    degree = result["degree"]
    stage = result["stage"]
    interest = result["interest"]
    best_path, best = ranked[0]

    st.markdown(
        """
        <div class="page-heading">
            <h1>Your AI Recommendation</h1>
            <p>Based on your academic performance and selected field of interest.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.progress(1.0, text="Step 2 of 2  ·  Recommendation")

    st.markdown(
        f"""
        <div class='recommendation-card'>
            <div class='recommendation-label'>YOUR AI RECOMMENDATION</div>
            <div class='recommendation-name'>{html.escape(best_path)}</div>
            <div class='match-number'>{best['final_score']:.1f}%</div>
            <div class='match-caption'>Match Score · This is a compatibility score, not a probability.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")
    c1, c2, c3 = st.columns(3)
    metrics = [
        ("Overall Match", best["final_score"]),
        ("Academic Fit", best["academic_score"]),
        ("Interest Alignment", best["interest_score"]),
    ]
    for col, (name, value) in zip((c1, c2, c3), metrics):
        with col:
            st.markdown(
                f"<div class='score-card'><div class='score-name'>{name}</div><div class='score-value'>{value:.1f}%</div></div>",
                unsafe_allow_html=True,
            )

    st.markdown("### Why We Recommended This")
    st.markdown(
        f"<div class='insight'>For <strong>{html.escape(degree)}</strong> at <strong>{html.escape(stage)}</strong>, the system considered your subject performance, GPA, and interest in <strong>{html.escape(interest)}</strong>. The highest final score is <strong>{html.escape(best_path)}</strong>.</div>",
        unsafe_allow_html=True,
    )

    st.markdown("### Top Contributing Subjects")
    for item in generate_explanation(best_path, marks, specializations):
        subject_name = item["subject"].replace("_", " ").title()
        mark = item["mark"]
        weight = item["weight"] * 100
        contribution = item["contribution"]
        st.markdown(
            f"""
            <div class='subject-row'>
                <div class='subject-top'><span class='subject-name'>{html.escape(subject_name)}</span><span class='subject-meta'>{mark:.0f}/100 · Weight {weight:.0f}% · Contribution {contribution:.1f}</span></div>
                <div class='progress-wrap'><div class='progress-line'><div class='progress-fill' style='width:{min(max(mark,0),100):.0f}%'></div></div></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("### Specialization Ranking")
    for index, (name, values) in enumerate(ranked, 1):
        badge = "<span class='recommended-badge'>RECOMMENDED</span>" if index == 1 else ""
        st.markdown(
            f"""
            <div class='rank-row'>
                <div class='subject-top'>
                    <span><span class='rank-number'>{index}</span>&nbsp;&nbsp;<span class='rank-name'>{html.escape(name)}</span>{badge}</span>
                    <span class='rank-score'>{values['final_score']:.1f}%</span>
                </div>
                <div class='progress-wrap'><div class='progress-line'><div class='progress-fill' style='width:{min(max(values['final_score'],0),100):.0f}%'></div></div></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.write("")
    if st.button("View Eligible Courses  →", type="primary", use_container_width=True):
        go("courses")


def render_courses():
    result = st.session_state["result"]
    ranked = result["ranked"]
    marks = result["marks"]
    completed = result["completed"]
    best_path = ranked[0][0]
    eligible = get_eligible_courses(best_path, marks, completed)

    st.markdown(
        f"""
        <div class="page-heading">
            <h1>Eligible Courses</h1>
            <p>Courses you are currently eligible to take in your recommended specialization: <strong>{html.escape(best_path)}</strong>.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if eligible:
        for course, details in eligible:
            mark_text = " · ".join(
                f"{subject.replace('_', ' ').title()} ≥ {minimum:.0f}"
                for subject, minimum in details["marks"].items()
            )
            st.markdown(
                f"""
                <div class='course-card'>
                    <div class='course-name'>{html.escape(course)}</div>
                    <div class='eligible'>✓ Prerequisites satisfied</div>
                    <div class='prereq'>{html.escape(mark_text)}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
    else:
        st.markdown(
            """
            <div class='empty-state'>
                <div class='empty-icon'>📚</div>
                <div class='empty-title'>No Eligible Courses</div>
                <div class='empty-copy'>No courses are currently eligible based on your completed courses and prerequisite marks.<br>Complete the required prerequisites to become eligible for additional courses.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("### Save Your Recommendation")
    st.markdown(
        "<div class='section-copy'>Keep a copy of your specialization recommendation and course eligibility result.</div>",
        unsafe_allow_html=True,
    )

    output = pd.DataFrame(
        {
            "Degree Program": [result["degree"]],
            "Study Stage": [result["stage"]],
            "Recommended Specialization": [best_path],
            "Match Score (%)": [round(ranked[0][1]["final_score"], 2)],
            "Academic Score (%)": [round(ranked[0][1]["academic_score"], 2)],
            "Interest Alignment (%)": [round(ranked[0][1]["interest_score"], 2)],
            "GPA": [result["gpa"]],
            "Area of Interest": [result["interest"]],
            "Eligible Courses": [", ".join(course for course, _ in eligible) if eligible else "None"],
            "Completed Courses": [", ".join(completed) if completed else "None"],
            **{name.title(): [mark] for name, mark in marks.items()},
        }
    )

    c1, c2 = st.columns(2)
    with c1:
        st.download_button(
            "↓ Download Recommendation",
            output.to_csv(index=False),
            "specialization_recommendation.csv",
            "text/csv",
            use_container_width=True,
        )
    with c2:
        if st.button("↻ Start a New Recommendation", use_container_width=True):
            st.session_state.pop("result", None)
            for key in list(st.session_state.keys()):
                if key.startswith("ui_mark_"):
                    st.session_state.pop(key, None)
            go("input")


if "screen" not in st.session_state:
    st.session_state["screen"] = "home"

render_header()

if st.session_state["screen"] == "home":
    render_home()
elif st.session_state["screen"] == "input":
    render_input()
elif st.session_state["screen"] == "result":
    if "result" not in st.session_state:
        go("input")
    render_result()
elif st.session_state["screen"] == "courses":
    if "result" not in st.session_state:
        go("input")
    render_courses()

render_footer()
