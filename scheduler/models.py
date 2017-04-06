from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
from datetime import datetime
from django.db.models import Q
from .utils import roundup

WEEKDAY_CHOICES = (
    (0, 'Sunday'),
    (1, 'Monday'),
    (2, 'Tuesday'),
    (3, 'Wednesday'),
    (4, 'Thursday'),
    (5, 'Friday'),
    (6, 'Saturday')
)

MIN_TIME = 8*60
MAX_TIME = 18*60

TIME_CHOICES = ()
for h in range(8, 18):
    for m in (0, 30):
        time_text = "%02d:%02d"%(h, m)
        time_number = h*60 + m
        TIME_CHOICES += ((time_number,time_text),)
TIME_CHOICES += ((MAX_TIME, "18:00"),)

class Job(models.Model):
    title = models.CharField(max_length=200)
    start_time = models.IntegerField(choices=TIME_CHOICES)
    end_time = models.IntegerField(choices=TIME_CHOICES)
    duration = models.IntegerField(validators=[MinValueValidator(1)])
    weekday = models.IntegerField(choices=WEEKDAY_CHOICES)
    location = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s - %s (%s)"%(self.id, self.title, self.location)

    def save(self, *args, **kwargs):
        self.duration = roundup(self.duration)
        self.end_time = self.start_time + self.duration
        super(Job, self).save(*args, **kwargs)

# check whether there is any time conflict
def validate_time(start_time, duration, weekday):
    end_time = start_time + duration

    if end_time > MAX_TIME:
        return False

    clash_filter = (Q(weekday=weekday, start_time__lte=start_time, end_time__gt=start_time) 
                  | Q(weekday=weekday, start_time__lt=end_time, end_time__gte=end_time)
                  | Q(weekday=weekday, start_time__gte=start_time, end_time__lte=end_time))
    
    if Job.objects.filter(clash_filter).exists():
        return False
    else:
        return True

# suggest at most 3 available timeslots to the user
def suggest_timeslot(duration):
    timeslots = []

    for weekday in range(7):
        start_time = MIN_TIME

        while start_time <= MAX_TIME and len(timeslots) < 3:
            if validate_time(start_time, duration, weekday):
                timeslots.append({'start_time': start_time, 'weekday': weekday})

            start_time += 30
    
        if len(timeslots) >= 3: break

    return timeslots