import os.path

import django.conf as conf
from django.contrib.auth import logout
from django.contrib.auth import login as org_login
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import connection, connections
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
# from django.core import serializers
# from .models import ProjectInfo
from tool import models
import json
from .forms import LoginForm
import quesadiya as q
# from quesadiya.django_tool.manage import projectName
from django.http import JsonResponse
import datetime
from django.views.decorators.csrf import csrf_exempt
from django.db.utils import DEFAULT_DB_ALIAS, load_backend
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
# def create_connection(alias=DEFAULT_DB_ALIAS):
#     database_root = os.path.join(q.get_projects_path(), "admin.db")
#     # connections.ensure_defaults(database_root)
#     # connections.prepare_test_settings(database_root)
#     db = connections.databases[database_root]
#     backend = load_backend(db['ENGINE'])
#     return backend.DatabaseWrapper(db, database_root)
from django.contrib.auth.backends import ModelBackend
from quesadiya.db.hasher import PH


# def error(request, exception):
#     logout(request)
#     return render(request, "registration/login.html")


class CustomAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None):
        projectName = request.session['projectName']
        try:
            user = User.objects.using(
                projectName).get(username=username)
        except User.DoesNotExist:
            user = None
            print('no user')
            return user
        check_password = PH.verify(user.password, password)
        # if True and self.user_can_authenticate(user):
        # PH.hash(new_password)
        if check_password:
            return user
        return None


def create_connection(project_name):
    """Create new database connection."""
    db = conf.settings.DATABASES["default"].copy()
    db['NAME'] = os.path.join(q.get_projects_path(),
                              project_name, "project.db")
    conf.settings.DATABASES[project_name] = db


def login(request):
    # print("project Name", os.environ.get("projectName"))
    if request.method == "POST":
        project = json.loads(request.POST.get(
            'selected_project').replace("\'", "\""))
        projectName = project.get("project_name")
        projectId = str(project["project_id"])
        userName = request.POST.get('username')
        password = request.POST.get('password')
        request.session['projectName'] = projectName
        request.session['projectId'] = projectId
        # swapDB(projectName)
        create_connection(projectName)
        print(projectName, " : ", userName, " : ", password, " : ",
              projectId, " : ", checkProjectUser(userName, projectId))
        md = CustomAuthBackend()
        user = md.authenticate(
            request, username=userName, password=password)
        # request.user = user
        # md = ModelBackend()
        # user = md.authenticate(
        #     request, username=userName, password=password)
        print(user)
        if user is not None:
            org_login(request, user, 'tool.views.CustomAuthBackend')
            # print(request.user.is_authenticated)
            # print(request.user)
            user = {'username': user.username,
                    'is_superuser': user.is_superuser}
            request.session['user'] = user
            # return HttpResponseRedirect("/")
            # return ProjectInfo(request)
            if user['is_superuser'] == 1:
                print("ap")
                return redirect("AssignCooperator")
            else:
                return redirect("home")
    logout(request)
    return render(request, "registration/login.html")
    # swapDB("t")
    # request.session['projectName'] = "t"
    # return redirect("home")


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def checkProjectUser(username, projectId):
    with connections['admin'].cursor() as cursor:
        cursor.execute(
            "SELECT * from project_user where username='"+username+"' and projectId='"+projectId+"'")
        data = cursor.fetchall()
    return False if not data else True


def swapDB(projectName):
    if(projectName == "admin"):
        path = conf.settings.DATABASES['admin']['NAME']
    else:
        path = os.path.join(q.get_projects_path(), projectName, "project.db")
    print("old db :", conf.settings.DATABASES['project']['NAME'])
    conf.settings.DATABASES['project']['NAME'] = path
    print("new db :", conf.settings.DATABASES['project']['NAME'])


def getUnfinish(p_name):
    with connections[p_name].cursor() as cursor:
        cursor.execute(
            "select * from Triplet_Dataset WHERE status='unfinished' or status='discarded' ORDER by time_changed LIMIT 1")
        data = dictfetchall(cursor)
        cursor.execute("UPDATE triplet_dataset SET time_changed=strftime('%Y-%m-%d %H:%M:%S.%f','now'), status = 'discarded' WHERE anchor_sample_id='" +
                       data[0].get("anchor_sample_id")+"'")
    return data
    # with connection.cursor() as cursor:
    #     cursor.execute(
    #         "select candidate_sample_id, sample_body, sample_title from candidate_groups INNER join sample_text on sample_text.sample_id = candidate_groups.candidate_sample_id where(candidate_group_id='"+candidate_group_id+"')")
    #     datas = dictfetchall(cursor)
    # return datas


def getSampleData(p_name, sample_id):
    with connections[p_name].cursor() as cursor:
        cursor.execute(
            "select * from sample_text where sample_id='"+sample_id+"'")
        data = dictfetchall(cursor)
    return data


def getCandidateGroup(p_name, candidate_group_id):
    with connections[p_name].cursor() as cursor:
        cursor.execute(
            "select candidate_sample_id, sample_body, sample_title from candidate_groups INNER join sample_text on sample_text.sample_id = candidate_groups.candidate_sample_id where(candidate_group_id='"+candidate_group_id+"')")
        data = dictfetchall(cursor)
    return data


def getProjectUser(p_name):
    with connections['admin'].cursor() as cursor:
        cursor.execute(
            "SELECT username from project_user where projectId='"+p_name+"'")
        data = [item[0] for item in cursor.fetchall()]
    return data


def getInfo(p_name):
    with connections['admin'].cursor() as cursor:
        cursor.execute(
            "select project_name, project_description from projects where project_name='"+p_name+"'")
        data = dictfetchall(cursor)
    data[0]['finished'] = 0
    data[0]['unfinished'] = 0
    data[0]['discarded'] = 0
    data[0]['total'] = 0
    return data
    # return models.Projects.objects.using(
    #     'admin').filter(project_name=p_name)
    # .only("project_name", "project_description")


def datetimeDefault(dt):
    if isinstance(dt, (datetime.date, datetime.datetime)):
        return dt.isoformat()


def updatePositiveAnchor(p_name, anchor_sample_id, positive_sample_id):
    with connections[p_name].cursor() as cursor:
        cursor.execute(
            "UPDATE triplet_dataset SET positive_sample_id='"+positive_sample_id+"', status = 'finished' WHERE anchor_sample_id='"+anchor_sample_id+"'")


def getStatus(p_name):
    with connections[p_name].cursor() as cursor:
        cursor.execute(
            "select status, count(*) from Triplet_dataset GROUP by status")
        data = cursor.fetchall()
    print(type(data))
    # data = json.dumps(data)
    total = 0
    for value in data:
        total += value[1]
    data.append(tuple(('total', total)))
    dict(data)
    return data


@ csrf_exempt
def nextAnchor(request):
    if request.method == 'POST':
        projectName = request.session['projectName']
        anchor_sample_id = request.POST.get('anchor_id')
        with connections[projectName].cursor() as cursor:
            cursor.execute(
                "UPDATE triplet_dataset SET time_changed=strftime('%Y-%m-%d %H:%M:%S.%f','now'), status = 'discarded' WHERE anchor_sample_id='"+anchor_sample_id+"'")
        return ProjectInfo(request)


@ csrf_exempt
def updateAnchor(request):
    if request.method == 'POST':
        projectName = request.session['projectName']
        anchor_id = request.POST.get('anchor_id')
        positive_anchor_id = request.POST.get('positive_anchor_id')
        print(anchor_id, "+ :", positive_anchor_id)
        updatePositiveAnchor(projectName, anchor_id, positive_anchor_id)
        return ProjectInfo(request)


def ProjectInfo(request):
    # print(request.session['projectName'])
    print(request.user.is_authenticated)
    print(request.user)
    if 'user' in request.session and request.session['user']['is_superuser'] == 0:
        #     print("yess")
        # if(request.user.is_authenticated):
        user = request.session['user']
        projectName = request.session['projectName']
        projectId = request.session['projectId']
        status = getStatus(projectName)
        projectUser = {"participants": getProjectUser(projectId)}
        infos = getInfo(projectName)
        infos[0].update(status)
        infos[0].update(projectUser)
        if(infos[0]["finished"] == infos[0]["total"]):
            return render(request, "home.html", {"infos": infos})
        unfinish_anchor = getUnfinish(projectName)
        anchor_data = getSampleData(projectName,
                                    unfinish_anchor[0].get("anchor_sample_id"))
        candidate_groups = getCandidateGroup(projectName,
                                             unfinish_anchor[0].get("candidate_group_id"))
        context_dict = {'user': user, 'infos': infos, 'anchor_data': anchor_data,
                        'candidate_groups': candidate_groups}
        return render(request, "home.html", context_dict)
    logout(request)
    return render(request, "registration/login.html")


# def AdminPanel(request):
#     print("welcome from admin panel")
#     if 'user' in request.session:
#         user = request.session['user']
#         print(user)
#         projectName = request.session['projectName']
#         projectId = request.session['projectId']
#         with connections[projectName].cursor() as cursor:
#             cursor.execute(
#                 "SELECT anchor_sample_id, status, username from triplet_dataset")
#             anchors = dictfetchall(cursor)
#         # context_dict = {'user': user, 'infos': infos, 'anchor_data': anchor_data,
#         #                 'candidate_groups': candidate_groups}
#         context_dict = {'anchors': anchors}
#         return render(request, "admin_panel.html", context_dict)
#     logout(request)
#     return render(request, "registration/login.html")


def AssignCooperator(request):
    print("welcome from project panel")
    if 'user' in request.session and request.session['user']['is_superuser'] == 1:
        user = request.session['user']
        print(user)
        projectName = request.session['projectName']
        projectId = request.session['projectId']
        with connections[projectName].cursor() as cursor:
            cursor.execute(
                "SELECT anchor_sample_id, status, username from triplet_dataset")
            anchors = dictfetchall(cursor)
        # context_dict = {'user': user, 'infos': infos, 'anchor_data': anchor_data,
        #                 'candidate_groups': candidate_groups}
        context_dict = {'anchors': anchors}
        return render(request, "assign_cooperator.html", context_dict)
    logout(request)
    return render(request, "registration/login.html")


@ csrf_exempt
def updateCooperator(request):
    if request.method == 'POST':
        projectName = request.session['projectName']
        anchor_id = request.POST.get('anchor_id')
        username = request.POST.get('cooperator')
        print(anchor_id, "+ :", username)
        with connections[projectName].cursor() as cursor:
            cursor.execute("UPDATE triplet_dataset SET username='" +
                           username+"' WHERE anchor_sample_id='"+anchor_id + "'")
        return AssignCooperator(request)


def CooperatorStatus(request):
    print("welcome from CooperatorStatus")
    if 'user' in request.session and request.session['user']['is_superuser'] == 1:
        user = request.session['user']
        print(user)
        projectName = request.session['projectName']
        # projectId = request.session['projectId']
        with connections[projectName].cursor() as cursor:
            cursor.execute(
                "SELECT au.username,(SELECT count(status) from triplet_dataset where username=au.username and status='discarded') as discarded,(SELECT count(status) from triplet_dataset where username=au.username and status='finished') as finished,count(td.anchor_sample_id) as assigned from auth_user as au left outer join triplet_dataset as td on au.username = td.username where au.is_superuser = 0 GROUP by au.username,discarded,finished")
            statuses = dictfetchall(cursor)
        # context_dict = {'user': user, 'infos': infos, 'anchor_data': anchor_data,
        #                 'candidate_groups': candidate_groups}
        context_dict = {'statuses': statuses}
        return render(request, "cooperator_status.html", context_dict)
    logout(request)
    return render(request, "registration/login.html")


def EditCooperator(request):
    if 'user' in request.session and request.session['user']['is_superuser'] == 1:
        user = request.session['user']
        print(user)
        projectName = request.session['projectName']
        # projectId = request.session['projectId']
        with connections[projectName].cursor() as cursor:
            cursor.execute(
                "select id,username,is_superuser as status,last_login from auth_user")
            users = dictfetchall(cursor)
        # context_dict = {'user': user, 'infos': infos, 'anchor_data': anchor_data,
        #                 'candidate_groups': candidate_groups}
        context_dict = {'users': users}
        return render(request, "edit_cooperator.html", context_dict)
    logout(request)
    return render(request, "registration/login.html")


@ csrf_exempt
def updateUser(request):
    if request.method == 'POST':
        projectName = request.session['projectName']
        id = request.POST.get('id')
        username = request.POST.get('username')
        password = request.POST.get('password')
        status = request.POST.get('status')
        act = request.POST.get('act')
        # print(id, " ", username, " ", password, " ", status)
        password = PH.hash(password)
        print(password)
        status = 0 if status.lower() == 'cooperator' else 1
        if act == "0":
            with connections[projectName].cursor() as cursor:
                cursor.execute("UPDATE auth_user SET username='"+username+"',password='" +
                               str(password)+"',is_superuser='"+str(status)+"' WHERE id='"+id+"'")
        elif act == "1":
            with connections[projectName].cursor() as cursor:
                cursor.execute("INSERT INTO auth_user (id, password, is_superuser, username, last_name, email, is_staff, is_active,date_joined, first_name) VALUES ('" +
                               str(id)+"', '"+password+"', '"+str(status)+"', '"+username+"', ' ', ' ', '1', '0', strftime('%Y-%m-%d %H:%M:%S.%f','now'), ' ')")
        return EditCooperator(request)
