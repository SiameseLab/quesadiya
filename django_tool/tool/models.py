from django.db import models
   
class ProjectInfo(models.Model): 
    project_name = models.CharField(max_length = 50)
    participants = models.TextField() 
    description = models.TextField() 
    total = models.IntegerField()
    finish = models.IntegerField()
    unLabled = models.IntegerField()
    abolished = models.IntegerField()
    def __str__(self): 
        return self.project_name 

class InputInfo(models.Model): 
    section_id = models.CharField(max_length = 50)
    def __str__(self): 
        return self.project_name 