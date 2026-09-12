def validate_mark(mark):
    if mark < 0 or mark > 100:
        return False

    return True


def validate_gpa(gpa):
    if gpa < 0 or gpa > 4:
        return False

    return True