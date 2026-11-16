"""Late fees."""

from datetime import date

from lendlite.config import LATE_FEE_PER_DAY_CENTS
from lendlite.loans import due_date


def calculate_late_fee(loan, today: date) -> int:
    """Return the late fee for each day the book is overdue, in cents.

    The days are counted from the due date up to the return date, or up to the
    given date while the book is still out. A book that is not late costs nothing.
    """
    end = loan.returned_on or today
    days_late = (end - due_date(loan)).days
    return max(days_late, 0) * LATE_FEE_PER_DAY_CENTS
