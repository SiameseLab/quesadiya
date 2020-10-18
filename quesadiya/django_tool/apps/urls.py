"""quesadiya URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from tool import views as tool_view
from django.shortcuts import redirect
# from django.views.generic.base import RedirectView
# favicon_view = RedirectView.as_view(url='/static/favicon.ico', permanent=True)
urlpatterns = [
    # path(r'^favicon\.ico$', favicon_view),
    path('admin/', admin.site.urls),
    path('auth/login/', tool_view.login, name='login'),
    path('auth/', include('django.contrib.auth.urls')),
    # path('', include("tool.urls")),
    # path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('', tool_view.ProjectInfo, name='home'),
    path('updateAnchor/', tool_view.updateAnchor),
    path('nextAnchor/', tool_view.nextAnchor),
    path('auth/login/', tool_view.login, name='login'),
    path('ReviewDiscarded/', tool_view.ReviewDiscarded, name='ReviewDiscarded'),
    path('reviewDiscarded/', tool_view.reviewDiscarded),
    path('ViewStatus/', tool_view.ViewStatus, name='ViewStatus'),
    path('EditCooperator/', tool_view.EditCooperator, name='EditCooperator'),
    path('updateUser/', tool_view.updateUser),
]
handler404 = 'tool.views.error'
handler500 = 'tool.views.error'
handler400 = 'tool.views.error'
