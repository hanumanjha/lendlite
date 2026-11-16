"""In-memory storage. Everything is lost when the program stops."""

from lendlite.models import Book, Loan, Member

BOOKS: dict[str, Book] = {}
MEMBERS: dict[str, Member] = {}
LOANS: dict[str, Loan] = {}


def add_book(book: Book) -> Book:
    """Store a book (or replace the stored copy with the same id)."""
    BOOKS[book.id] = book
    return book


def add_member(member: Member) -> Member:
    """Store a member (or replace the stored copy with the same id)."""
    MEMBERS[member.id] = member
    return member


def get_book(book_id: str) -> Book | None:
    """Return the book with this id, or None."""
    return BOOKS.get(book_id)


def get_member(member_id: str) -> Member | None:
    """Return the member with this id, or None."""
    return MEMBERS.get(member_id)


def get_loan(loan_id: str) -> Loan | None:
    """Return the loan with this id, or None."""
    return LOANS.get(loan_id)


def save_loan(loan: Loan) -> Loan:
    """Store a loan (or replace the stored copy with the same id)."""
    LOANS[loan.id] = loan
    return loan


def loans_for_member(member_id: str) -> list[Loan]:
    """Return every loan of one member, in the order they were made."""
    return [loan for loan in LOANS.values() if loan.member_id == member_id]


def list_books() -> list[Book]:
    """Return every stored book."""
    return list(BOOKS.values())


def new_id(prefix: str) -> str:
    """Make the next id for a kind of record, such as L-1, L-2."""
    count = sum(1 for key in (*BOOKS, *MEMBERS, *LOANS) if key.startswith(prefix + "-"))
    return f"{prefix}-{count + 1}"
