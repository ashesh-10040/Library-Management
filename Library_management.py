# Simple Library Management 
# Project structure and files below — copy files into a folder and run as instructed.

# -----------------------------------------------------------------------------
# README.md
# -----------------------------------------------------------------------------
# Project Title: Simple Library Management 
# Overview:
# A small project that demonstrates:
# - User management (login as librarian)
# - Book CRUD (add, view, update, delete)
# - Search and reporting (list books, report counts)
# - File-based storage (JSON)
# - Clear input/output and simple CLI workflow
#
# Features:
# - Login with a hardcoded librarian user (demo)
# - Add / Update / Delete / List books
# - Search by title or author
# - Export simple report (counts by category)
# - Basic unit test for book storage
#
# Technologies: Python 3 (no external packages required)
# How to run:
# 1. Save the files in a folder (see structure below).
# 2. Run `python main.py` to start the CLI app.
# 3. To run tests: `python -m unittest discover tests`
#
# Files included: README.md, statement.md, main.py, auth.py, books.py, storage.py,
# reports.py, utils.py, tests/test_storage.py
#
# -----------------------------------------------------------------------------
# statement.md
# -----------------------------------------------------------------------------
# Problem statement:
# Many small libraries need a simple system to manage books and keep basic reports.
# This project helps students apply CRUD, file storage, and simple reporting.
# Scope: Small demo CLI application suitable for learning.
# Target users: Students, small library staff, or learners practicing Python.
# High-level features: login, add/view/update/delete books, search, generate report.

# -----------------------------------------------------------------------------
# File: storage.py
# Responsible for reading/writing JSON data (acts as a tiny database).
# -----------------------------------------------------------------------------

# storage.py
import json
import os
from typing import List, Dict, Any

DB_FILE = 'data.json'

def _ensure_db():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, 'w') as f:
            json.dump({'books': [], 'users': []}, f, indent=2)

def read_db() -> Dict[str, Any]:
    _ensure_db()
    with open(DB_FILE, 'r') as f:
        return json.load(f)

def write_db(data: Dict[str, Any]):
    with open(DB_FILE, 'w') as f:
        json.dump(data, f, indent=2)

# helper functions for books

def get_all_books() -> List[Dict[str, Any]]:
    db = read_db()
    return db.get('books', [])

def save_all_books(books: List[Dict[str, Any]]):
    db = read_db()
    db['books'] = books
    write_db(db)

# users

def get_all_users() -> List[Dict[str, Any]]:
    db = read_db()
    return db.get('users', [])

def add_user(user: Dict[str, Any]):
    db = read_db()
    users = db.get('users', [])
    users.append(user)
    db['users'] = users
    write_db(db)

# -----------------------------------------------------------------------------
# File: utils.py
# Small utilities for input validation and id generation
# -----------------------------------------------------------------------------

# utils.py
import uuid
from typing import Optional

def generate_id() -> str:
    return str(uuid.uuid4())[:8]

def confirm(prompt: str) -> bool:
    ans = input(f"{prompt} (y/n): ").strip().lower()
    return ans == 'y'

# -----------------------------------------------------------------------------
# File: auth.py
# Handles a simple login flow and initial demo user creation
# -----------------------------------------------------------------------------

# auth.py
from storage import get_all_users, add_user

DEMO_USER = {'username': 'librarian', 'password': 'lib123', 'role': 'admin'}

def ensure_demo_user():
    users = get_all_users()
    if not any(u['username'] == DEMO_USER['username'] for u in users):
        add_user(DEMO_USER)

def login() -> bool:
    print('\n=== Login ===')
    username = input('Username: ').strip()
    password = input('Password: ').strip()
    users = get_all_users()
    for u in users:
        if u['username'] == username and u['password'] == password:
            print('Login successful!')
            return True
    print('Login failed. Try demo user: librarian / lib123')
    return False

# -----------------------------------------------------------------------------
# File: books.py
# Book CRUD operations using storage helpers
# -----------------------------------------------------------------------------

# books.py
from typing import List, Dict, Any, Optional
from storage import get_all_books, save_all_books
from utils import generate_id


def add_book(title: str, author: str, category: str, year: int) -> Dict[str, Any]:
    books = get_all_books()
    book = {
        'id': generate_id(),
        'title': title,
        'author': author,
        'category': category,
        'year': year
    }
    books.append(book)
    save_all_books(books)
    return book

def list_books() -> List[Dict[str, Any]]:
    return get_all_books()

def find_book_by_id(book_id: str) -> Optional[Dict[str, Any]]:
    books = get_all_books()
    for b in books:
        if b['id'] == book_id:
            return b
    return None

def update_book(book_id: str, **kwargs) -> Optional[Dict[str, Any]]:
    books = get_all_books()
    for i, b in enumerate(books):
        if b['id'] == book_id:
            books[i].update({k: v for k, v in kwargs.items() if v is not None})
            save_all_books(books)
            return books[i]
    return None

def delete_book(book_id: str) -> bool:
    books = get_all_books()
    new_books = [b for b in books if b['id'] != book_id]
    if len(new_books) == len(books):
        return False
    save_all_books(new_books)
    return True

def search_books(query: str) -> List[Dict[str, Any]]:
    q = query.lower()
    books = get_all_books()
    return [b for b in books if q in b['title'].lower() or q in b['author'].lower()]

# -----------------------------------------------------------------------------
# File: reports.py
# Small reporting utilities (e.g., count by category)
# -----------------------------------------------------------------------------

# reports.py
from typing import Dict
from books import list_books


def count_by_category() -> Dict[str, int]:
    books = list_books()
    counts = {}
    for b in books:
        cat = b.get('category', 'Unknown')
        counts[cat] = counts.get(cat, 0) + 1
    return counts

# -----------------------------------------------------------------------------
# File: main.py
# Simple command-line interface showing workflow and user interaction
# -----------------------------------------------------------------------------

# main.py
import sys
from auth import ensure_demo_user, login
from books import add_book, list_books, update_book, delete_book, find_book_by_id, search_books
from reports import count_by_category

MENU = '''\nSimple Library CLI - choose an option:
1. Add book
2. List books
3. Update book
4. Delete book
5. Search books
6. Generate report (count by category)
7. Exit
'''


def run_app():
    ensure_demo_user()
    if not login():
        return
    while True:
        print(MENU)
        choice = input('Enter choice: ').strip()
        if choice == '1':
            title = input('Title: ').strip()
            author = input('Author: ').strip()
            category = input('Category: ').strip() or 'General'
            year = input('Year: ').strip()
            try:
                year = int(year)
            except:
                year = 0
            book = add_book(title, author, category, year)
            print('Added book:', book)
        elif choice == '2':
            books = list_books()
            print('\nBooks:')
            for b in books:
                print(f"{b['id']} | {b['title']} by {b['author']} ({b['year']}) - {b['category']}")
        elif choice == '3':
            bid = input('Enter book id to update: ').strip()
            b = find_book_by_id(bid)
            if not b:
                print('Book not found')
                continue
            print('Leave blank to keep current value')
            title = input(f"Title [{b['title']}]: ").strip() or None
            author = input(f"Author [{b['author']}]: ").strip() or None
            category = input(f"Category [{b['category']}]: ").strip() or None
            year = input(f"Year [{b['year']}]: ").strip() or None
            year_val = None
            if year is not None:
                try:
                    year_val = int(year)
                except:
                    year_val = None
            updated = update_book(bid, title=title, author=author, category=category, year=year_val)
            print('Updated:', updated)
        elif choice == '4':
            bid = input('Enter book id to delete: ').strip()
            if delete_book(bid):
                print('Deleted')
            else:
                print('Book not found')
        elif choice == '5':
            q = input('Search query (title or author): ').strip()
            results = search_books(q)
            print('Results:')
            for r in results:
                print(f"{r['id']} | {r['title']} by {r['author']}")
        elif choice == '6':
            report = count_by_category()
            print('Count by category:')
            for k, v in report.items():
                print(f"{k}: {v}")
        elif choice == '7':
            print('Goodbye')
            break
        else:
            print('Invalid choice')

if __name__ == '__main__':
    run_app()

# -----------------------------------------------------------------------------
# File: tests/test_storage.py
# Very small unit test to show testing usage
# -----------------------------------------------------------------------------

# tests/test_storage.py
import unittest
import os
import json
from storage import DB_FILE, write_db, read_db, _ensure_db

class TestStorage(unittest.TestCase):
    def setUp(self):
        # backup
        if os.path.exists(DB_FILE):
            os.rename(DB_FILE, DB_FILE + '.bak')

    def tearDown(self):
        if os.path.exists(DB_FILE):
            os.remove(DB_FILE)
        if os.path.exists(DB_FILE + '.bak'):
            os.rename(DB_FILE + '.bak', DB_FILE)

    def test_read_write(self):
        data = {'books': [{'id':'1','title':'A'}], 'users': []}
        write_db(data)
        loaded = read_db()
        self.assertEqual(loaded['books'][0]['title'], 'A')

if __name__ == '__main__':
    unittest.main()

# -----------------------------------------------------------------------------
# Usage notes for students (small checklist)
# 1. Create folder and files as named above.
# 2. Run `python main.py` to try the app.
# 3. Read README.md and statement.md to prepare your GitHub repo.
# 4. Put screenshots and add README instructions for submission.
# -----------------------------------------------------------------------------
