from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from rest_cms.models import Challenge


class Command(BaseCommand):

	def handle(self, *args, **options):
		now = timezone.now()
		Challenge.objects.filter(due_date__lt=now, status=1).update(status=2)

