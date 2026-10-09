def check_eligibility(course_prerequisites, student_marks, completed_courses=None):
    """Check subject-mark and completed-course prerequisites."""
    completed_courses = set(completed_courses or [])
    failed_requirements = []

    required_courses = course_prerequisites.get("required_courses", [])
    for course in required_courses:
        if course not in completed_courses:
            failed_requirements.append(
                f"Completed course required: {course}"
            )

    mark_requirements = course_prerequisites.get("marks", {})
    for subject, minimum_mark in mark_requirements.items():
        student_mark = student_marks.get(subject, 0)
        if student_mark < minimum_mark:
            failed_requirements.append(
                f"{subject} requires {minimum_mark:.0f}, "
                f"but your mark is {student_mark:.0f}"
            )
 return len(failed_requirements) == 0, failed_requirements

