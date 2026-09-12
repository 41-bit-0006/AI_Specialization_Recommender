import pandas as pd

from logic.scoring import calculate_scores
from logic.recommendation import calculate_final_scores


def evaluate_system(
    evaluation_file,
    specializations,
    interest_profiles
):

    evaluation_data = pd.read_csv(evaluation_file)

    results = []

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

        results.append({
            "Student": student["student_name"],
            "Expected": student["expected_specialization"],
            "Recommended": recommended,
            "Correct": (
                recommended ==
                student["expected_specialization"]
            )
        })

    return pd.DataFrame(results)