from django_cron import CronJobBase, Schedule
from django.utils import timezone
from rest_cms.models import Challenge

class MyCronJob(CronJobBase):
    RUN_AT_TIMES = ['00:01'] # every 2 hours

    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'rest_cms.my_cron_job'    # a unique code

    def do(self):
        now = timezone.now()
		Challenge.objects.filter(due_date__lt=now, status=1).update(status=2)