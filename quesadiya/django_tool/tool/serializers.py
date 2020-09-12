from rest_framework import serializers
from tool import models


class ProjectInfoSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'project_name',
            'participants',
            'description',
            'Total',
            'Finish',
            'UnLabled',
            'Abolished'
        )
        model = models.ProjectInfo