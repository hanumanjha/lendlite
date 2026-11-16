"""A plain route table. There is no web framework; a server would call these handlers.

Every handler returns (status code, body). Handlers that depend on the current date
take it as a parameter.
"""

from dataclasses import asdict
from datetime import date

from lendlite import loans, store
from lendlite.models import Book, Member


def handle_health() -> tuple[int, dict]:
    return 200, {"status": "ok"}


def handle_list_books() -> tuple[int, list]:
    return 200, [asdict(b) for b in store.list_books()]


def handle_add_book(body: dict) -> tuple[int, dict]:
    book = Book(store.new_id("B"), body["title"], body["author"])
    return 201, asdict(store.add_book(book))


def handle_add_member(body: dict) -> tuple[int, dict]:
    member = Member(store.new_id("M"), body["name"])
    return 201, asdict(store.add_member(member))


def _run(action, *args) -> tuple[int, dict]:
    try:
        return 200, asdict(action(*args))
    except ValueError as error:
        return 400, {"error": str(error)}


def handle_borrow(body: dict, today: date) -> tuple[int, dict]:
    return _run(loans.borrow_book, body["member_id"], body["book_id"], today)


def handle_return(loan_id: str, today: date) -> tuple[int, dict]:
    return _run(loans.return_book, loan_id, today)


def handle_renew(loan_id: str, today: date) -> tuple[int, dict]:
    return _run(loans.renew_loan, loan_id, today)


def handle_member_loans(member_id: str) -> tuple[int, list]:
    return 200, [asdict(x) for x in store.loans_for_member(member_id)]


ROUTES = [
    ("GET", "/health", handle_health),
    ("GET", "/books", handle_list_books),
    ("POST", "/books", handle_add_book),
    ("POST", "/members", handle_add_member),
    ("POST", "/loans", handle_borrow),
    ("POST", "/loans/{id}/return", handle_return),
    ("POST", "/loans/{id}/renew", handle_renew),
    ("GET", "/members/{id}/loans", handle_member_loans),
]
