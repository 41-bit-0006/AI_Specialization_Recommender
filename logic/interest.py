def calculate_interest_score(interest, student_marks, interest_profiles):

    profile = interest_profiles[interest]

    total_score = 0
    total_weight = 0

    for subject, interest_weight in profile.items():

        mark = student_marks[subject]

        total_score += mark * interest_weight
        total_weight += interest_weight

    return total_score / total_weight