# ================================================================
# EDUTEXT SUBJECT REGISTRY
# ================================================================

from mathematics import get_mathematics
from computer_science import get_computer_science


def get_subjects():
    """
    Returns all available subjects.
    """

    mathematics = get_mathematics()
    computer_science = get_computer_science()

    return {
        "1": computer_science,
        "2": mathematics
    }


SUBJECTS = get_subjects()


def get_subject(subject_key):
    """
    Return one subject using its key.
    """

    return SUBJECTS.get(str(subject_key))


def get_all_subjects():
    """
    Return all registered subjects.
    """

    return SUBJECTS


def get_subject_questions(subject_key):
    """
    Return questions belonging to a subject.
    """

    subject = get_subject(subject_key)

    if subject is None:
        return []

    return subject["questions"]
