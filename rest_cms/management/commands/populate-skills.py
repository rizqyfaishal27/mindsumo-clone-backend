from django.core.management.base import BaseCommand, CommandError
from rest_cms.models import Skill
import json


class Command(BaseCommand):

	def handle(self, *args, **options):
		with open('skills.json', 'r') as skills_file:
			json_decoded = json.loads(skills_file.readline())
			Skill.objects.bulk_create([Skill(skill_name=skill) for skill in json_decoded])
			skills_file.close()

