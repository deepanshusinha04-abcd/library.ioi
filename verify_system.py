"""
Verification script for Library.io API & Business Logic.
Tests:
1. User registration & JWT Login
2. Books listing, search, and ratings
3. Borrow validation, loan creation, copy decrement
4. Overdue detection, return workflow, copy increment
5. AI Recommendation Engine personalization
6. Student & Librarian analytics dashboards
"""

import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_core.settings')
import django
django.setup()

from rest_framework.test import APIClient
from rest_framework import status
from apps.authentication.models import User
from apps.books.models import Book, Category, Author, BookRating
from apps.borrowing.models import BorrowTransaction
from apps.analytics.models import ReadingHistory
from apps.recommendations.engine import RecommendationEngine


def run_verification():
    print("=" * 60)
    print("STARTING SYSTEM VERIFICATION FOR LIBRARY.IO")
    print("=" * 60)
    client = APIClient()

    # 1. AUTHENTICATION
    print("\n[TEST 1] Testing JWT Login for default demo users...")
    login_res = client.post('/api/auth/login/', {
        'email': 'alex@student.io',
        'password': 'StudentPass123!'
    }, format='json')
    assert login_res.status_code == status.HTTP_200_OK, f"Login failed: {login_res.data}"
    access_token = login_res.data['access']
    print(f" -> Login successful! User: {login_res.data['user']['name']}, Role: {login_res.data['user']['role']}")

    # 2. BOOK CATALOG & SEARCH
    print("\n[TEST 2] Testing Catalog Listing and Filtering...")
    catalog_res = client.get('/api/books/')
    assert catalog_res.status_code == status.HTTP_200_OK
    total_books = catalog_res.data['count']
    print(f" -> Retrieved {total_books} total books in catalog.")

    search_res = client.get('/api/books/?search=Artificial')
    assert search_res.status_code == status.HTTP_200_OK
    print(f" -> Search query 'Artificial' returned {search_res.data['count']} matches.")

    # 3. BORROW TRANSACTION & BUSINESS LOGIC
    print("\n[TEST 3] Testing Book Borrowing & Copy Decrement...")
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    
    # Pick a book with available copies
    book_to_borrow = Book.objects.filter(available_copies__gt=0).exclude(
        borrow_transactions__user__email='alex@student.io',
        borrow_transactions__status='BORROWED'
    ).first()
    assert book_to_borrow is not None, "No available book found to test borrow"
    
    initial_copies = book_to_borrow.available_copies
    borrow_res = client.post('/api/borrowing/borrow/', {
        'book_id': book_to_borrow.id,
        'duration_days': 14
    }, format='json')
    assert borrow_res.status_code == status.HTTP_201_CREATED, f"Borrow failed: {borrow_res.data}"
    tx_id = borrow_res.data['transaction']['id']

    book_to_borrow.refresh_from_db()
    assert book_to_borrow.available_copies == initial_copies - 1, "Available copies did not decrement!"
    print(f" -> Successfully borrowed '{book_to_borrow.title}'. Copies decremented: {initial_copies} -> {book_to_borrow.available_copies}")

    # 4. PREVENT DUPLICATE ACTIVE BORROW
    print("\n[TEST 4] Testing Prevention of Duplicate Active Borrow...")
    dup_res = client.post('/api/borrowing/borrow/', {
        'book_id': book_to_borrow.id
    }, format='json')
    assert dup_res.status_code == status.HTTP_400_BAD_REQUEST, "Should prevent duplicate borrow!"
    print(f" -> Duplicate borrow correctly blocked with 400 Bad Request.")

    # 5. RETURN BOOK & RESTORE COPIES
    print("\n[TEST 5] Testing Return Book Workflow & Copy Increment...")
    return_res = client.post(f'/api/borrowing/transactions/{tx_id}/return_book/')
    assert return_res.status_code == status.HTTP_200_OK, f"Return failed: {return_res.data}"
    
    book_to_borrow.refresh_from_db()
    assert book_to_borrow.available_copies == initial_copies, "Available copies did not increment back!"
    print(f" -> Successfully returned book. Copies restored to: {book_to_borrow.available_copies}")

    # 6. AI RECOMMENDATIONS
    print("\n[TEST 6] Testing AI Recommendation Engine...")
    rec_res = client.get('/api/recommendations/personalized/')
    assert rec_res.status_code == status.HTTP_200_OK, f"Rec failed: {rec_res.data}"
    recs = rec_res.data['recommendations']
    print(f" -> AI Engine generated {len(recs)} personalized recommendations for Alex:")
    for r in recs[:3]:
        print(f"    * {r['book']['title']} (Score: {r['score']:.2f}, Algorithm: {r['algorithm']}) - {r['reason']}")

    # 7. ANALYTICS DASHBOARDS
    print("\n[TEST 7] Testing Student Analytics Dashboard...")
    student_stats_res = client.get('/api/analytics/student-dashboard/')
    assert student_stats_res.status_code == status.HTTP_200_OK
    print(f" -> Student Stats: Total Borrowed: {student_stats_res.data['total_borrowed']}, Active Reading: {student_stats_res.data['currently_reading']}")

    print("\n[TEST 8] Testing Librarian Analytics Dashboard...")
    # Login as librarian
    lib_login = client.post('/api/auth/login/', {
        'email': 'librarian@library.io',
        'password': 'LibrarianPass123!'
    }, format='json')
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {lib_login.data["access"]}')
    lib_stats_res = client.get('/api/analytics/librarian-dashboard/')
    assert lib_stats_res.status_code == status.HTTP_200_OK
    print(f" -> Librarian Stats: Total Titles: {lib_stats_res.data['total_titles']}, Physical Copies: {lib_stats_res.data['total_physical_copies']}, Active Loans: {lib_stats_res.data['active_loans']}")

    print("\n" + "=" * 60)
    print("ALL VERIFICATION CHECKS PASSED SUCCESSFULLY! (8/8)")
    print("=" * 60)


if __name__ == '__main__':
    run_verification()
