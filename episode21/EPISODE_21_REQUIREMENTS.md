# Episode 21: Django Forms and Add Student Functionality

**Concepts:** Django Forms, ModelForm, Form Widgets, Form Validation, GET/POST Handling, CSRF Protection, Bootstrap Form Integration, Messages Framework, Form Rendering, Custom Validation

**Total Topics:** 80 (40 per assignment)

---

## Assignment 1: Form Fundamentals and Setup (40 Topics)

### A1.1: Django Forms Module (10 topics)
1. Django Forms Module
2. ModelForm Class
3. Form Meta Class
4. Model to Form Conversion
5. Automatic Field Generation
6. Widget System in Django Forms
7. TextInput Widget
8. EmailInput Widget
9. DateInput Widget
10. CheckboxInput Widget

### A1.2: Form Fields and Widgets (10 topics)
11. Select Widget
12. Textarea Widget
13. Widget Attributes and Classes
14. Form Field Types
15. CharField in Forms
16. EmailField in Forms
17. DateField in Forms
18. BooleanField in Forms
19. ChoiceField in Forms
20. IntegerField in Forms

### A1.3: Form Customization (10 topics)
21. Field Labels and Labels Dictionary
22. Form Help Text
23. Form Error Messages
24. Custom Error Messages
25. Form Validation
26. is_valid() Method
27. cleaned_data Dictionary
28. Field Cleaning Methods
29. clean_email() Custom Validation
30. clean_phone() Custom Validation

### A1.4: GET/POST and Form Submission (10 topics)
31. GET Request Handling
32. POST Request Handling
33. request.method Check
34. GET and POST Differentiation
35. Creating Blank Form Instance
36. Creating Form with POST Data
37. Form Submission Processing
38. Template Form Rendering
39. CSRF Token Security
40. {% csrf_token %} Tag

**Skills:** ModelForm creation, widget configuration, field customization, basic validation, request method handling

---

## Assignment 2: Advanced Validation and User Feedback (40 Topics)

### A2.1: Advanced Validation (10 topics)
41. CSRF Protection in POST
42. Form-Level Validation
43. clean() Method in Forms
44. ValidationError Exception
45. Cross-Field Validation
46. Raising ValidationError
47. Unique Email Validation
48. Database Lookup Validation
49. Conditional Field Exclusion
50. Form Save Method

### A2.2: Form Saving and Instance Handling (10 topics)
51. Form Commit Parameter
52. save() without Commit
53. Modifying Data Before Save
54. Form HTML Generation
55. {{ form.field }} Rendering
56. {{ form.field.label }} Rendering
57. {{ form.field.errors }} Rendering
58. Field Error Display
59. Non-Field Errors Display
60. Bootstrap Form Integration

### A2.3: Styling and Feedback (10 topics)
61. Form Control Classes
62. Form Feedback Classes
63. Alert Bootstrap Component
64. Error Message Styling
65. Success Message Styling
66. View Context Dictionary
67. Passing Form to Template
68. Template Context Variables
69. URL Routing for Forms
70. URL name Parameter

### A2.4: Routing and Messages Framework (10 topics)
71. {% url %} Template Tag
72. Redirect Function
73. Redirect After Success
74. messages Framework
75. messages.success() Function
76. messages.error() Function
77. Message Display in Templates
78. Form Edit Pattern
79. Instance in Form Constructor
80. Update vs Add Operations

**Skills:** Form-level validation, save operations, Bootstrap styling, CSRF protection, messages framework, edit patterns
