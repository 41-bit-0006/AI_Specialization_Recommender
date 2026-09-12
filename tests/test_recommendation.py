from logic.scoring import calculate_scores
from logic.recommendation import calculate_final_scores


# Test specialization data
specializations = {
    "Data Science": {
        "programming": 0.25,
        "database": 0.20,
        "networking": 0.05,
        "security": 0.05,
        "mathematics": 0.45
    },

    "Cyber Security": {
        "programming": 0.15,
        "database": 0.05,
        "networking": 0.30,
        "security": 0.40,
        "mathematics": 0.10
    },

    "Networking": {
        "programming": 0.15,
        "database": 0.05,
        "networking": 0.45,
        "security": 0.30,
        "mathematics": 0.05
    },

    "Software Engineering": {
        "programming": 0.40,
        "database": 0.25,
        "networking": 0.05,
        "security": 0.05,
        "mathematics": 0.25
    }
}


interest_profiles = {
    "Data Science": {
        "programming": 1.0,
        "database": 0.8,
        "networking": 0.2,
        "security": 0.2,
        "mathematics": 1.0
    },

    "Cyber Security": {
        "programming": 0.7,
        "database": 0.2,
        "networking": 0.8,
        "security": 1.0,
        "mathematics": 0.4
    },

    "Networking": {
        "programming": 0.5,
        "database": 0.2,
        "networking": 1.0,
        "security": 0.8,
        "mathematics": 0.3
    },

    "Software Engineering": {
        "programming": 1.0,
        "database": 0.7,
        "networking": 0.2,
        "security": 0.2,
        "mathematics": 0.6
    }
}


def test_scoring_returns_all_specializations():

    student_marks = {
        "programming": 80,
        "database": 70,
        "networking": 60,
        "security": 65,
        "mathematics": 85
    }

    scores = calculate_scores(
        student_marks,
        3.5,
        specializations
    )

    assert len(scores) == 4

    assert "Data Science" in scores
    assert "Cyber Security" in scores
    assert "Networking" in scores
    assert "Software Engineering" in scores


def test_scores_are_valid():

    student_marks = {
        "programming": 80,
        "database": 70,
        "networking": 60,
        "security": 65,
        "mathematics": 85
    }

    scores = calculate_scores(
        student_marks,
        3.5,
        specializations
    )

    for score in scores.values():
        assert 0 <= score <= 100


def test_final_scores_are_generated():

    student_marks = {
        "programming": 80,
        "database": 70,
        "networking": 60,
        "security": 65,
        "mathematics": 85
    }

    academic_scores = calculate_scores(
        student_marks,
        3.5,
        specializations
    )

    final_scores = calculate_final_scores(
        academic_scores,
        "Data Science",
        interest_profiles,
        specializations
    )

    assert len(final_scores) == 4

    for result in final_scores.values():
        assert "academic_score" in result
        assert "interest_score" in result
        assert "final_score" in result