from django.shortcuts import HttpResponse, render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import *
from .models import Classes
from .models import Assignments
from datetime import datetime, timedelta
import requests

modifyUser = True

def main(request):
    return render(request, "main.html", {'week': (datetime.now().date()) + timedelta(days=10), 'today': datetime.now().date(), 'courses': Classes.objects.filter(user=request.user), 'assignments': Assignments.objects.filter(course_id__user=request.user), 'isRow': Classes.objects.filter(user=request.user).first().isRow})

def completed(request):
    assignmentID = request.POST.get("assignment_id")
    assignment = Assignments.objects.get(key=assignmentID)
    if assignment.completed == False:
        assignment.completed = True
        assignment.save()
    else:
        assignment.completed = False
        assignment.save()
    return render(request, "flags/completedToggle.html", {'assignment': Assignments.objects.get(key=assignmentID), 'isRow': Classes.objects.filter(user=request.user).first().isRow})

def toggleView(request):
    isRow = request.POST.get("isRow")
    class_entries = Classes.objects.filter(user=request.user)
    if isRow == "true":
        for aclass in class_entries:
            aclass.isRow = True
            aclass.save()
    else:
        for aclass in class_entries:
            aclass.isRow = False
            aclass.save()
    return HttpResponse("")

def filter(request):
    class_entries = Classes.objects.filter(user=request.user)
    if not class_entries[0].filter:
        for aclass in class_entries:
            aclass.filter = True
            aclass.save()
        return render(request, "filter/true.html", {'week': (datetime.now().date()) + timedelta(days=10), 'today': datetime.now().date(), 'courses': Classes.objects.filter(user=request.user), 'assignments': Assignments.objects.filter(course_id__user=request.user)})
    else:
        for aclass in class_entries:
            aclass.filter = False
            aclass.save()
        return render(request, "filter/false.html", {'week': (datetime.now().date()) + timedelta(days=10), 'today': datetime.now().date(), 'courses': Classes.objects.filter(user=request.user), 'assignments': Assignments.objects.filter(course_id__user=request.user)})

def get_assignments_canvas(request, user_session):
    sessionCookies = {
        "canvas_session": user_session
    }
    classes = Classes.objects.filter(user=request.user)
    assignments = Assignments.objects
    assignments.filter(course_id__user=request.user).delete()
    for aclass in classes:
        assignData = requests.get(
            "https://canvas.liberty.edu/api/v1/courses/"
            + str(aclass.course_id)
            + "/assignments?per_page=100",
            cookies=sessionCookies, ).json()
        for assignment in assignData:
            curAssign = assignments.create(course_id=aclass)
            curAssign.name = assignment["name"]
            curAssign.type = assignment["submission_types"][0]
            curAssign.total_points = assignment["points_possible"]
            curAssign.url = assignment["html_url"]

            if assignment["due_at"] is None:
                curAssign.due = datetime.strptime("2006-01-26", "%Y-%m-%d").date()
            else:
                curAssign.due = datetime.strptime(str(assignment["due_at"])[:10], "%Y-%m-%d").date()

            curAssign.save()
    return HttpResponseRedirect("/accounts/dashboard/")

def get_classes_canvas(data, request, user_session):
    entries = Classes.objects
    entries.filter(user=request.user).delete()
    for course in data:
        course_id = course["id"]
        course_name = course["name"]
        if (entries.filter(user=request.user)).count() > 0:
            curUser = entries.create(user=request.user)
            curUser.name = course_name
            curUser.course_id = course_id
            curUser.save()
        else:
            curUser, created = Classes.objects.get_or_create(user=request.user)  # returns tuple of object (the actual entry) and created (a boolean). Thus, must split the tuple so only object gets retrieved.
            curUser.course_id = course_id
            curUser.name = course_name
            curUser.save()
    get_assignments_canvas(request, user_session)

def refresh(request):
    global modifyUser
    modifyUser = True
    return HttpResponseRedirect("/accounts/setup/")

def retrieve_data_canvas(user_session, request):
    sessionCookies = {
        "canvas_session": user_session
    }
    data = requests.get(
    "https://canvas.liberty.edu/api/v1/courses/",
        cookies=sessionCookies).json()
    get_classes_canvas(data, request, user_session)

def get_assignments_blackboard(request, user_session):
    sessionCookies = {
        "BbRouter": user_session
    }
    classes = Classes.objects.filter(user=request.user)
    assignments = Assignments.objects
    assignments.filter(course_id__user=request.user).delete()
    for aclass in classes:
        assignData = requests.get(
            "https://bb-csuohio.blackboard.com/learn/api/public/v2/courses/"
            + str(aclass.course_id)
            + "/gradebook/columns/",
            cookies=sessionCookies).json()["results"]
        print(assignData)
        for assignment in assignData[1:]: # first (0) is overall grade, so go one more than that
            curAssign = assignments.create(course_id=aclass)
            curAssign.name = assignment["name"]
            try:
                curAssign.type = assignment["scoreProviderHandle"]
            except KeyError:
                curAssign.type = "resource/x-bb-assessment"
            curAssign.total_points = assignment["score"]["possible"]

            try:
                curAssign.due = datetime.strptime(str(assignment["grading"]["due"])[:10], "%Y-%m-%d").date()
            except KeyError:
                curAssign.due = datetime.strptime("2006-01-26", "%Y-%m-%d").date()
            curAssign.save()
    return HttpResponseRedirect("/accounts/dashboard/")

def get_classes_blackboard(data, request, user_session):
    sessionCookies = {
        "BbRouter": user_session
    }
    entries = Classes.objects
    entries.filter(user=request.user).delete()

    for course in data:
        course_id = course["courseId"]
        course_name = requests.get("https://bb-csuohio.blackboard.com/learn/api/public/v1/courses/" + str(course_id),
                                   cookies=sessionCookies).json()["name"]
        if (entries.filter(user=request.user)).count() > 0:
            curUser = entries.create(user=request.user)
            curUser.name = course_name
            curUser.course_id = course_id
            curUser.save()
        else:
            curUser, created = Classes.objects.get_or_create(user=request.user)  # returns tuple of object (the actual entry) and created (a boolean). Thus, must split the tuple so only object gets retrieved.
            curUser.course_id = course_id
            curUser.name = course_name
            curUser.save()
    get_assignments_blackboard(request, user_session)

def retrieve_data_blackboard(user_session, request):
    sessionCookies = {
        "BbRouter": user_session
    }
    data = requests.get(
    "https://bb-csuohio.blackboard.com/learn/api/public/v1/users/me/courses",
        cookies=sessionCookies).json()["results"]
    get_classes_blackboard(data, request, user_session)

@login_required

def landing(request):
    global modifyUser
    if not modifyUser:
        main(request)
        return HttpResponseRedirect("/accounts/dashboard/")
    elif request.method == 'POST':
        modifyUser = False
        LMS = request.POST.get('LMS')
        session_id = request.POST.get('session_id', '')
        if LMS == 'canvas':
            retrieve_data_canvas(session_id, request)
        if LMS == 'blackboard':
            retrieve_data_blackboard(session_id, request)
    return render(request, "landing.html")

def addAssignment(request):
    if request.method == 'POST':
        courseId = request.POST.get('course')
        assiName = request.POST.get('assiName')
        due = request.POST.get('duedate')
        newAssignment = Assignments.objects.create(course_id=Classes.objects.get(key=courseId))
        newAssignment.name = assiName
        newAssignment.due = due
        newAssignment.save()
        return HttpResponseRedirect("/accounts/dashboard/")
# Create your views here.