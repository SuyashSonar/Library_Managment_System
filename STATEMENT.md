# Project Statement: Library Management System

## 1. Problem Statement

Small libraries, like those in schools, colleges, or local communities, often keep track of books using notebooks or loose spreadsheets. This makes it easy to lose track of which book is with whom, when it is due, and how much fine someone owes. Counting available copies by hand also leads to mistakes.

This project is a simple command-line program that takes care of these everyday tasks, so a librarian can manage books, members, loans and late fines in one place without paperwork.

## 2. Scope of the Project

**What the project covers**

- Keeping a record of books (title, author, number of copies) and members
- Issuing books for 14 days, with a limit of 3 books per member
- Returning books and calculating late fines at Rs 2 per day
- Searching for books and listing overdue books
- Saving all data in a local JSON file so it is not lost when the program closes
- Running fully from the terminal with only the Python standard library

**What the project does not cover**

- A graphical or web interface
- Multiple users using the system at the same time
- Login and different roles for librarians and members
- Online fine payment, reservations or renewals
- Barcode scanning or a database server

## 3. Target Users

- **Librarians / library staff** of small school, college or community libraries who need a simple way to manage lending
- **Students and beginners** who want an example of a complete Python project covering functions, dictionaries, file handling and exceptions
- **Course evaluators**, who can run the project easily from the command line with no extra setup

## 4. High-Level Features

- **Book management:** add, list, search and remove books; adding the same book again increases its copies
- **Member management:** register members with unique ids and view what each member currently has
- **Issue and return:** automatic due dates, copy count updates and checks (no copies left, borrowing limit, duplicate issue)
- **Fine calculation:** late returns are charged automatically per day
- **Overdue report:** a quick list of late books with days late and fine so far
- **Persistent storage:** data is saved automatically after every change
- **Friendly error handling:** wrong input shows a clear message instead of crashing
