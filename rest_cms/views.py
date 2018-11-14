from django.shortcuts import render
from rest_framework import viewsets, permissions, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework.pagination import LimitOffsetPagination

from . import serializers as custom_serializers, models

# Create your views here.

class CustomUserCreateView(generics.CreateAPIView):
	serializer_class = custom_serializers.CustomUserSerializer
	queryset = models.CustomUser.objects.all()
	permission_classes = (permissions.AllowAny, )


class CustomUserUpdateView(generics.UpdateAPIView):
	serializer_class = custom_serializers.CustomUserSerializer
	queryset = models.CustomUser.objects.all()
	permission_classes = (permissions.IsAuthenticated, )

class SkillListView(generics.ListAPIView):
	serializer_class = custom_serializers.SkillSerializer
	queryset = models.Skill.objects.all()
	permission_classes = (permissions.AllowAny, )
	pagination_class = None																										

class ChallengeListView(generics.ListAPIView):
	serializer_class = custom_serializers.ChallengeSerializer
	permission_classes = (permissions.AllowAny, )

	def get_queryset(self):
		
		if not self.request.query_params.__contains__('skill'):
			return models.Challenge.objects.all()
		else:
			skill = self.request.query_params['skill']
			skill_object = models.Skill.objects.get(skill_name=skill)
			return models.Challenge.objects.filter(skills__in=[skill_object])


class ChallengeRetrieveView(generics.RetrieveAPIView):
	serializer_class = custom_serializers.ChallengeSerializer
	queryset = models.Challenge.objects.all()
	permission_classes = (permissions.AllowAny, )

class SubmissionViewSet(viewsets.ModelViewSet):
	permission_classes = (permissions.IsAuthenticated, )

	def get_serializer_class(self):
		request_method = self.request.method
		print(self.request.FILES)
		if request_method == 'GET' or request_method == 'DELETE':
			return custom_serializers.SubmissionReadSerializer
		return custom_serializers.SubmissionWriteSerializer

	def get_queryset(self):
		request_method = self.request.method
		if request_method == 'GET' or request_method == 'DELETE':
			return models.Submission.objects.filter(submission_user=self.request.user)
		return models.Submission.objects.all()

	def perform_create(self, serializer):
		user = self.request.user
		serializer.save(submission_user=user)
