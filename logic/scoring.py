def calculate_scores(student_marks, gpa, specializations):
    """Calculate academic compatibility for every specialization."""
    scores = {}
    gpa_percentage = (gpa / 4) * 100

    for specialization, weights in specializations.items():
        subject_score = sum(
            student_marks[subject] * weight
            for subject, weight in weights.items()
        )

        # Prototype academic model: 90% weighted subject performance,
        # 10% latest/overall GPA converted to a 0-100 scale.
        scores[specialization] = (
            subject_score * 0.90 + gpa_percentage * 0.10
        )

    return scores
