# Girls Education Sponsorship & Mentorship Platform

A menu-driven command-line app for managing students, sponsors, mentors, and their assignments in support of girls' education. Built in Python with a MySQL database on Aiven, using a layered architecture: **menus → services → models → database**.

> Peer Learning Project II — BSE Year 1, African Leadership University.

## Features

- **Students / Sponsors / Mentors** — register, view, search, update, delete.
- **Assignments** — match sponsors and mentors to students, with duplicate prevention at both the app and database level.
- **Reports** — totals for each entity, plus sponsored vs. unsponsored counts and a sponsorship rate.

## Tech Stack

Python 3 · MySQL (Aiven) · `mysql-connector-python` · `python-dotenv`

## Setup

**1. Virtual environment**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1        # Windows
# source .venv/bin/activate       # macOS / Linux
```

**2. Install dependencies**

```bash
pip install -r requirements.txt
```

**3. Configure credentials** — copy the template and fill in your Aiven values (the `.env` file is gitignored, so each member needs their own):

```bash
copy .env.example .env            # Windows
# cp .env.example .env            # macOS / Linux
```

**4. Run**

```bash
python3 main.py
```

Tables are created automatically on first run (`CREATE TABLE IF NOT EXISTS`), then you land on the main menu. Type a number to navigate; `0` to exit.

## Project Structure

```
config/      Database settings from environment variables
database/    Connection module and schema
models/      Plain data classes (Student, Sponsor, Mentor, User)
services/    Business logic and SQL for each feature
menus/       CLI screens and routing (no SQL here)
utils/       Table printing, prompts, validators, password hashing
main.py      Entry point
```

## Team

| Member | Module |
|---|---|
| acquahh | Database & integration lead (`config/`, `database/`, `main.py`) |
| Abigail | Students |
| Arnold | Sponsors |
| Wezzie | Mentors |
| Yom | Assignments |
| mwayo-tech | Reports, validation & testing |

## Troubleshooting

- **`Startup failed` / can't connect** — check your `.env` values against the Aiven console.
- **PowerShell "running scripts is disabled"** — run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once, confirm with `Y`, then activate again.
- **`ModuleNotFoundError`** — run from the project root (the folder with `main.py`).

## Status

Core features (students, sponsors, mentors, assignments, reports) are fully functional. Password hashing and a roles-based `Users` table exist, but the login flow is not yet wired into `main.py` — the app currently opens straight to the menu.
