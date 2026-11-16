# LendLite

LendLite is a small sample library-lending API. It keeps everything in memory and uses only the Python standard library.

## Features

- Add books
- Add members
- Borrow a book
- Return a book
- Renew a loan
- List a member's loans

## Project layout

```
src/lendlite/
  config.py        the lending settings
  models.py        Book, Member and Loan records
  store.py         in-memory storage
  loans.py         borrow, return and renew
  fees.py          late fees
  api.py           the route table and its handlers
tests/
  test_loans.py    unit tests
docs/              the API, the lending rules and the architecture
```

## More information

See the `docs/` folder:

- `docs/api.md` lists the endpoints.
- `docs/loan-rules.md` explains the lending rules.
- `docs/architecture.md` explains how the modules fit together.
