"""Settings for LendLite. Every value is a plain constant."""

# A book may be borrowed for twenty-one days.
LOAN_PERIOD_DAYS = 21

# A member may borrow at most three books at a time.
MAX_BOOKS_PER_MEMBER = 3

# A loan may be renewed at most two times.
MAX_RENEWALS = 2

# The late fee is twenty-five cents for each day a book is overdue.
LATE_FEE_PER_DAY_CENTS = 25

# Each renewal adds seven days.
RENEWAL_EXTENSION_DAYS = 7
