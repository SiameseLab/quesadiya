import os.path

import django.conf as conf
from django.contrib.auth import authenticate, logout
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


def login(request):
    # print("project Name", os.environ.get("projectName"))
    # if request.method == "POST":
    #     projectName = request.POST.get('selected_project')
    #     userName = request.POST.get('username')
    #     password = request.POST.get('password')
    #     request.session['projectName'] = projectName
    #     # database = os.path.normpath(os.path.abspath(__file__) + os.sep + os.pardir + os.sep + os.pardir + os.sep +
    #     #                             os.pardir + os.sep + "/projects" + os.sep + projectName + os.sep + "project.db")
    #     swapDB(projectName)
    #     print(projectName, " : ", userName, " : ", password)
    #     user = authenticate(username=userName, password=password)
    #     print(user)
    #     if user is not None:
    #         org_login(request, user)
    #         return redirect("home")
    # logout(request)
    # swapDB("admin")
    # return render(request, "registration/login.html")
    request.session['projectName'] = "t"
    return redirect("home")


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def swapDB(projectName):
    if("admin"):
        path = conf.settings.DATABASES['admin']['NAME']
    else:
        path = os.path.join(q.get_projects_path(), projectName, "project.db")
    print("old db :", conf.settings.DATABASES['default']['NAME'])
    conf.settings.DATABASES['default']['NAME'] = path
    print("new db :", conf.settings.DATABASES['default']['NAME'])


def getUnfinish():
    with connection.cursor() as cursor:
        cursor.execute(
            "select * from Triplet_Dataset WHERE status='unfinished' LIMIT 1")
        datas = dictfetchall(cursor)
    return datas
    # with connection.cursor() as cursor:
    #     cursor.execute(
    #         "select candidate_sample_id, sample_body, sample_title from candidate_groups INNER join sample_text on sample_text.sample_id = candidate_groups.candidate_sample_id where(candidate_group_id='"+candidate_group_id+"')")
    #     datas = dictfetchall(cursor)
    # return datas


def getSampleData(sample_id):
    with connection.cursor() as cursor:
        cursor.execute(
            "select * from sample_text where sample_id='"+sample_id+"'")
        data = dictfetchall(cursor)
    return data


def getCandidateGroup(candidate_group_id):
    with connection.cursor() as cursor:
        cursor.execute(
            "select candidate_sample_id, sample_body, sample_title from candidate_groups INNER join sample_text on sample_text.sample_id = candidate_groups.candidate_sample_id where(candidate_group_id='"+candidate_group_id+"')")
        datas = dictfetchall(cursor)
    return datas


def getInfo(p_name):
    with connections['admin'].cursor() as cursor:
        cursor.execute(
            "select project_name, project_description from projects where project_name='"+p_name+"'")
        datas = dictfetchall(cursor)
    return datas
    # return models.Projects.objects.using(
    #     'admin').filter(project_name=p_name)
    # .only("project_name", "project_description")


def datetimeDefault(dt):
    if isinstance(dt, (datetime.date, datetime.datetime)):
        return dt.isoformat()


def updatePositiveAnchor(anchor_sample_id, positive_sample_id):
    with connection.cursor() as cursor:
        cursor.execute(
            "UPDATE triplet_dataset SET positive_sample_id='"+positive_sample_id+"', status = 'finished' WHERE anchor_sample_id='"+anchor_sample_id+"'")


@csrf_exempt
def updateAnchor(request):

    if request.method == 'POST':
        anchor_id = request.POST.get('anchor_id')
        positive_anchor_id = request.POST.get('positive_anchor_id')
        print(anchor_id, "+ :", positive_anchor_id)
        updatePositiveAnchor(anchor_id, positive_anchor_id)
        # infos = getInfo("t")
        # unfinish_anchor = getUnfinish()
        # anchor_data = getSampleData(
        #     unfinish_anchor[0].get("anchor_sample_id"))
        # candidate_groups = getCandidateGroup(
        #     unfinish_anchor[0].get("candidate_group_id"))
        # context_dict = {'infos': infos, 'anchor_data': anchor_data,
        #                 'candidate_groups': candidate_groups}
        # return JsonResponse(context_dict, safe=False)
        return ProjectInfo(request)


def ProjectInfo(request):

    # projectName = request.session['projectName']
    # print("db :", conf.settings.DATABASES['default']['NAME'])
    # datas = models.TripletDataset.objects.all()
    # print(datas)
    # user = authenticate(username="test", password="test")
    projectName = request.session['projectName']
    print("project Name : ", projectName)
    if(conf.settings.DATABASES['default']['NAME'] != conf.settings.DATABASES['admin']['NAME']):
        infos = getInfo(projectName)
        unfinish_anchor = getUnfinish()
        anchor_data = getSampleData(
            unfinish_anchor[0].get("anchor_sample_id"))
        print(type(anchor_data))
        candidate_groups = getCandidateGroup(
            unfinish_anchor[0].get("candidate_group_id"))
    context_dict = {'infos': infos, 'anchor_data': anchor_data,
                    'candidate_groups': candidate_groups}
    # print(context_dict)
    # return JsonResponse(context_dict)
    return render(request, "home.html", context_dict)

    # infos = models.Projects.objects.using(
    #     'admin').filter(project_name=projectName).values("project_name", "project_description")

    # if(conf.settings.DATABASES['default']['NAME'] != conf.settings.DATABASES['admin']['NAME']):
    #     with connection.cursor() as cursor:
    #         cursor.execute("select * from Triplet_Dataset")
    #         datasets = dictfetchall(cursor)
    #     print(datasets)
    #     candidate_group = {}
    #     for data in datasets:
    #         with connection.cursor() as cursor:
    #             cursor.execute(
    #                 "select candidate_sample_id, sample_body, sample_title from candidate_groups INNER join sample_text on sample_text.sample_id = candidate_groups.candidate_sample_id where(candidate_group_id='"+data["candidate_group_id"]+"')")
    #             group = dictfetchall(cursor)
    #         candidate_group[data["candidate_group_id"]] = group
    #     return HttpResponse(json.dumps(candidate_group))

    # section = {"section_id": "323rasf22",
    #            "section_body": "aaabbbccdadlkfjweiokln,mxcvnjnuwefkjnkanvkanunvwkn,nvkjnioufvwojflnwalfnwoiafnlkanflksnvlsjvoiwvonebebenbeoeoihro"}
    # articles = [
    #     {"articles_id": "2222", "articles_url": "www.google.com",
    #         "articles_body": "saldkfjalksdfjklsjdfklajskldfjl"},
    #     {"articles_id": "090080", "articles_url": "www.yahoo.com",
    #         "articles_body": "5678908765467890-98765467890"},
    #     {"articles_id": "2222", "articles_url": "www.google.com",
    #         "articles_body": "saldkfjalksdfjklsjdfklajskldfjl"},
    #     {"articles_id": "090080", "articles_url": "www.yahoo.com",
    #         "articles_body": "5678908765467890-98765467890"},
    #     {"articles_id": "2222", "articles_url": "www.google.com",
    #         "articles_body": "saldkfjalksdfjklsjdfklajskldfjl"},
    #     {"articles_id": "090080", "articles_url": "www.yahoo.com",
    #         "articles_body": "5678908765467890-98765467890"},
    #     {"articles_id": "2222", "articles_url": "www.google.com",
    #         "articles_body": "saldkfjalksdfjklsjdfklajskldfjl"},
    #     {"articles_id": "090080", "articles_url": "www.yahoo.com",
    #         "articles_body": "5678908765467890-98765467890"}
    # ]
