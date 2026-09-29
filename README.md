# Library Management System

A small command-line app to run a library: add books, register members, issue and return books, and keep track of late fines. It's written in plain Python with no external packages, and everything is saved in a JSON file so nothing is lost when you close it.

I built this for the Python Essentials course (VITyarthi) project evaluation.

## What it can do

- Add books (adding the same title + author again just increases the copies)
- List, search, and remove books
- Register members
- Issue a book (14 days, max 3 books per member)
- Return a book and automatically work out the fine (Rs 2 per late day)
- Show all overdue books
- Save data automatically to `data/library.json`

## What you need

- Python 3.8 or newer
- A terminal (Command Prompt, PowerShell, Terminal, whatever you like)

No `pip install` needed, it only uses the standard library.

## How to run it

1. **Check Python is installed**
   ```
   python --version
   ```
   On Mac/Linux you might need `python3` instead of `python`.

2. **Get the code**
   ```
   git clone https://github.com/SuyashSonar/Library_Managment_System.git
   cd library-management-system
   ```

3. **Start the program**
   ```
   python main.py
   ```

4. **Use the menu.** Type a number and press Enter. A quick first try:
   - `1` to add a book
   - `5` to register a member (you'll get an id like `M001`)
   - `7` to issue the book (use the member id and book id, like `M001` and `B001`)
   - `8` to return it

The data file is created automatically the first time you add something. To start fresh, delete `data/library.json`.

## Project layout

```
library-management-system/
├── main.py            # the menu and user input
├── library.py         # all the actual logic + saving/loading
├── test_library.py    # unit tests
├── data/              # library.json gets created here
├── REPORT.md          # project report
└── README.md
```

I kept the menu code (`main.py`) separate from the logic (`library.py`) so the logic could be tested without typing into the menu.

## Settings

The loan period, fine per day, and book limit are constants at the top of `library.py` (`LOAN_DAYS`, `FINE_PER_DAY`, `MAX_BOOKS`). Change them there if you want different rules.

## Known limitations

- Only one person can use it at a time (it's a single JSON file).
- No login or admin roles.
- Fines are calculated but not stored as a payment record.
