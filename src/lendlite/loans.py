"""Borrowing, returning and renewing books."""

from datetime import date, timedelta

from lendlite import store
from lendlite.config import (
    LOAN_PERIOD_DAYS,
    MAX_BOOKS_PER_MEMBER,
    MAX_RENEWALS,
    RENEWAL_EXTENSION_DAYS,
)
from lendlite.models import Loan


def due_date(loan: Loan) -> date:
    """Work out the day a loan must be back: the loan period after the borrow date,
    plus the extra days that each renewal added."""
    extra = loan.renewals * RENEWAL_EXTENSION_DAYS
    return loan.borrowed_on + timedelta(days=LOAN_PERIOD_DAYS + extra)


def is_overdue(loan: Loan, today: date) -> bool:
    """Say whether a loan that is still open has gone past its due date."""
    return loan.returned_on is None and today > due_date(loan)


def _open_loans(member_id: str) -> list[Loan]:
    return [x for x in store.loans_for_member(member_id) if x.returned_on is None]


def borrow_book(member_id: str, book_id: str, today: date) -> Loan:
    """Lend a book to a member. It fails if the member or book is unknown, if the
    book is already out, or if the member already has the most books allowed."""
    book = store.get_book(book_id)
    if store.get_member(member_id) is None or book is None:
        raise ValueError("unknown member or book")
    if not book.available:
        raise ValueError("book is not available")
    if len(_open_loans(member_id)) >= MAX_BOOKS_PER_MEMBER:
        raise ValueError("member has reached the borrowing limit")
    book.available = False
    loan = Loan(store.new_id("L"), member_id, book_id, today)
    return store.save_loan(loan)


def return_book(loan_id: str, today: date) -> Loan:
    """Take a book back. The loan is closed with the given date and the book can
    be borrowed again."""
    loan = store.get_loan(loan_id)
    if loan is None:
        raise ValueError("unknown loan")
    if loan.returned_on is not None:
        raise ValueError("loan is already closed")
    loan.returned_on = today
    book = store.get_book(loan.book_id)
    if book is not None:
        book.available = True
    return store.save_loan(loan)


def renew_loan(loan_id: str, today: date) -> Loan:
    """Give a loan more time. It fails if the loan is closed, if it is overdue, or
    if it has already been renewed the most times allowed."""
    loan = store.get_loan(loan_id)
    if loan is None:
        raise ValueError("unknown loan")
    if loan.returned_on is not None:
        raise ValueError("loan is already closed")
    if is_overdue(loan, today):
        raise ValueError("an overdue loan cannot be renewed")
    if loan.renewals >= MAX_RENEWALS:
        raise ValueError("renewal limit reached")
    loan.renewals += 1
    return store.save_loan(loan)
