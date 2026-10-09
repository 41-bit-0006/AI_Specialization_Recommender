import pandas as pd
from pathlib import Path

from logic.scoring import calculate_scores
from logic.recommendation import calculate_final_scores

ROOT = Path(__file__).resolve().parents[1]

specialization_data = pd.read_csv(
    ROOT / "data" / "specializations.csv"
)

interest_data = pd.read_csv(
    ROOT / "data" / "interests.csv"
)

evaluation_data = pd.read_csv(
    ROOT / "data" / "evaluation_students.csv"
)

specializations = {}

for _, row in specialization_data.iterrows():

    specializations[row["specialization"]] = {
        "programming": row["programming"],
        "database": row["database"],
        "networking": row["networking"],
        "security": row["security"],
        "mathematics": row["mathematics"]
    }

interest_profiles = {}

for _, row in interest_data.iterrows():

    interest_profiles[row["interest"]] = {
        "programming": row["programming"],
        "database": row["database"],
        "networking": row["networking"],
        "security": row["security"],
        "mathematics": row["mathematics"]
    }

def test_evaluation_dataset():

    correct = 0
    total = len(evaluation_data)

    for _, student in evaluation_data.iterrows():

        student_marks = {
            "programming": student["programming"],
            "database": student["database"],
            "networking": student["networking"],
            "security": student["security"],
            "mathematics": student["mathematics"]
        }

        academic_scores = calculate_scores(
            student_marks,
            student["gpa"],
            specializations
        )

        final_scores = calculate_final_scores(
            academic_scores,
            student["interest"],
            interest_profiles,
            specializations
        )

        recommended = max(
            final_scores,
            key=lambda specialization:
            final_scores[specialization]["final_score"]
        )

        if recommended == student["expected_specialization"]:
            correct += 1

    accuracy = correct / total

    print(
        f"\nEvaluation Accuracy: "
        f"{accuracy * 100:.2f}%"
    )

    print(
        f"Correct Recommendations: "
        f"{correct}/{total}"
    )

    assert total > 0
