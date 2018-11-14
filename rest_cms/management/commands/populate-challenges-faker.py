from django_faker import Faker
# this Populator is only a function thats return a django_faker.populator.Populator instance
# correctly initialized with a faker.generator.Generator instance, configured as above
from django.core.management.base import BaseCommand, CommandError
from rest_cms.models import Challenge, CustomUser

class Command(BaseCommand):

	def handle(self, *args, **options):
		populator = Faker.getPopulator()
		populator.addEntity(Challenge, 27)
		insertedPks = populator.execute()
		print(insertedPks)

