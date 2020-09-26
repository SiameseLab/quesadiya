from django import template
from tool import models
import django.conf as conf

register = template.Library()


@register.simple_tag
def getProjects():

    # conf.settings.DATABASES['default']['NAME'] = conf.settings.DATABASES['admin']['NAME']
    # print("db in md:", conf.settings.DATABASES['default']['NAME'])
    # Author.objects.using('default').all()
    projects = models.Projects.objects.using(
        'admin').values("project_id", "project_name")
    # projects = [{"project_name": 'testP'}]
    return projects

    # with connection.cursor() as cursor:
    #     cursor.execute("UPDATE bar SET foo = 1 WHERE baz = %s", [self.baz])
    #     cursor.execute("SELECT foo FROM bar WHERE baz = %s", [self.baz])
    #     row = cursor.fetchone()
