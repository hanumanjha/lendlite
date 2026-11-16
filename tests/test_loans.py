import sys
import unittest
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from lendlite import loans, store  # noqa: E402
from lendlite.fees import calculate_late_fee  # noqa: E402
from lendlite.models import Book, Member  # noqa: E402

START = date(2025, 1, 1)


def reset_and_seed(book_count: int = 4) -> None:
    store.BOOKS.clear()
    store.MEMBERS.clear()
    store.LOANS.clear()
    store.add_member(Member("M-1", "Ada Example"))
    for number in range(1, book_count + 1):
        store.add_book(Book(f"B-{number}", f"Book {number}", "Sample Author"))


class BorrowTests(unittest.TestCase):
    def setUp(self):
        reset_and_seed()

    def test_borrow_marks_book_unavailable(self):
        loan = loans.borrow_book("M-1", "B-1", START)
        self.assertFalse(store.get_book("B-1").available)
        self.assertEqual(loan.borrowed_on, START)

    def test_fourth_book_is_refused(self):
        for number in (1, 2, 3):
            loans.borrow_book("M-1", f"B-{number}", START)
        with self.assertRaises(ValueError):
            loans.borrow_book("M-1", "B-4", START)

    def test_book_that_is_out_is_refused(self):
        store.add_member(Member("M-2", "Ben Example"))
        loans.borrow_book("M-1", "B-1", START)
        with self.assertRaises(ValueError):
            loans.borrow_book("M-2", "B-1", START)


class ReturnTests(unittest.TestCase):
    def setUp(self):
        reset_and_seed()

    def test_return_closes_loan_and_frees_book(self):
        loan = loans.borrow_book("M-1", "B-1", START)
        closed = loans.return_book(loan.id, START + timedelta(days=5))
        self.assertEqual(closed.returned_on, START + timedelta(days=5))
        self.assertTrue(store.get_book("B-1").available)

    def test_return_frees_a_borrowing_slot(self):
        first = loans.borrow_book("M-1", "B-1", START)
        loans.borrow_book("M-1", "B-2", START)
        loans.borrow_book("M-1", "B-3", START)
        loans.return_book(first.id, START)
        self.assertIsNotNone(loans.borrow_book("M-1", "B-4", START))


class RenewTests(unittest.TestCase):
    def setUp(self):
        reset_and_seed()

    def test_two_renewals_work_and_a_third_is_refused(self):
        loan = loans.borrow_book("M-1", "B-1", START)
        loans.renew_loan(loan.id, START)
        loans.renew_loan(loan.id, START)
        self.assertEqual(loan.renewals, 2)
        with self.assertRaises(ValueError):
            loans.renew_loan(loan.id, START)

    def test_each_renewal_adds_seven_days(self):
        loan = loans.borrow_book("M-1", "B-1", START)
        self.assertEqual(loans.due_date(loan), START + timedelta(days=21))
        loans.renew_loan(loan.id, START)
        self.assertEqual(loans.due_date(loan), START + timedelta(days=28))

    def test_overdue_loan_cannot_be_renewed(self):
        loan = loans.borrow_book("M-1", "B-1", START)
        late = START + timedelta(days=22)
        self.assertTrue(loans.is_overdue(loan, late))
        with self.assertRaises(ValueError):
            loans.renew_loan(loan.id, late)


class LateFeeTests(unittest.TestCase):
    def setUp(self):
        reset_and_seed()

    def test_no_fee_on_the_due_date(self):
        loan = loans.borrow_book("M-1", "B-1", START)
        self.assertEqual(calculate_late_fee(loan, START + timedelta(days=21)), 0)

    def test_fee_is_twenty_five_cents_per_late_day(self):
        loan = loans.borrow_book("M-1", "B-1", START)
        self.assertEqual(calculate_late_fee(loan, START + timedelta(days=26)), 125)

    def test_fee_stops_growing_after_return(self):
        loan = loans.borrow_book("M-1", "B-1", START)
        loans.return_book(loan.id, START + timedelta(days=23))
        self.assertEqual(calculate_late_fee(loan, START + timedelta(days=60)), 50)


if __name__ == "__main__":
    unittest.main()
