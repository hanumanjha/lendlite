# API

The routes are listed in `ROUTES` in `src/lendlite/api.py`.

| Method | Path | What it does |
| --- | --- | --- |
| GET | `/health` | Reports that the service is up. |
| GET | `/books` | Lists every book. |
| POST | `/books` | Adds a book with a title and an author. |
| POST | `/members` | Adds a member with a name. |
| POST | `/loans` | Lends a book to a member. |
| POST | `/loans/{id}/return` | Takes a borrowed book back. |
| POST | `/loans/{id}/renew` | Renews a loan to give the member more time. |
| GET | `/members/{id}/loans` | Lists the loans of one member. |

A request that breaks a lending rule gets status 400 and an error message.
