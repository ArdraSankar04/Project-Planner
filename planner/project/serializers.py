from rest_framework import serializers
from . models import Project
from . models import AssignedProjects
from authentication.serializers import ProfileSerializer
from authentication.models import Profile
from .models import Task

class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model=Project
        fields='__all__'
        read_only_fields=['active_status']

class ProjectField(serializers.PrimaryKeyRelatedField):
    def get_attribute(self, instance):
        return getattr(instance,self.source_attrs[0])

    def to_representation(self, value):
        return ProjectSerializer(value).data

class ProfileField(serializers.PrimaryKeyRelatedField):
    def get_attribute(self, instance):
        return getattr(instance,self.source_attrs[0])
    def to_representation(self, value):
        return ProfileSerializer(value).data

class AssignedProjectsSerializer(serializers.ModelSerializer):

    project=ProjectField(queryset=Project.objects.all())
    coordinator=ProfileField(queryset=Profile.objects.filter(role='Project Coordinator'))
    developers=ProfileField(queryset=Profile.objects.filter(role='Developer'),many=True)

    class Meta:
        model=AssignedProjects
        fields='__all__'
        read_only_fields=['active_status']

class AssignedProjectField(serializers.PrimaryKeyRelatedField):
    def get_attribute(self, instance):
        return getattr(instance,self.source_attrs[0])
    def to_representation(self, value):
        return AssignedProjectsSerializer(value).data

class TaskSerializer(serializers.ModelSerializer):

    assigned_project=AssignedProjectField(read_only=True)
    assigned_to=ProfileField(queryset=Profile.objects.filter(role='Developer'))
    
    class Meta:
        model=Task
        fields='__all__'
        read_only_fields=['active_status']