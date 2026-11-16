# Architecture

LendLite is a handful of small modules in `src/lendlite/`.

| Module | What it does |
| --- | --- |
| `config.py` | Holds the lending settings as constants. |
| `models.py` | Defines the Book, Member and Loan records. |
| `store.py` | Keeps books, members and loans in dictionaries and offers functions to add and find them. |
| `loans.py` | Applies the lending rules when a book is borrowed, returned or renewed. |
| `fees.py` | Works out the late fee for a loan. |
| `api.py` | Lists the routes and the handler for each one. There is no web framework. |

## Storage

Storage is in memory. All books, members and loans are lost when the program restarts.
