from django import template
from tool import models
import django.conf as conf

register = template.Library()


@register.simple_tag
def getProjects():
    projects = models.Projects.objects.using(
        'admin').values("project_id", "project_name")
    return projects
