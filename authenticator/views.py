from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from .models import CustomUser, Student, Subject, Results
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Avg, Sum
from PIL import Image
from django.core.files.base import ContentFile
from django.http import HttpResponse, Http404

from io import BytesIO
import segno
import hashlib


# Create your views here.
def is_staff_user(user):
    return user.is_staff


def compress_image(image):
    img = Image.open(image)
    output = BytesIO()
    quality = 85

    img.save(output, format='JPEG', quality=quality)

    while output.tell() > 100 * 1024 and quality > 0:
        output = BytesIO()
        quality -= 5
        img.save(output, format='JPEG', quality=quality)

    output.seek(0)
    return output


def registration(request):
    all_subjects = Subject.objects.all()

    if request.method == "POST":
        photo = request.FILES.get('photo')  # Use FILES to get uploaded files

        # Compress the image to around 100KB
        compressed_photo = compress_image(photo)

        # Create a File object from the compressed image data
        compressed_photo_file = ContentFile(compressed_photo.getvalue())

        name = request.POST['name']
        phone = request.POST['phone']
        form = request.POST['form']
        number = request.POST['number']
        selected_subjects = request.POST.getlist('subjects')

        student = Student.objects.create(  # Corrected 'object' to 'objects'
            name=name,
            photo=compressed_photo_file,
            phone=phone,
            form=form,
            student_no=number
        )

        # Add selected subjects to the student's registered_subjects
        student.registered_subject.set(selected_subjects)

        return redirect('success')  # Redirect to a success page (assuming you have a URL pattern named 'success')

    else:
        context = {
            'all_subjects': all_subjects
        }

    return render(request, 'authenticator/register.html', context)


def success(request):
    return render(request, "authenticator/success.html")


def index(request):
    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('entry')
        else:
            context = {'error': 'Invalid username or password'}
            return render(request, 'authenticator/index.html', context)

    return render(request, 'authenticator/index.html')


@login_required
def entry(request):
    if request.user.is_authenticated:

        # Check if the user is an admin
        if request.user.is_staff:
            # Redirect to another page for admins
            return redirect('results')

        subject = request.user.subject
        # students = Student.objects.all()
        user_subject = Subject.objects.get(name=subject)
        registered_students = Student.objects.filter(registered_subject=user_subject, ).order_by('name')

        # Get results for the registered students
        results = Results.objects.filter(student__in=registered_students, subject=user_subject)

        # Check if each registered student has existing results. If not, create new results with zeros.
        for student in registered_students:

            if not results.filter(student=student).exists():
                Results.objects.create(
                    student=student,
                    subject=user_subject,
                    cat1=0,
                    cat2=0,
                    exam=0,
                    total=0,
                    grade="F",
                    remark="None",
                )

        # Get results for the registered students
        results = Results.objects.filter(student__in=registered_students, subject=user_subject)

        context = {
            'name': request.user.username,
            'subject': subject,
            'students': registered_students,
            'results': results,
        }
        return render(request, 'authenticator/entry.html', context)
    else:
        return redirect('index')  # Redirect to the login page if the user is not authenticated


# logout user and clear auth session
def logout_view(request):
    logout(request)
    return redirect('index')


# save and compute score to database
# encapsulated grading function
def calculate_grade_remark(score):
    if score <= 39:
        return "F", "FAIL"
    elif 40 <= score <= 44:
        return "E", "PASS"
    elif 45 <= score <= 49:
        return "D", "CREDIT"
    elif 50 <= score <= 59:
        return "C", "GOOD"
    elif 60 <= score <= 69:
        return "B", "VERY GOOD"
    else:
        return "A", "EXCELLENT"


def calculate_grade_and_coord_remark(score):
    if score <= 39:
        return "F", "FAIL", "Poor result, you failed. Ensure you work very hard next Semester."
    elif 40 <= score <= 44:
        return "E", "PASS", "Pass result. Work very hard next Semester."
    elif 45 <= score <= 49:
        return "D", "CREDIT", "Credit result. Work harder next Semester. "
    elif 50 <= score <= 59:
        return "C", "GOOD", "Good result. Work hard next Semester."
    elif 60 <= score <= 69:
        return "B", "VERY GOOD", "Very Good result. You can do better next Semester."
    else:
        return "A", "EXCELLENT", "Excellent result. Maintain the momentum."


def result_processor(request):
    # extract data from form
    if request.method == 'POST':

        subject = request.user.subject
        user_subject = Subject.objects.get(name=subject)

        # Retrieve the registered students for the subject
        registered_students = Student.objects.filter(registered_subject=user_subject)

        # Update the scores for each student
        for student in registered_students:
            # Data extraction
            # Get the unique field names for each student
            cat1_field_name = f"CAT1_{student.id}"
            cat2_field_name = f"CAT2_{student.id}"
            exam_field_name = f"EXAM_{student.id}"

            # Get the values from the POST data for each student
            cat1 = int(request.POST.get(cat1_field_name, 0))
            cat2 = int(request.POST.get(cat2_field_name, 0))
            exam = int(request.POST.get(exam_field_name, 0))

            # Processing
            total = cat1 + cat2 + exam

            # Grading
            grade, remarks = calculate_grade_remark(total)

            # Updating the database
            # Check if the student already has a record for this subject
            result, created = Results.objects.get_or_create(student=student, subject=user_subject)

            # Update the scores
            result.cat1 = cat1
            result.cat2 = cat2
            result.exam = exam
            result.total = total
            result.grade = grade
            result.remark = remarks

            # Save the changes
            result.save()

            # Process the student result summary statistics
            all_results = Results.objects.filter(student=student)

            total_score = all_results.aggregate(Sum('total'))['total__sum']
            derived_total_score = total_score / all_results.count()

            avg = total_score / all_results.count()

            student.avg = avg
            student.total_score = total_score
            student.total_grade, student.total_remark, student.coordinator_remark = calculate_grade_and_coord_remark(
                derived_total_score)

            # Calculate hash of student's result data
            result_data = f"{student.id}_{student.total_score}_{student.total_grade}".encode('utf-8')
            result_hash = hashlib.sha256(result_data).hexdigest()

            text_template = f"""
            {student.name}
            {student.total_score}
            {result_hash}
                            """

            # Create QR code using segno
            qr = segno.make(text_template)
            qr.save(f'media/{student.id}_qr.png', scale=5)

            # Save the QR code image path to the student's data
            student.qr_code = f'media/{student.id}_qr.png'

            student.save()

        return redirect('entry')

    else:
        return render(request, 'authenticator/entry.html')


def verify_hash(hash_to_verify):
    all_students = Student.objects.all()

    for student in all_students:
        result_data = f"{student.id}_{student.total_score}_{student.total_grade}".encode('utf-8')
        calculated_hash = hashlib.sha256(result_data).hexdigest()
        if calculated_hash == hash_to_verify:
            return student
    return None


@login_required
@user_passes_test(is_staff_user)
def admin_viewer(request):
    all_students = Student.objects.all().order_by('name')

    if request.method == 'POST':
        search = request.POST.get('search')

        if search:
            filtered_students = all_students.filter(name__icontains=search)
            context = {
                'all_students': filtered_students,
            }

            return render(request, 'authenticator/results.html', context)

    context = {
        'all_students': all_students,
        'name': request.user.username,
    }
    return render(request, 'authenticator/results.html', context)


@login_required
@user_passes_test(is_staff_user)
def result_viewer(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    results = Results.objects.filter(student=student)

    context = {
        'student': student,
        'results': results,
    }

    return render(request, 'authenticator/viewer.html', context)


@login_required
@user_passes_test(is_staff_user)
def masterdatasheet(request):
    # Get your list of students and subjects
    all_students = Student.objects.all().order_by('name')
    subjects = Subject.objects.all().order_by('name')
    results = Results.objects.all()

    context = {
        'all_students': all_students,
        'subjects': subjects,
        'results': results,
    }

    return render(request, 'authenticator/master.html', context)


@login_required
@user_passes_test(is_staff_user)
def export(request):
    all_students = Student.objects.all().order_by('name')
    results = Results.objects.all()

    context = {
        'all_students': all_students,
        'results': results,
    }

    return render(request, 'authenticator/export.html', context)


def error(request, exception):
    return render(request, 'authenticator/error.html')


@login_required
def verify(request):
    all_students = Student.objects.all().order_by('name')
    student_match = None

    if request.method == 'POST':
        puzzle = request.POST.get('puzzle')

        if puzzle:
            student_match = verify_hash(puzzle)

    context = {
        'all_students': all_students,
        'student_match': student_match,

    }

    return render(request, 'authenticator/verify.html', context)


def check_result(request):
    if request.method == 'POST':
        check = request.POST.get('check')

        try:
            student = get_object_or_404(Student, student_no=check)
            results = Results.objects.filter(student=student)

            context = {
                'student': student,
                'results': results,
            }

            return render(request, 'authenticator/viewer.html', context)

        except Http404:
            # Student not found, return an error message
            error_message = "We cant find that student here!!."
            return render(request, 'authenticator/checker.html', {'error': error_message})

    else:
        return render(request, 'authenticator/checker.html')