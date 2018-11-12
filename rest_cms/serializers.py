from django.db import transaction, IntegrityError
from rest_framework import status, permissions, serializers
import uuid
from .models import CustomUser, Skill, Submission, Challenge

class SkillSerializer(serializers.ModelSerializer):
	id = serializers.IntegerField(read_only=True)
	updated_at = serializers.DateTimeField(read_only=True)
	created_at = serializers.DateTimeField(read_only=True)

	class Meta:
		model = Skill
		fields = ('skill_name', 'id', 'created_at', 'updated_at', 'is_primary', )

class CustomUserSerializer(serializers.ModelSerializer):
	id = serializers.IntegerField(read_only=True)
	username = serializers.CharField(read_only=True)
	birthdate = serializers.DateField(required=False)
	updated_at = serializers.DateTimeField(read_only=True)
	created_at = serializers.DateTimeField(read_only=True)
	password = serializers.CharField(write_only=True, required=True)
	avatar = serializers.ImageField(use_url=True, max_length=255, required=False)
	skills = SkillSerializer(many=True, read_only=True)
	hometown = serializers.CharField(required=False)
	phone_number = serializers.CharField(required=False)
	facebook_id = serializers.CharField(required=False)
	twitter_id = serializers.CharField(required=False)
	activities_and_interest = serializers.CharField(required=False)
	organization_team_clubs = serializers.CharField(required=False)
	privacy_setting = serializers.IntegerField(required=False)
	is_staff = serializers.BooleanField(read_only=True)

	class Meta:	
		model = CustomUser
		fields = ('first_name', 'last_name', 'email', 'updated_at', 'created_at', \
			'avatar', 'username', 'birthdate', 'avatar', 'skills', 'hometown', 'phone_number', \
			'facebook_id', 'twitter_id', 'activities_and_interest', 'organization_team_clubs', 'privacy_setting', \
			'is_staff', 'id', 'password', )

	def create(self, validated_data):
		password = validated_data.pop('password', None)
		instance = self.Meta.model(**validated_data)
		first_name = validated_data.pop('first_name', None)
		username = first_name + "_" + str(uuid.uuid4())
		instance.username = username
		instance.set_password(password)
		instance.save()
		return instance

	def update(self, instance, validated_data):
		for attr, value in validated_data.items():
			if attr == 'password':
				instance.set_password(value)
			else:
				setattr(instance, attr, value)
		instance.save()
		return instance

class ChallengeSerializer(serializers.ModelSerializer):
	updated_at = serializers.DateTimeField(read_only=True)
	created_at = serializers.DateTimeField(read_only=True)
	author = CustomUserSerializer(read_only=True)
	skills = SkillSerializer(many=True, read_only=True)
	price = serializers.DecimalField(read_only=True, decimal_places=2, max_digits=10)
	due_date = serializers.DateField(read_only=True)
	description = serializers.CharField(read_only=True)
	deliverables = serializers.CharField(read_only=True)
	status = serializers.BooleanField(read_only=True)
	is_anonymous_author = serializers.BooleanField(read_only=True)
	banner_image = serializers.ImageField(use_url=True, read_only=True)
	title = serializers.CharField(read_only=True)
	id = serializers.IntegerField(read_only=True)
	total_submission = serializers.SerializerMethodField()
	next_challenge_id = serializers.SerializerMethodField(read_only=True)
	next_challenge_title = serializers.SerializerMethodField(read_only=True)

	def get_total_submission(self, obj):
		return obj.submission_set.count()

	def get_next_challenge_id(self, obj):
		id = obj.id
		challenge = Challenge.objects.filter(id__gt=id).first()
		if challenge is not None:
			return challenge.id
		else:	
			return -1

	def get_next_challenge_title(self, obj):
		id = obj.id
		challenge = Challenge.objects.filter(id__gt=id).first()
		if challenge is not None:
			if len(challenge.title) > 25:
				return challenge.title[0:25] + '...'
			else:
				return challenge.title
		else:	
			return None

	class Meta:
		model = Challenge
		fields = ('id', 'created_at', 'updated_at', 'author', 'skills', 'price', 'due_date', 'description', 'deliverables', \
			'status', 'is_anonymous_author', 'banner_image', 'title', 'total_submission', 'next_challenge_id', 'next_challenge_title', )


class SubmissionWriteSerializer(serializers.ModelSerializer):
	challenge = serializers.PrimaryKeyRelatedField(required=True, queryset=Challenge.objects.all())
	submission_title = serializers.CharField(min_length=10, max_length=100, required=True)
	submission_text = serializers.CharField(required=True)
	submission_file = serializers.FileField(use_url=True, required=False)
	updated_at = serializers.DateTimeField(read_only=True)
	created_at = serializers.DateTimeField(read_only=True)

	class Meta:
		model = Submission
		fields = ('created_at', 'updated_at', 'challenge', 'submission_user', 'submission_title', \
			'submission_text', 'submission_file', )


class SubmissionReadSerializer(serializers.ModelSerializer):
	id = serializers.IntegerField(read_only=True)
	challenge = ChallengeSerializer()
	submission_user = CustomUserSerializer()
	submission_title = serializers.CharField(read_only=True)
	submission_text = serializers.CharField(read_only=True)
	submission_file = serializers.FileField(use_url=True, read_only=True)
	updated_at = serializers.DateTimeField(read_only=True)
	created_at = serializers.DateTimeField(read_only=True)

	class Meta:
		model = Submission
		fields = ('created_at', 'updated_at', 'challenge', 'submission_user', 'submission_title', \
			'submission_text', 'id', 'submission_file', )


# class AttachmentFileReadSerializer(serializers.ModelSerializer):
# 	id = serializers.IntegerField(read_only=True)
# 	file = serializers.FileField(use_url=True, read_only=True)
# 	updated_at = serializers.DateTimeField(read_only=True)
# 	created_at = serializers.DateTimeField(read_only=True)

# 	class Meta:
# 		model = AttachmentFile
# 		fields = ('created_at', 'updated_at', 'id', 'file', )


# class AttachmentFileWriteSerializer(serializers.ModelSerializer):
# 	file = serializers.FileField(use_url=True)
# 	updated_at = serializers.DateTimeField(read_only=True)
# 	created_at = serializers.DateTimeField(read_only=True)

# 	class Meta:
# 		model = AttachmentFile
# 		fields = ('created_at', 'updated_at', 'file', )
