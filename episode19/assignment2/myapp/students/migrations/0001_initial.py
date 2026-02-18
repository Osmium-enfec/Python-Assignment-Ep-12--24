# Generated migration for Episode 19 Assignment 2

from django.db import migrations, models
import django.db.models.deletion
import django.core.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('code', models.CharField(max_length=10, unique=True)),
                ('head', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=20)),
            ],
            options={
                'verbose_name_plural': 'Departments',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('level', models.IntegerField(choices=[(100, 'Introductory'), (200, 'Intermediate'), (300, 'Advanced'), (400, 'Graduate')], default=100)),
                ('credits', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(4)])),
                ('description', models.TextField(blank=True)),
                ('is_active', models.BooleanField(default=True)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='students.department')),
            ],
            options={
                'verbose_name_plural': 'Courses',
                'ordering': ['code'],
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('roll_no', models.CharField(max_length=20, unique=True)),
                ('date_of_birth', models.DateField()),
                ('phone', models.CharField(max_length=20)),
                ('status', models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive'), ('graduated', 'Graduated'), ('suspended', 'Suspended')], default='active', max_length=15)),
                ('gpa', models.DecimalField(decimal_places=2, default=0.0, max_digits=3)),
                ('admission_date', models.DateField()),
                ('is_scholarship_holder', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='students.department')),
            ],
            options={
                'verbose_name_plural': 'Students',
                'ordering': ['-admission_date'],
                'permissions': [('can_export_students', 'Can export student list'), ('can_view_gpa', 'Can view GPA information')],
            },
        ),
        migrations.CreateModel(
            name='Enrollment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semester', models.CharField(choices=[('fall', 'Fall'), ('spring', 'Spring'), ('summer', 'Summer')], max_length=10)),
                ('year', models.IntegerField()),
                ('score', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('grade', models.CharField(blank=True, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('F', 'F'), ('I', 'Incomplete')], max_length=2, null=True)),
                ('enrollment_date', models.DateTimeField(auto_now_add=True)),
                ('is_completed', models.BooleanField(default=False)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='students.course')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='students.student')),
            ],
            options={
                'verbose_name_plural': 'Enrollments',
                'ordering': ['-year', '-semester'],
                'unique_together': {('student', 'course', 'semester', 'year')},
            },
        ),
    ]
