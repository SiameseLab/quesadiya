from django.shortcuts import render
# from .models import ProjectInfo 
from tool import models
#from .serializers import ProjectInfoSerializer
  
def ProjectInfo(request): 
    infos = models.ProjectInfo.objects.all()
    section = { "section_id":"323rasf22", "section_body":"aaabbbccdadlkfjweiokln,mxcvnjnuwefkjnkanvkanunvwkn,nvkjnioufvwojflnwalfnwoiafnlkanflksnvlsjvoiwvonebebenbeoeoihro" }
    articles = [
        {"articles_id":"2222", "articles_url":"www.google.com","articles_body":"saldkfjalksdfjklsjdfklajskldfjl"},
    {"articles_id":"090080", "articles_url":"www.yahoo.com","articles_body":"5678908765467890-98765467890"},
    {"articles_id":"2222", "articles_url":"www.google.com","articles_body":"saldkfjalksdfjklsjdfklajskldfjl"},
    {"articles_id":"090080", "articles_url":"www.yahoo.com","articles_body":"5678908765467890-98765467890"},
    {"articles_id":"2222", "articles_url":"www.google.com","articles_body":"saldkfjalksdfjklsjdfklajskldfjl"},
    {"articles_id":"090080", "articles_url":"www.yahoo.com","articles_body":"5678908765467890-98765467890"},
    {"articles_id":"2222", "articles_url":"www.google.com","articles_body":"saldkfjalksdfjklsjdfklajskldfjl"},
    {"articles_id":"090080", "articles_url":"www.yahoo.com","articles_body":"5678908765467890-98765467890"}
    ]
    #serializer_class = ProjectInfoSerializer
    # context = serializer_class
    
    context_dict = {'infos': infos, 'section':section, 'articles':articles}
    
    return render(request, "home.html",context_dict) 