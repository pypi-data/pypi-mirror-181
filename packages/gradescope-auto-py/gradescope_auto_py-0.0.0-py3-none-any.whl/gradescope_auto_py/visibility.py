from enum import StrEnum, auto


class Visibility(StrEnum):
    """ controls visibility of a test case

    https://gradescope-autograders.readthedocs.io/en/latest/specs/#controlling-test-case-visibility

    visible (default): test case will always be shown
    hidden: test case will never be shown to students
    after_due_date: test case will be shown after the assignment's due date has passed. If late submission is allowed, then test will be shown only after the late due date.
    after_published: test case will be shown only when the assignment is explicitly published from the "Review Grades" page
    """
    VISIBLE = auto()
    HIDDEN = auto()
    AFTER_DUE_DATE = auto()
    AFTER_PUBLISHED = auto()
