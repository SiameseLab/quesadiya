from django import template
import django.conf as conf
import os.path

register = template.Library()
  
@register.simple_tag
def SelectDB(projectName):
    database = os.path.normpath(os.path.abspath(__file__) + os.sep + os.pardir + os.sep + os.pardir + os.sep + os.pardir+ os.sep + os.pardir + os.sep +"/projects" + os.sep + projectName + os.sep + "project.db")
    print(conf.settings.DATABASES['default']['NAME'])
    # conf.settings.DATABASES['default']['NAME'] = database
    # print(conf.settings.DATABASES['default']['NAME'])
    return database