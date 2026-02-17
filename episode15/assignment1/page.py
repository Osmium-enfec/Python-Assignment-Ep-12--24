"""
EPISODE 15 - HTML Template Rendering Module
Generates HTML pages for the student management system
"""


def html_escape(value):
    """Escape HTML special characters"""
    if value is None:
        return ""
    value = str(value)
    # Escape in correct order
    value = value.replace('&', '&amp;')
    value = value.replace('<', '&lt;')
    value = value.replace('>', '&gt;')
    value = value.replace('"', '&quot;')
    return value


def render_base(title, content):
    """Render base HTML template"""
    return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{html_escape(title)}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        h1 {{ color: #333; }}
        .container {{ max-width: 800px; margin: 0 auto; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 10px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
        tr:hover {{ background-color: #f5f5f5; }}
        .form-group {{ margin-bottom: 15px; }}
        label {{ display: block; margin-bottom: 5px; font-weight: bold; }}
        input, textarea {{ width: 100%; padding: 8px; border: 1px solid #ddd; }}
        button {{ padding: 10px 20px; background-color: #4CAF50; color: white; border: none; cursor: pointer; }}
        button:hover {{ background-color: #45a049; }}
        .btn-secondary {{ background-color: #008CBA; }}
        .btn-secondary:hover {{ background-color: #007399; }}
        .btn-danger {{ background-color: #f44336; }}
        .btn-danger:hover {{ background-color: #da190b; }}
        .error {{ color: red; padding: 10px; background-color: #ffe6e6; margin: 10px 0; }}
        .success {{ color: green; padding: 10px; background-color: #e6ffe6; margin: 10px 0; }}
        .nav {{ margin-bottom: 20px; }}
        a {{ color: #008CBA; text-decoration: none; margin-right: 15px; }}
        a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="nav">
            <a href="/">Home</a>
            <a href="/add">Add Student</a>
        </div>
        {content}
    </div>
</body>
</html>"""


def render_home(students):
    """Render home page with student list"""
    if not students:
        table = "<p>No students found. <a href='/add'>Add one now</a></p>"
    else:
        rows = ""
        for roll_no in sorted(students.keys(), key=lambda x: int(x) if x.isdigit() else x):
            student = students[roll_no]
            name = html_escape(student.get('name', ''))
            grade = html_escape(student.get('grade', ''))
            attendance = html_escape(student.get('attendance', ''))
            added = html_escape(student.get('added_on', ''))
            rows += f"""<tr>
                <td>{html_escape(roll_no)}</td>
                <td>{name}</td>
                <td>{grade}</td>
                <td>{attendance}%</td>
                <td>{added}</td>
                <td>
                    <a href="/view/{html_escape(roll_no)}">View</a> |
                    <a href="/edit/{html_escape(roll_no)}">Edit</a> |
                    <a href="/delete/{html_escape(roll_no)}">Delete</a>
                </td>
            </tr>"""
        
        table = f"""<table>
            <tr>
                <th>Roll No</th>
                <th>Name</th>
                <th>Grade</th>
                <th>Attendance</th>
                <th>Added On</th>
                <th>Actions</th>
            </tr>
            {rows}
        </table>"""
    
    content = f"""<h1>Student Management System</h1>
        <p>Total Students: {len(students)}</p>
        {table}"""
    
    return render_base("Student List", content)


def render_add_form():
    """Render add student form"""
    content = """<h1>Add New Student</h1>
        <form method="post" action="/add">
            <div class="form-group">
                <label for="roll_no">Roll Number:</label>
                <input type="text" id="roll_no" name="roll_no" required>
            </div>
            <div class="form-group">
                <label for="name">Name:</label>
                <input type="text" id="name" name="name" required>
            </div>
            <div class="form-group">
                <label for="grade">Grade:</label>
                <input type="text" id="grade" name="grade" required>
            </div>
            <div class="form-group">
                <label for="attendance">Attendance (%):</label>
                <input type="number" id="attendance" name="attendance" min="0" max="100" required>
            </div>
            <div class="form-group">
                <label for="fees_paid">Fees Paid:</label>
                <input type="checkbox" id="fees_paid" name="fees_paid">
            </div>
            <button type="submit">Add Student</button>
            <a href="/"><button type="button" class="btn-secondary">Cancel</button></a>
        </form>"""
    
    return render_base("Add Student", content)


def render_view_student(roll_no, student):
    """Render view student page"""
    name = html_escape(student.get('name', ''))
    grade = html_escape(student.get('grade', ''))
    attendance = html_escape(student.get('attendance', ''))
    fees = "Yes" if student.get('fees_paid', False) else "No"
    added = html_escape(student.get('added_on', ''))
    
    content = f"""<h1>Student Details</h1>
        <div style="border: 1px solid #ddd; padding: 15px; border-radius: 5px;">
            <p><strong>Roll Number:</strong> {html_escape(roll_no)}</p>
            <p><strong>Name:</strong> {name}</p>
            <p><strong>Grade:</strong> {grade}</p>
            <p><strong>Attendance:</strong> {attendance}%</p>
            <p><strong>Fees Paid:</strong> {fees}</p>
            <p><strong>Added On:</strong> {added}</p>
            <br>
            <a href="/edit/{html_escape(roll_no)}"><button>Edit</button></a>
            <a href="/delete/{html_escape(roll_no)}"><button class="btn-danger">Delete</button></a>
            <a href="/"><button class="btn-secondary">Back</button></a>
        </div>"""
    
    return render_base(f"View Student - {name}", content)


def render_edit_form(roll_no, student):
    """Render edit student form"""
    name = html_escape(student.get('name', ''))
    grade = html_escape(student.get('grade', ''))
    attendance = html_escape(student.get('attendance', ''))
    fees_checked = 'checked' if student.get('fees_paid', False) else ''
    
    content = f"""<h1>Edit Student</h1>
        <form method="post" action="/edit/{html_escape(roll_no)}">
            <div class="form-group">
                <label>Roll Number:</label>
                <p>{html_escape(roll_no)} (Cannot be changed)</p>
            </div>
            <div class="form-group">
                <label for="name">Name:</label>
                <input type="text" id="name" name="name" value="{name}" required>
            </div>
            <div class="form-group">
                <label for="grade">Grade:</label>
                <input type="text" id="grade" name="grade" value="{grade}" required>
            </div>
            <div class="form-group">
                <label for="attendance">Attendance (%):</label>
                <input type="number" id="attendance" name="attendance" min="0" max="100" value="{attendance}" required>
            </div>
            <div class="form-group">
                <label for="fees_paid">Fees Paid:</label>
                <input type="checkbox" id="fees_paid" name="fees_paid" {fees_checked}>
            </div>
            <button type="submit">Update Student</button>
            <a href="/"><button type="button" class="btn-secondary">Cancel</button></a>
        </form>"""
    
    return render_base("Edit Student", content)


def render_delete_confirmation(roll_no, student):
    """Render delete confirmation page"""
    name = html_escape(student.get('name', ''))
    
    content = f"""<h1>Confirm Delete</h1>
        <div class="error">
            <p>Are you sure you want to delete this student?</p>
            <p><strong>Roll Number:</strong> {html_escape(roll_no)}</p>
            <p><strong>Name:</strong> {name}</p>
        </div>
        <form method="post" action="/delete/{html_escape(roll_no)}">
            <input type="hidden" name="confirm" value="yes">
            <button type="submit" class="btn-danger">Yes, Delete</button>
            <a href="/"><button type="button" class="btn-secondary">Cancel</button></a>
        </form>"""
    
    return render_base("Delete Student", content)


def render_error(error_message):
    """Render error page"""
    content = f"""<h1>Error</h1>
        <div class="error">
            <p>{html_escape(error_message)}</p>
        </div>
        <a href="/"><button>Back to Home</button></a>"""
    
    return render_base("Error", content)


def render_success(message, redirect_url="/"):
    """Render success page"""
    content = f"""<h1>Success</h1>
        <div class="success">
            <p>{html_escape(message)}</p>
        </div>
        <p>Redirecting to <a href="{html_escape(redirect_url)}">home</a>...</p>
        <script>setTimeout(function() {{ window.location.href = "{html_escape(redirect_url)}"; }}, 2000);</script>"""
    
    return render_base("Success", content)
