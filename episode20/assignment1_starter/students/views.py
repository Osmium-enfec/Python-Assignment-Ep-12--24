from django.shortcuts import render, redirect, get_object_or_404

# TODO: Create views (Topics 27-40):
#
# 1. student_list (GET):
#    - Display all students
#    - Topics 38: Model.objects.all()
#    - Context: students
#    - Template: students/list.html
#
# 2. student_detail (GET):
#    - Display single student by ID
#    - Topics 34-36: get_object_or_404()
#    - Topics 28: Request parameter
#    - Context: student
#    - Template: students/detail.html
#
# 3. student_by_roll (GET):
#    - Display single student by roll_no
#    - Topics 5: str converter parameter
#    - Topics 34-36: get_object_or_404()
#    - Context: student
#    - Template: students/detail.html
#
# 4. student_redirect (GET):
#    - Topics 19-26: Redirect after operation
#    - Redirect to list after some operation
