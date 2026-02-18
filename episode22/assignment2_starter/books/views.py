from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

# TODO: Create CRUD views (Topics 65-80):
#
# 1. book_list (GET):
#    - Display all books
#    - Template: books/book_list.html
#    - Context: books
#
# 2. book_create (GET/POST):
#    - GET: Display empty form
#    - POST: Create new book
#    - Form: BookForm
#    - Template: books/book_form.html
#    - Success: messages + redirect to list
#    - Topics 65-70: Form validation, error display, success message
#
# 3. book_update (GET/POST):
#    - GET: Display form with book data
#    - POST: Update existing book
#    - Form: BookForm with instance
#    - Template: books/book_form.html
#    - Success: messages + redirect to list
#    - Topics 66-77: Pre-filled form, data persistence
#
# 4. book_delete (GET/POST):
#    - GET: Display confirmation page
#    - POST: Delete book
#    - Template: books/book_confirm_delete.html
#    - Success: messages + redirect to list
#    - Topics 68-70: Confirmation, warning, success
