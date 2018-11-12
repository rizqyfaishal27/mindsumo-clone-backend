from django.urls import include, path
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token
from rest_framework import permissions
from . import permissions as custom_permissions

from . import views as rest_cms_views

rest_cms_views_submission_list_create = rest_cms_views.SubmissionViewSet.as_view({
	'post': 'create',
	'get': 'list'
})

rest_cms_views_submission_retrieve_update_destroy = rest_cms_views.SubmissionViewSet.as_view({
	'put': 'update',
	'patch': 'partial_update',
	'get': 'retrieve',
	'delete': 'destroy'
})


urlpatterns = [
	path(r'auth/', obtain_jwt_token),
	path(r'auth-verify/', verify_jwt_token),
	path(r'auth-refresh/', refresh_jwt_token),
	path(r'skills/', rest_cms_views.SkillListView.as_view()),
	path(r'challenges/', rest_cms_views.ChallengeListView.as_view()),
	path(r'challenges/<int:pk>/', rest_cms_views.ChallengeRetrieveView.as_view()),
	path(r'auth-register/', rest_cms_views.CustomUserCreateView.as_view()),
	path(r'users/<int:pk>/', rest_cms_views.CustomUserRetrieveView.as_view()),
	path(r'submissions/', rest_cms_views_submission_list_create),
	path(r'submissions/<int:pk>/', rest_cms_views_submission_retrieve_update_destroy)
]