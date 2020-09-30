from django.db import models


# class Projects(models.Model):
#     # project_id = models.IntegerField()
#     project_name = models.CharField(max_length=30)
#     project_description = models.TextField()

#     class Meta:
#         managed = False
#         db_table = 'projects'

# class Collaborators(models.Model):
#     project = models.ForeignKey('Projects', models.DO_NOTHING)
#     collaborator_name = models.CharField()
#     collaborator_password = models.CharField()

#     class Meta:
#         managed = False
#         db_table = 'collaborators'


# class DjangoSession(models.Model):
#     session_key = models.CharField(primary_key=True, max_length=40)
#     session_data = models.TextField()
#     expire_date = models.DateTimeField()

#     class Meta:
#         managed = False
#         db_table = 'django_session'


# class Projects(models.Model):
#     project_id = models.AutoField()
#     project_name = models.CharField()
#     admin_name = models.CharField()
#     admin_password = models.CharField()
#     date_created = models.DateField()

#     class Meta:
#         managed = False
#         db_table = 'projects'


# class AuthUser(models.Model):
#     password = models.CharField(max_length=128)
#     last_login = models.DateTimeField(blank=True, null=True)
#     is_superuser = models.BooleanField()
#     username = models.CharField(unique=True, max_length=150)
#     last_name = models.CharField(max_length=150)
#     email = models.CharField(max_length=254)
#     is_staff = models.BooleanField()
#     is_active = models.BooleanField()
#     date_joined = models.DateTimeField()
#     first_name = models.CharField(max_length=150)

#     class Meta:
#         managed = False
#         db_table = 'auth_user'


# class CandidateGroups(models.Model):
#     candidate_group_id = models.CharField(max_length=100)
#     candidate_sample = models.ForeignKey(
#         'SampleText', models.DO_NOTHING, max_length=100)

#     class Meta:
#         managed = False
#         db_table = 'candidate_groups'


# class DjangoContentType(models.Model):
#     app_label = models.CharField(max_length=100)
#     model = models.CharField(max_length=100)

#     class Meta:
#         managed = False
#         db_table = 'django_content_type'
#         unique_together = (('app_label', 'model'),)


# class SampleText(models.Model):
#     sample_id = models.CharField(max_length=100)
#     sample_body = models.TextField(blank=True, null=True)
#     sample_title = models.TextField(blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'sample_text'


# class TripletDataset(models.Model):
#     anchor_sample = models.ForeignKey(
#         SampleText, models.DO_NOTHING)
#     candidate_group = models.ForeignKey(CandidateGroups, models.DO_NOTHING)
#     positive_sample = models.ForeignKey(
#         SampleText, models.DO_NOTHING, blank=True, null=True, related_name='positive')
#     negative_sample = models.ForeignKey(
#         SampleText, models.DO_NOTHING, blank=True, null=True, related_name='negative')
#     status = models.CharField(max_length=10)
#     time_changed = models.DateTimeField()

#     class Meta:
#         managed = False
#         db_table = 'triplet_dataset'
