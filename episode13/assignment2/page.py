"""
EPISODE 13 - ASSIGNMENT 2: page.py module
HTML template rendering with dynamic content
"""


def render_base(title, content, flash_html=''):
    """
    Render base HTML structure
    Demonstrates base template pattern
    """
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>{title}</title>
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{ 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: #f5f5f5;
                color: #333;
            }}
            nav {{
                background: #2c3e50;
                padding: 1rem;
                color: white;
            }}
            nav a {{
                color: white;
                text-decoration: none;
                margin-right: 1.5rem;
                transition: opacity 0.3s;
            }}
            nav a:hover {{
                opacity: 0.8;
            }}
            .container {{
                max-width: 1000px;
                margin: 2rem auto;
                padding: 0 1rem;
            }}
            .alert {{
                padding: 1rem;
                margin: 1rem 0;
                border-radius: 4px;
                animation: slideIn 0.3s ease-in;
            }}
            .alert-success {{
                background: #d4edda;
                color: #155724;
                border: 1px solid #c3e6cb;
            }}
            .alert-error {{
                background: #f8d7da;
                color: #721c24;
                border: 1px solid #f5c6cb;
            }}
            .card {{
                background: white;
                border-radius: 4px;
                padding: 1.5rem;
                box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                margin: 1rem 0;
            }}
            .stats {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 1rem;
                margin: 1rem 0;
            }}
            .stat-box {{
                background: white;
                padding: 1.5rem;
                border-left: 4px solid #3498db;
                box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            }}
            .stat-value {{
                font-size: 2rem;
                font-weight: bold;
                color: #3498db;
            }}
            .stat-label {{
                color: #666;
                font-size: 0.9rem;
                margin-top: 0.5rem;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                background: white;
                margin: 1rem 0;
            }}
            th {{
                background: #f8f9fa;
                padding: 1rem;
                text-align: left;
                font-weight: 600;
                border-bottom: 2px solid #dee2e6;
            }}
            td {{
                padding: 1rem;
                border-bottom: 1px solid #dee2e6;
            }}
            tr:hover {{
                background: #f9f9f9;
            }}
            form {{
                background: white;
                padding: 1.5rem;
                border-radius: 4px;
                box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            }}
            .form-group {{
                margin: 1rem 0;
            }}
            label {{
                display: block;
                margin-bottom: 0.5rem;
                font-weight: 500;
            }}
            input, textarea {{
                width: 100%;
                padding: 0.5rem;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 1rem;
                font-family: inherit;
            }}
            input:focus {{
                outline: none;
                border-color: #3498db;
                box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1);
            }}
            button {{
                background: #3498db;
                color: white;
                border: none;
                padding: 0.75rem 1.5rem;
                border-radius: 4px;
                cursor: pointer;
                font-size: 1rem;
                transition: background 0.3s;
                margin-right: 0.5rem;
            }}
            button:hover {{
                background: #2980b9;
            }}
            button.danger {{
                background: #e74c3c;
            }}
            button.danger:hover {{
                background: #c0392b;
            }}
            a.btn {{
                display: inline-block;
                background: #3498db;
                color: white;
                text-decoration: none;
                padding: 0.75rem 1.5rem;
                border-radius: 4px;
                transition: background 0.3s;
            }}
            a.btn:hover {{
                background: #2980b9;
            }}
            a.btn.danger {{
                background: #e74c3c;
            }}
            a.btn.danger:hover {{
                background: #c0392b;
            }}
            @keyframes slideIn {{
                from {{ transform: translateY(-10px); opacity: 0; }}
                to {{ transform: translateY(0); opacity: 1; }}
            }}
        </style>
    </head>
    <body>
        <nav>
            <div class="container">
                <strong>Student Dashboard</strong>
                <a href="/">Dashboard</a>
                <a href="/students">Students</a>
                <a href="/add">Add Student</a>
            </div>
        </nav>
        <div class="container">
            {flash_html}
            {content}
        </div>
    </body>
    </html>
    '''


def render_home(students, statistics):
    """
    Render home/dashboard page with statistics
    Demonstrates dynamic content injection
    """
    total = statistics['total_students']
    average = statistics['average_grade']
    pass_rate = statistics['pass_rate']
    
    stats_html = f'''
    <div class="stats">
        <div class="stat-box">
            <div class="stat-value">{total}</div>
            <div class="stat-label">Total Students</div>
        </div>
        <div class="stat-box">
            <div class="stat-value">{average:.2f}</div>
            <div class="stat-label">Average Grade</div>
        </div>
        <div class="stat-box">
            <div class="stat-value">{pass_rate:.1f}%</div>
            <div class="stat-label">Pass Rate (≥60)</div>
        </div>
    </div>
    '''
    
    if total > 0:
        student_html = '<h2>Recent Students</h2><table><thead><tr><th>ID</th><th>Name</th><th>Grade</th><th>Actions</th></tr></thead><tbody>'
        for student in students[-5:]:
            student_html += f'''
            <tr>
                <td>{student["id"]}</td>
                <td>{student["name"]}</td>
                <td>{student["grade"]:.2f}</td>
                <td>
                    <a href="/edit?id={student["id"]}" class="btn">Edit</a>
                    <a href="/delete?id={student["id"]}" class="btn danger" onclick="return confirm('Delete this student?')">Delete</a>
                </td>
            </tr>
            '''
        student_html += '</tbody></table>'
    else:
        student_html = '<p>No students yet. <a href="/add">Add one now</a></p>'
    
    content = f'''
    <h1>Dashboard</h1>
    {stats_html}
    {student_html}
    '''
    
    return render_base('Dashboard', content)


def render_student_list(students, flash_html=''):
    """Render list of all students"""
    if students:
        rows = ''
        for student in students:
            rows += f'''
            <tr>
                <td>{student["id"]}</td>
                <td>{student["name"]}</td>
                <td>{student["grade"]:.2f}</td>
                <td>
                    <a href="/edit?id={student["id"]}" class="btn">Edit</a>
                    <a href="/delete?id={student["id"]}" class="btn danger" onclick="return confirm('Delete this student?')">Delete</a>
                </td>
            </tr>
            '''
        table = f'''
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Grade</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                {rows}
            </tbody>
        </table>
        '''
    else:
        table = '<p>No students found. <a href="/add">Add a student</a></p>'
    
    content = f'<h1>Students</h1>{table}'
    return render_base('Students', content, flash_html)


def render_add_form(flash_html=''):
    """Render add student form"""
    content = '''
    <h1>Add Student</h1>
    <form method="POST" action="/add">
        <div class="form-group">
            <label for="id">Student ID:</label>
            <input type="number" id="id" name="id" required>
        </div>
        <div class="form-group">
            <label for="name">Name:</label>
            <input type="text" id="name" name="name" required>
        </div>
        <div class="form-group">
            <label for="grade">Grade:</label>
            <input type="number" id="grade" name="grade" min="0" max="100" step="0.1" required>
        </div>
        <button type="submit">Add Student</button>
        <a href="/students" class="btn" style="display: inline-block;">Cancel</a>
    </form>
    '''
    return render_base('Add Student', content, flash_html)


def render_edit_form(student, flash_html=''):
    """Render edit student form"""
    content = f'''
    <h1>Edit Student</h1>
    <form method="POST" action="/edit">
        <input type="hidden" name="id" value="{student["id"]}">
        <div class="form-group">
            <label for="name">Name:</label>
            <input type="text" id="name" name="name" value="{student["name"]}" required>
        </div>
        <div class="form-group">
            <label for="grade">Grade:</label>
            <input type="number" id="grade" name="grade" min="0" max="100" step="0.1" value="{student["grade"]}" required>
        </div>
        <button type="submit">Update Student</button>
        <a href="/students" class="btn" style="display: inline-block;">Cancel</a>
    </form>
    '''
    return render_base('Edit Student', content, flash_html)


def render_error(message):
    """Render error page"""
    content = f'<h1>Error</h1><p>{message}</p>'
    return render_base('Error', content)
