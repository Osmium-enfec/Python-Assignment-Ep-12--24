"""
Page rendering module for Episode 15 Assignment 2
Advanced templates with search, filter, and statistics views
"""

import html


def html_escape(text):
    """Escape HTML special characters"""
    if not isinstance(text, str):
        text = str(text)
    return html.escape(text)


def render_base(content, title='Student Management'):
    """Base template wrapper"""
    return f"""<!DOCTYPE html>
<html>
<head>
    <title>{html_escape(title)}</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        .container {{
            max-width: 1000px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        .header h1 {{ font-size: 28px; margin-bottom: 5px; }}
        .header p {{ font-size: 14px; opacity: 0.9; }}
        .content {{ padding: 30px; }}
        .navbar {{
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
            flex-wrap: wrap;
            padding: 0 30px;
            padding-top: 15px;
            background: #f8f9fa;
            border-bottom: 1px solid #e0e0e0;
        }}
        .navbar a {{
            display: inline-block;
            padding: 10px 15px;
            background: #667eea;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            font-size: 14px;
            transition: all 0.3s;
        }}
        .navbar a:hover {{ background: #764ba2; transform: translateY(-2px); }}
        .nav-active {{ background: #764ba2 !important; }}
        .form-group {{ margin-bottom: 15px; }}
        .form-group label {{ display: block; margin-bottom: 5px; font-weight: 500; }}
        .form-group input, .form-group select {{
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 14px;
        }}
        .form-group input:focus, .form-group select:focus {{
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102,126,234,0.1);
        }}
        .button-group {{ display: flex; gap: 10px; }}
        .btn {{
            flex: 1;
            padding: 12px;
            border: none;
            border-radius: 5px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
            text-align: center;
            text-decoration: none;
            display: inline-block;
        }}
        .btn-primary {{
            background: #667eea;
            color: white;
        }}
        .btn-primary:hover {{ background: #764ba2; }}
        .btn-secondary {{
            background: #e0e0e0;
            color: #333;
        }}
        .btn-secondary:hover {{ background: #d0d0d0; }}
        .btn-danger {{
            background: #ef5350;
            color: white;
        }}
        .btn-danger:hover {{ background: #c62828; }}
        .btn-success {{
            background: #66bb6a;
            color: white;
        }}
        .btn-success:hover {{ background: #2e7d32; }}
        .table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
        .table th {{
            background: #f5f5f5;
            padding: 12px;
            text-align: left;
            font-weight: 600;
            border-bottom: 2px solid #ddd;
        }}
        .table td {{
            padding: 12px;
            border-bottom: 1px solid #eee;
        }}
        .table tr:hover {{ background: #f9f9f9; }}
        .badge {{
            display: inline-block;
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
        }}
        .badge-success {{ background: #c8e6c9; color: #1b5e20; }}
        .badge-danger {{ background: #ffcdd2; color: #b71c1c; }}
        .badge-warning {{ background: #fff3cd; color: #856404; }}
        .badge-info {{ background: #bbdefb; color: #0d47a1; }}
        .alert {{
            padding: 15px;
            margin-bottom: 20px;
            border-radius: 5px;
            border-left: 4px solid;
        }}
        .alert-error {{
            background: #ffebee;
            border-color: #ef5350;
            color: #c62828;
        }}
        .alert-success {{
            background: #e8f5e9;
            border-color: #66bb6a;
            color: #1b5e20;
        }}
        .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; }}
        .stat-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        }}
        .stat-value {{ font-size: 28px; font-weight: bold; }}
        .stat-label {{ font-size: 12px; opacity: 0.8; margin-top: 5px; }}
        .search-form {{ display: flex; gap: 10px; margin-bottom: 20px; }}
        .search-form input {{ flex: 1; }}
        .recent-students {{ margin-top: 20px; }}
        .action-links {{ display: flex; gap: 10px; }}
        .action-links a {{
            padding: 6px 12px;
            font-size: 12px;
            border-radius: 3px;
            text-decoration: none;
            background: #667eea;
            color: white;
        }}
        .action-links a:hover {{ background: #764ba2; }}
        .success-message {{
            background: #e8f5e9;
            border-left: 4px solid #66bb6a;
            padding: 15px;
            margin-bottom: 20px;
            border-radius: 5px;
            color: #1b5e20;
        }}
        .filter-section {{
            background: #f9f9f9;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
            border: 1px solid #eee;
        }}
        .filter-row {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📚 Student Management System</h1>
            <p>Advanced Features - Episode 15 Assignment 2</p>
        </div>
        <div class="navbar">
            <a href="/">Dashboard</a>
            <a href="/students">All Students</a>
            <a href="/add">Add Student</a>
            <a href="/stats">Statistics</a>
            <a href="/export/csv">Export CSV</a>
        </div>
        <div class="content">
            {content}
        </div>
    </div>
</body>
</html>"""


def render_dashboard(students, stats, recent):
    """Render dashboard with statistics"""
    stats_html = f"""
    <div class="stats">
        <div class="stat-card">
            <div class="stat-value">{stats['total_students']}</div>
            <div class="stat-label">Total Students</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{stats['average_grade']:.1f}</div>
            <div class="stat-label">Average Grade</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{stats['average_attendance']:.1f}%</div>
            <div class="stat-label">Average Attendance</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{stats['pass_count']}/{stats['total_students']}</div>
            <div class="stat-label">Pass Rate</div>
        </div>
    </div>
    """
    
    recent_html = "<h3 style='margin-top: 30px; margin-bottom: 15px;'>Recent Students</h3>"
    if recent:
        recent_html += '<table class="table"><thead><tr><th>Roll No</th><th>Name</th><th>Grade</th><th>Actions</th></tr></thead><tbody>'
        for student_data in recent:
            roll_no = next((k for k, v in students.items() if v == student_data), 'N/A')
            recent_html += f"""
            <tr>
                <td>{html_escape(roll_no)}</td>
                <td>{student_data.get('name', 'N/A')}</td>
                <td>{student_data.get('grade', 0)}</td>
                <td><a href="/students/{html_escape(roll_no)}" class="btn btn-secondary" style="padding: 5px 10px; font-size: 12px;">View</a></td>
            </tr>
            """
        recent_html += '</tbody></table>'
    else:
        recent_html += '<p style="color: #999;">No students yet.</p>'
    
    content = stats_html + recent_html
    return render_base(content, 'Dashboard')


def render_student_list(students, sort_by='roll_no'):
    """Render all students list"""
    search_form = """
    <div class="search-form">
        <form style="display: flex; gap: 10px; width: 100%;">
            <input type="text" name="q" placeholder="Search by name or roll number" style="flex: 1;">
            <button type="submit" class="btn btn-primary" style="flex: 0.2;">Search</button>
        </form>
    </div>
    
    <div style="margin-bottom: 15px;">
        <p style="font-size: 12px; color: #666; margin-bottom: 10px;">Sort by:</p>
        <div style="display: flex; gap: 10px; flex-wrap: wrap;">
            <a href="/sort?by=roll_no" class="btn btn-secondary" style="padding: 8px 12px; flex: none;">Roll No</a>
            <a href="/sort?by=name" class="btn btn-secondary" style="padding: 8px 12px; flex: none;">Name</a>
            <a href="/sort?by=grade" class="btn btn-secondary" style="padding: 8px 12px; flex: none;">Grade</a>
            <a href="/sort?by=attendance" class="btn btn-secondary" style="padding: 8px 12px; flex: none;">Attendance</a>
        </div>
    </div>
    """
    
    table = '<table class="table"><thead><tr><th>Roll No</th><th>Name</th><th>Grade</th><th>Attendance</th><th>Actions</th></tr></thead><tbody>'
    
    for roll_no, student in students.items():
        grade = student.get('grade', 0)
        grade_badge = 'badge-success' if grade >= 60 else 'badge-danger'
        
        attendance = student.get('attendance', 0)
        att_badge = 'badge-success' if attendance >= 80 else 'badge-warning'
        
        table += f"""
        <tr>
            <td>{html_escape(roll_no)}</td>
            <td>{student.get('name', 'N/A')}</td>
            <td><span class="badge {grade_badge}">{grade}</span></td>
            <td><span class="badge {att_badge}">{attendance}%</span></td>
            <td class="action-links">
                <a href="/students/{html_escape(roll_no)}">View</a>
                <a href="/edit?roll_no={html_escape(roll_no)}">Edit</a>
                <a href="/delete/{html_escape(roll_no)}">Delete</a>
            </td>
        </tr>
        """
    
    table += '</tbody></table>'
    
    if not students:
        table = '<p style="color: #999;">No students found.</p>'
    
    content = search_form + table
    return render_base(content, 'Students List')


def render_search_results(results, query):
    """Render search results"""
    content = f"""
    <p style="margin-bottom: 20px; color: #666;">
        Search results for: <strong>{html_escape(query)}</strong> ({len(results)} found)
    </p>
    
    <table class="table">
        <thead>
            <tr>
                <th>Roll No</th>
                <th>Name</th>
                <th>Grade</th>
                <th>Attendance</th>
                <th>Actions</th>
            </tr>
        </thead>
        <tbody>
    """
    
    if results:
        for roll_no, student in results.items():
            grade = student.get('grade', 0)
            grade_badge = 'badge-success' if grade >= 60 else 'badge-danger'
            attendance = student.get('attendance', 0)
            att_badge = 'badge-success' if attendance >= 80 else 'badge-warning'
            
            content += f"""
            <tr>
                <td>{html_escape(roll_no)}</td>
                <td>{student.get('name', 'N/A')}</td>
                <td><span class="badge {grade_badge}">{grade}</span></td>
                <td><span class="badge {att_badge}">{attendance}%</span></td>
                <td class="action-links">
                    <a href="/students/{html_escape(roll_no)}">View</a>
                    <a href="/edit?roll_no={html_escape(roll_no)}">Edit</a>
                </td>
            </tr>
            """
    else:
        content += '<tr><td colspan="5" style="text-align: center; color: #999;">No results found</td></tr>'
    
    content += """
        </tbody>
    </table>
    
    <div style="margin-top: 15px;">
        <a href="/students" class="btn btn-secondary">Back to All Students</a>
    </div>
    """
    
    return render_base(content, 'Search Results')


def render_filter_results(results, filters):
    """Render filter results"""
    filter_info = []
    if 'grade_min' in filters:
        filter_info.append(f"Grade ≥ {filters['grade_min']}")
    if 'attendance_min' in filters:
        filter_info.append(f"Attendance ≥ {filters['attendance_min']}%")
    
    filter_text = ' AND '.join(filter_info) if filter_info else 'No filters'
    
    content = f"""
    <p style="margin-bottom: 20px; color: #666;">
        Filters: <strong>{filter_text}</strong> ({len(results)} results)
    </p>
    
    <div class="filter-section">
        <form method="get" action="/filter">
            <div class="filter-row">
                <div class="form-group">
                    <label>Minimum Grade</label>
                    <input type="number" name="grade_min" min="0" max="100" placeholder="e.g., 60">
                </div>
                <div class="form-group">
                    <label>Minimum Attendance</label>
                    <input type="number" name="attendance_min" min="0" max="100" placeholder="e.g., 75">
                </div>
                <div style="display: flex; align-items: flex-end; gap: 10px;">
                    <button type="submit" class="btn btn-primary">Apply Filter</button>
                    <a href="/students" class="btn btn-secondary">Clear</a>
                </div>
            </div>
        </form>
    </div>
    
    <table class="table">
        <thead>
            <tr>
                <th>Roll No</th>
                <th>Name</th>
                <th>Grade</th>
                <th>Attendance</th>
                <th>Actions</th>
            </tr>
        </thead>
        <tbody>
    """
    
    if results:
        for roll_no, student in results.items():
            grade = student.get('grade', 0)
            grade_badge = 'badge-success' if grade >= 60 else 'badge-danger'
            attendance = student.get('attendance', 0)
            att_badge = 'badge-success' if attendance >= 80 else 'badge-warning'
            
            content += f"""
            <tr>
                <td>{html_escape(roll_no)}</td>
                <td>{student.get('name', 'N/A')}</td>
                <td><span class="badge {grade_badge}">{grade}</span></td>
                <td><span class="badge {att_badge}">{attendance}%</span></td>
                <td class="action-links">
                    <a href="/students/{html_escape(roll_no)}">View</a>
                </td>
            </tr>
            """
    else:
        content += '<tr><td colspan="5" style="text-align: center; color: #999;">No results match these filters</td></tr>'
    
    content += '</tbody></table>'
    
    return render_base(content, 'Filter Results')


def render_statistics(stats):
    """Render statistics dashboard"""
    content = f"""
    <div class="stats">
        <div class="stat-card">
            <div class="stat-value">{stats['total_students']}</div>
            <div class="stat-label">Total Students</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{stats['average_grade']:.1f}</div>
            <div class="stat-label">Average Grade</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{stats['average_attendance']:.1f}%</div>
            <div class="stat-label">Average Attendance</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{stats['pass_count']}</div>
            <div class="stat-label">Pass Count (≥60)</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{stats['fail_count']}</div>
            <div class="stat-label">Fail Count (<60)</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{stats['high_attendance']}</div>
            <div class="stat-label">High Attendance (≥80%)</div>
        </div>
    </div>
    
    <div style="margin-top: 30px; padding: 20px; background: #f9f9f9; border-radius: 5px;">
        <h3 style="margin-bottom: 15px;">Performance Summary</h3>
        <p style="margin-bottom: 10px;">
            <strong>Pass Rate:</strong> {stats['pass_count']}/{stats['total_students']} 
            ({(stats['pass_count']/stats['total_students']*100 if stats['total_students'] > 0 else 0):.1f}%)
        </p>
        <p style="margin-bottom: 10px;">
            <strong>Attendance Rate:</strong> {stats['average_attendance']:.1f}% average
        </p>
        <p>
            <strong>Grade Range:</strong> 0-100 (Average: {stats['average_grade']:.1f})
        </p>
    </div>
    """
    
    return render_base(content, 'Statistics')


def render_add_form(errors=None):
    """Render add student form"""
    error_html = ''
    if errors:
        error_html = '<div class="alert alert-error"><ul style="margin-left: 20px;">'
        for error in errors:
            error_html += f'<li>{html_escape(error)}</li>'
        error_html += '</ul></div>'
    
    content = f"""
    {error_html}
    
    <h2 style="margin-bottom: 20px;">Add New Student</h2>
    
    <form method="post" action="/add">
        <div class="form-group">
            <label for="roll_no">Roll Number *</label>
            <input type="text" id="roll_no" name="roll_no" required>
        </div>
        
        <div class="form-group">
            <label for="name">Name *</label>
            <input type="text" id="name" name="name" required>
        </div>
        
        <div class="form-group">
            <label for="grade">Grade (0-100) *</label>
            <input type="number" id="grade" name="grade" min="0" max="100" step="0.1" required>
        </div>
        
        <div class="form-group">
            <label for="attendance">Attendance (0-100) *</label>
            <input type="number" id="attendance" name="attendance" min="0" max="100" step="0.1" required>
        </div>
        
        <div class="form-group">
            <label>
                <input type="checkbox" name="fees_paid"> Fees Paid
            </label>
        </div>
        
        <div class="button-group">
            <button type="submit" class="btn btn-primary">Add Student</button>
            <a href="/students" class="btn btn-secondary">Cancel</a>
        </div>
    </form>
    """
    
    return render_base(content, 'Add Student')


def render_add_success(roll_no, name):
    """Render add success page"""
    content = f"""
    <div class="success-message">
        ✓ Student <strong>{html_escape(name)}</strong> (Roll: {html_escape(roll_no)}) added successfully!
    </div>
    
    <div class="button-group">
        <a href="/students" class="btn btn-primary">View All Students</a>
        <a href="/add" class="btn btn-secondary">Add Another</a>
    </div>
    """
    
    return render_base(content, 'Success')


def render_edit_form(roll_no, student, errors=None):
    """Render edit student form"""
    error_html = ''
    if errors:
        error_html = '<div class="alert alert-error"><ul style="margin-left: 20px;">'
        for error in errors:
            error_html += f'<li>{html_escape(error)}</li>'
        error_html += '</ul></div>'
    
    fees_checked = 'checked' if student.get('fees_paid') else ''
    
    content = f"""
    {error_html}
    
    <h2 style="margin-bottom: 20px;">Edit Student</h2>
    
    <form method="post" action="/edit">
        <input type="hidden" name="roll_no" value="{html_escape(roll_no)}">
        
        <div class="form-group">
            <label>Roll Number</label>
            <input type="text" value="{html_escape(roll_no)}" disabled style="background: #f5f5f5;">
        </div>
        
        <div class="form-group">
            <label for="name">Name *</label>
            <input type="text" id="name" name="name" value="{html_escape(student.get('name', ''))}" required>
        </div>
        
        <div class="form-group">
            <label for="grade">Grade (0-100) *</label>
            <input type="number" id="grade" name="grade" value="{student.get('grade', 0)}" min="0" max="100" step="0.1" required>
        </div>
        
        <div class="form-group">
            <label for="attendance">Attendance (0-100) *</label>
            <input type="number" id="attendance" name="attendance" value="{student.get('attendance', 0)}" min="0" max="100" step="0.1" required>
        </div>
        
        <div class="form-group">
            <label>
                <input type="checkbox" name="fees_paid" {fees_checked}> Fees Paid
            </label>
        </div>
        
        <div class="button-group">
            <button type="submit" class="btn btn-primary">Update Student</button>
            <a href="/students/{html_escape(roll_no)}" class="btn btn-secondary">Cancel</a>
        </div>
    </form>
    """
    
    return render_base(content, 'Edit Student')


def render_edit_success(roll_no, name):
    """Render edit success page"""
    content = f"""
    <div class="success-message">
        ✓ Student <strong>{html_escape(name)}</strong> updated successfully!
    </div>
    
    <div class="button-group">
        <a href="/students/{html_escape(roll_no)}" class="btn btn-primary">View Student</a>
        <a href="/students" class="btn btn-secondary">View All Students</a>
    </div>
    """
    
    return render_base(content, 'Success')


def render_student_detail(roll_no, student):
    """Render student details page"""
    fees_status = 'Paid' if student.get('fees_paid') else 'Pending'
    fees_badge = 'badge-success' if student.get('fees_paid') else 'badge-danger'
    
    grade = student.get('grade', 0)
    grade_badge = 'badge-success' if grade >= 60 else 'badge-danger'
    
    attendance = student.get('attendance', 0)
    att_badge = 'badge-success' if attendance >= 80 else 'badge-warning'
    
    content = f"""
    <h2 style="margin-bottom: 20px;">Student Details</h2>
    
    <div style="background: #f9f9f9; padding: 20px; border-radius: 5px; margin-bottom: 20px;">
        <p style="margin-bottom: 10px;"><strong>Roll Number:</strong> {html_escape(roll_no)}</p>
        <p style="margin-bottom: 10px;"><strong>Name:</strong> {student.get('name', 'N/A')}</p>
        <p style="margin-bottom: 10px;"><strong>Grade:</strong> <span class="badge {grade_badge}">{grade}</span></p>
        <p style="margin-bottom: 10px;"><strong>Attendance:</strong> <span class="badge {att_badge}">{attendance}%</span></p>
        <p style="margin-bottom: 10px;"><strong>Fees Status:</strong> <span class="badge {fees_badge}">{fees_status}</span></p>
        <p style="margin-bottom: 10px;"><strong>Added:</strong> {student.get('added_on', 'N/A')}</p>
        <p><strong>Updated:</strong> {student.get('updated_on', 'N/A')}</p>
    </div>
    
    <div class="button-group">
        <a href="/edit?roll_no={html_escape(roll_no)}" class="btn btn-primary">Edit</a>
        <a href="/delete/{html_escape(roll_no)}" class="btn btn-danger">Delete</a>
        <a href="/students" class="btn btn-secondary">Back</a>
    </div>
    """
    
    return render_base(content, f'Student {roll_no}')


def render_delete_confirm(roll_no, student):
    """Render delete confirmation page"""
    content = f"""
    <div class="alert alert-error" style="font-size: 16px; padding: 20px;">
        ⚠️ You are about to delete this student permanently!
    </div>
    
    <div style="background: #f9f9f9; padding: 20px; border-radius: 5px; margin-bottom: 30px;">
        <p style="margin-bottom: 10px;"><strong>Roll Number:</strong> {html_escape(roll_no)}</p>
        <p><strong>Name:</strong> {student.get('name', 'N/A')}</p>
    </div>
    
    <form method="post" action="/delete/{html_escape(roll_no)}" style="margin-bottom: 20px;">
        <div class="button-group">
            <button type="submit" class="btn btn-danger">Confirm Delete</button>
            <a href="/students/{html_escape(roll_no)}" class="btn btn-secondary">Cancel</a>
        </div>
    </form>
    """
    
    return render_base(content, 'Delete Confirmation')


def render_delete_success(roll_no, name):
    """Render delete success page"""
    content = f"""
    <div class="success-message">
        ✓ Student <strong>{html_escape(name)}</strong> (Roll: {html_escape(roll_no)}) deleted successfully!
    </div>
    
    <div class="button-group">
        <a href="/students" class="btn btn-primary">View All Students</a>
    </div>
    """
    
    return render_base(content, 'Deleted')


def render_error(message):
    """Render error page"""
    content = f"""
    <div class="alert alert-error" style="font-size: 16px; padding: 20px; margin-bottom: 20px;">
        ❌ Error: {html_escape(message)}
    </div>
    
    <div class="button-group">
        <a href="/" class="btn btn-primary">Go to Dashboard</a>
        <a href="/students" class="btn btn-secondary">View Students</a>
    </div>
    """
    
    return render_base(content, 'Error')
