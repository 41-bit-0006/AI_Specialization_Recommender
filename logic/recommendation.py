def calculate_final_scores(
    academic_scores,
    student_interest,
    interest_profiles,
    specializations,
):
    """Combine academic compatibility and interest alignment."""
    final_scores = {}
    interest_vector = interest_profiles[student_interest]

    for specialization, academic_score in academic_scores.items():
        weights = specializations[specialization]
        alignment = sum(
            interest_vector[subject] * weights[subject]
            for subject in interest_vector
        )
        interest_score = alignment * 100

        final_score = academic_score * 0.80 + interest_score * 0.20

        final_scores[specialization] = {
            "academic_score": academic_score,
            "interest_score": interest_score,
            "final_score": final_score,
        }

    return final_scores


def generate_explanation(specialization, student_marks, specializations):
    """Return the strongest weighted subjects for the recommended path."""
    weights = specializations[specialization]
    top_subjects = sorted(
        weights.items(), key=lambda item: item[1], reverse=True
    )[:3]

    return [
        {
            "subject": subject,
            "mark": student_marks[subject],
            "weight": weight,
            "contribution": student_marks[subject] * weight,
        }
        for subject, weight in top_subjects
    ]
