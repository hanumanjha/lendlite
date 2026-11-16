"""Plain records used by LendLite."""

from dataclasses import dataclass
from datetime import date


@dataclass
class Book:
    id: str
    title: str
    author: str
    available: bool = True


@dataclass
class Member:
    id: str
    name: str


@dataclass
class Loan:
    id: str
    member_id: str
    book_id: str
    borrowed_on: date
    returned_on: date | None = None
    renewals: int = 0
